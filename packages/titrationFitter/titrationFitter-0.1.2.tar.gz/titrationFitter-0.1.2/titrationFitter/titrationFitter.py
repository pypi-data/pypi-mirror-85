# -*- coding: utf-8 -*-
"""
Frédéric Dux @ 2017


Implements a simulation of a titration, for a system of two main components,
N species and N-1 equilibrium constants.
Some species (composed usually of a combination of a metal (M) and of a ligand (L),
with a given UV-VIS spectrum) are contained in a flask. More of a solution of
a ligand or of the metal (the titrant) is added to the flask, modifying the concentrations
of the species depending on the metal/ligand concentrations ratio.
The UV-VIS spectra are recorded experimentally at each step of the titration,
and the routines contained in this script try to obtain a best fit of the data
by finding the equilibrium constants that will describe best the concentrations 
of the species. If the UV-VIS spectra of a given species is not known, its values
will be added to the variables to be optimized.

Example:
a flask contains M
L is added to the flask, generating the species ML and ML2
The spectra of L and M are known, but not those of ML and ML2.
The initial guess for ML2 is given by the end result of the titration, when
L is in large excess compared to M

"""
import     numpy                 as      np 
from       scipy.optimize        import  fsolve, least_squares,\
                                         root
import     pickle
import     matplotlib.pyplot     as      plt
from       matplotlib.widgets    import  Slider
import     matplotlib            as      mpl
from       mpl_toolkits.mplot3d  import  Axes3D

class Component:
    """
    class attributes:
        - eqconst      :  Equilibrium constant for the formation of this Component
        - buildblocks  :  List of the species that together build the Component. 
                           (other Components, Ex: ML2 asks for the list [M,L])
        - coeffs       :  List of the same length as that of buildblocks, containing
                           the number of each component, Ex: ML2 asks for the list [1,2])
        - name         :  Used when building other Components, essential if
                           the current Component is a raw building block.
                           (Ex: L or M from ML2, which are not composed)
        - uvvis        :  Contains the numpy array with the current uv spectrum. 
                           its span corresponds to that of the linked system.
                           Can be None if no initial spectrum is known.
        - uv_known     :  Boolean, whether or not the uvvis entry has to be optimized.
        - eqconst_known:  Boolean, whether or not the affinity/formation constant
                           has to be optimized.
        - linked       :  Another component that has the same uv spectrum.
                           If the Component is linked, only the uv spectrum of the
                           reference instance will be optimized. 
        - titrant      :  Boolean flag indicating that this component is added
                           to the flask.
    """
    def __init__(self, eqconst=0, conc_ini=0, buildblocks=[], coeffs=[], name="", uvvis=None,\
                 uv_known=False, eqconst_known=False, linked=None, titrant=False):
        self.eqconst     =  eqconst
        self.buildblocks =  buildblocks
        self.coeffs      =  coeffs
        self.name        =  name
        if uvvis is not None:
            self.uvvis       =  np.copy(uvvis)
        else:
            self.uvvis       =  None
        self.uv_known    =  uv_known
        self.linked      =  linked
        self.conc_ini    =  conc_ini
        self.titrant     =  titrant


        # float concentration attribute
        self.conc        =  0.

        # safety checks:
        if len(buildblocks)!= len(coeffs):
            raise(Exception("Wrong list of building blocks or coefficients"))
        if uv_known and uvvis is None:
            raise(Exception("No spectrum provided"))
        if not uv_known and linked:
            print(("Warning, spectrum set to be optimized, but a component \
                   was linked. "+name+".uv_known set to True."))
        if name=="" and len(coeffs) == 0:
            raise(Exception("Raw building block with no name provided."))
        
        self.eqconst_known = eqconst_known
        self.deqconst = 0
        if len(buildblocks) == 0:
            self.eqconst_known = True
        
        if self.linked is not None:
            self.uvvis = linked.uvvis
                
        
        ## for mass balance, a dictionnary containing the number of brick in the component:
        self.composition = {}
        liste = []
        self.atomize(liste)
        for entry in liste:
            key = list(entry.keys())[0]
            val = entry[key]
            if key in list(self.composition.keys()):
                self.composition[key] += val
            else:
                self.composition[key] = val
                
                
        ### constructing the name:

        if len(coeffs)!=0:
            for block,coeff in zip(buildblocks,coeffs):
                if len(block.buildblocks) != 0:
                    if coeff == 1:
                        self.name += "+(" + block.name + ")+"
                    else:
                        self.name += "+("+block.name+")"+str(coeff)+"+"
                else:
                    if coeff == 1:
                        strcoeff = ""
                    else:
                        strcoeff = str(coeff)
                    self.name += block.name+strcoeff
                if self.name[-1] == "+":
                    self.name = self.name[:-1]
                if self.name[0] == "+" :
                    self.name = self.name[1:]
                self.name = self.name.replace('++','+')
                
        
            
    def __repr__(self):
        return self.name +  "\t: " + str(self.conc)
    
    def visUVVIS(self):
        plt.figure()
        plt.plot(self.uvvis)
        plt.show()
    
    def atomize(self,liste):
        if len(self.buildblocks) == 0:
            liste.append({self: 1})
        else:
            for bloc,N in zip(self.buildblocks,self.coeffs):
                for i in range(N):
                    bloc.atomize(liste)


class System:
    """
    class attributes:
        - bricks     : a list of the raw Components (M, L from ML2)
        - components : a list of Component instances (ML, ML2 ...)
        - span       : x-axis of the uv spectrum that is going to be used.
    """
    def __init__(self, bricks, components, conc_ini, span=np.linspace(200,400)):
        self.bricks       =  bricks
        self.components   =  components
        self.span         =  span
        self.titrantconc  =  0
        self.titrant      =  None
        self.initializeSpectrumComponents()
        self.conc_ini     =  conc_ini
        
        # check that a single brick or component is a titrant:
        for brick in bricks:
            if brick.titrant == True:
                self.titrant = brick
        for comp in components:
            if comp.titrant  == True:
                self.titrant = comp
        if self.titrant is None:
            raise(Exception("No titrating agent provided to the system. Stop !"))
                
        
    def __repr__(self):
        rep = ""
        for brick in self.bricks: 
            rep += brick.name +"\t: "+ str(brick.conc) + "\n"
        for comp in self.components:
            rep += comp.__repr__() + "\n"
        return rep

    def getAllConcs(self):
        liste = [brick.conc for brick in self.bricks]
        liste.extend([comp.conc for comp in self.components])
        liste = np.array(liste)
        liste[liste < 0] = 0
        return liste
    
    def concBalance(self, concs):
        """
            mass balance and equilibrium equations, returns
            a system of equations allowing to compute the concentrations
            given the equilibrium and affinity constants of the system.
        """

        # redistribute the concentrations for easier access.
        i  = 0
        for brick in self.bricks:
            brick.conc = concs[i]
            i += 1
        for comp in self.components:
            comp.conc  = concs[i]
            i += 1
        
        # list containing the equations
        equations = []
        # the mass of each brick must be conserved, yielding Nbricks mass
        # conservation equations:
        for brick in self.bricks:
            if brick.titrant:
                balance = -self.titrantconc  + brick.conc 
            else:
                balance = -brick.conc_ini    + brick.conc
                
            for comp in self.components:
                for key in list(comp.composition.keys()):
                    if key == brick:
                        balance += comp.conc * comp.composition[key]
            equations.append(balance)
        

        # now the equilibrium equations, as many as we have components:
        for comp in self.components:
            balance = comp.conc 
            removal_from_balance = 1.
            for block, j in zip(comp.buildblocks, comp.coeffs):
                removal_from_balance *= block.conc ** j
            removal_from_balance *= comp.eqconst
            balance -= removal_from_balance
            equations.append(balance)

        return np.array(equations)
    
    def concBalanceSum(self, concs):
        return np.sum(self.concBalance(concs)**2)
    
    def calcConcs(self):
        """
            computes the current concentrations given the equilibrium constant
            of each Component.
        """
        concs = np.ones_like(self.getAllConcs())*self.conc_ini# initial guess
        
        sol = fsolve(self.concBalance, concs)
        i = 0
        try_least_squares = False
        while (sol<-0.0001).any():
            sol = fsolve(self.concBalance, np.abs(sol))
            if i > 100:
                try_least_squares = True
                break
                # return np.abs(sol)
            i+=1
        if try_least_squares:
            sol2 = least_squares(self.concBalanceSum, np.abs(sol), 
                                 bounds=(0, np.inf))
            if sol2.success:
                sol = sol2.x 
            else:
                sol = np.abs(sol)
                print('warning: solving for the concentrations failed.')
                return
        i = 0
        for brick in self.bricks:
            brick.conc = sol[i]
            i += 1
        for comp in self.components:
            comp.conc = sol[i]
            i += 1


    
    def initializeSpectrumComponents(self):
        """ 
            provides an "initial guess" for unknown uv spectra 
        """
        for brick in self.bricks:
            if not brick.uv_known and brick.uvvis is None:
                brick.uvvis = np.ones_like(self.span)*0.1
        for component in self.components:
            if not component.uv_known and component.uvvis is None:
                component.uvvis = np.ones_like(self.span)*0.1
                
    def generateUVSpectrum(self):
        """ 
            under the assumption of a linear response to the concentration,
            computes the UV Spectrum by linear combination of the different basis
            and concentrations 
        """
        spectr = np.zeros_like(self.span)
        for brick in self.bricks:
            spectr += brick.conc     *  brick.uvvis
        for component in self.components:
            spectr += component.conc *  component.uvvis
        return spectr




class Boundaries(object):
    """ utility class for the hopping solver in Titration.optimize """
    def __init__(self,xmin):
        self.xmin = np.array(xmin)
    def __call__(self, **kwargs):
        x = kwargs["x_new"]
        tmin = bool(np.all(x>=self.xmin))
        return tmin


class Titration:
    """ class containing the span of equivalents applied to the system,
        and the global optimisation routines
            - system: A system object as defined by the System class
            
            - eqspan: an array containing the different points of the titration
                       in terms of equivalents
            - exp   : 2d array containing the uv-vis spectra, one uv-vis spectrum per column.
            
    """
    def __init__(self, system, eqspan, exp, volumes=None):
        self.system      = system
        self.eqspan      = eqspan
        self.exp         = exp
        if volumes is None:
            volumes = np.ones_like(eqspan)
        self.volumes     = volumes
        self.concProfile = {}
        self.optstatus   = {}
        self.iteration_number = 0

    
    def observableFromModel(self):
        alluvs = []
        #reset the concentrations profiles:
        for brick in self.system.bricks:
            self.concProfile[brick.name] = []
        for comp  in self.system.components:
            self.concProfile[comp.name]  = []
            
        # now from the model, compute and store all the concentrations
        for eq, vol in zip(self.eqspan, self.volumes):
            self.system.titrantconc = eq * self.system.conc_ini
            self.system.calcConcs()
            for brick in self.system.bricks:
                self.concProfile[brick.name].append(brick.conc)
            for comp  in self.system.components:
                self.concProfile[comp.name].append(comp.conc)
            uv_eq = self.system.generateUVSpectrum()
            uv_eq = np.array(uv_eq) / (vol / self.volumes[0])
            alluvs.append(uv_eq)
        # get all the data in a 2d-array, to be directly compared with the raw data.
        stacked = np.vstack(alluvs).transpose()
        return stacked

    def observableFromModel_concentration(self):
        alluvs = []
        for eq in self.eqspan:
            uv_eq = self.system.generateUVSpectrum()
            uv_eq = np.array(uv_eq)
            alluvs.append(uv_eq)
        # get all the data in a 2d-array, to be directly compared with the raw data.
        stacked = np.vstack(alluvs).transpose()
        return stacked            

        
    def residuals(self, params):
        # from the least squares perspective.
        i = 0
        params = np.abs(params)
        for brick in self.system.bricks:
            if not brick.eqconst_known:
                brick.eqconst = params[i]
                i += 1
            if not brick.uv_known:
                brick.uvvis   = params[i:i+len(brick.uvvis)]
                i += len(brick.uvvis)
        for comp in self.system.components:
            if not comp.eqconst_known:
                comp.eqconst = params[i]
                i += 1
            if not comp.uv_known:
                comp.uvvis   = params[i:i+len(comp.uvvis)]
                i += len(comp.uvvis)
        res = np.sum((self.exp-self.observableFromModel())**2)
    
        return res
    
    def residuals_root(self, params):
        # from the least squares perspective.
        params = np.abs(params)
        i = 0
        for brick in self.system.bricks:
            if not brick.uv_known:
                brick.uvvis[:]   = params[i:i+len(brick.uvvis)]
                i += len(brick.uvvis)
        for comp in self.system.components:
            if not comp.eqconst_known:
                comp.eqconst = params[i]
                i += 1
            if not comp.uv_known:
                comp.uvvis[:]   = params[i:i+len(comp.uvvis)]
                i += len(comp.uvvis)
                
                
        self.iteration_number += 1 
        obs_sim = self.observableFromModel()
        if self.iteration_number % 10 == 0:
            print("Current status:")
            self.printCurrentModel(result=obs_sim)
        
        return (self.exp-obs_sim).flatten('K')
    
    
    
    def optimize(self, optimize_uv=True, update_values=True):
        x0 = np.array([])
        # bounds = [] # prepare the bounds for x.
        for brick in self.system.bricks:
            if not brick.uv_known:
                if optimize_uv:
                    uvvis   = brick.uvvis
                    x0 = np.append(x0, uvvis)
                    # for e in uvvis:
                        # bounds.append((0,1))
        for comp in self.system.components:
            if not comp.eqconst_known:
                eqconst = np.array([comp.eqconst])
                x0 = np.append(x0, eqconst)
                # bounds.append((0,30))
            if not comp.uv_known:
                if optimize_uv:
                    uvvis   = comp.uvvis
                    x0 = np.append(x0, uvvis)
                    # for e in uvvis:
                        # bounds.append((0,1))
        if len(x0) == 0:
            print("No variable to to be optimized.")
            return
        print("Titration.optimize: array of length "+str(len(x0))+" to be optimized.")
        res = root(self.residuals_root, x0=x0, method='lm', tol=1e-9)
        res.x = np.abs(res.x)
        #std   = np.sqrt(np.diag(res.cov_x))

        
        if update_values:
            # putting back the optimized values in the system:
            i = 0
            for brick in self.system.bricks:
                if optimize_uv:
                    if not brick.uv_known:
                        brick.uvvis[:]   = res.x[i:i+len(comp.uvvis)]
                        i += len(comp.uvvis)
            for comp in self.system.components:
                if not comp.eqconst_known:
                    comp.eqconst = res.x[i]
                    #comp.deqconst = std[i]
                    i += 1
                if optimize_uv:
                    if not comp.uv_known:
                        comp.uvvis[:]   = res.x[i:i+len(comp.uvvis)]
                        i += len(comp.uvvis)
            #update the system with the new parameters
            self.system.calcConcs()
        self.optstatus = res.message
        self.res       = res
        #if optimize_uv or update_values:
        #    self.errorEstimate()

        
    def residuals_concentration_root(self, params):
        # from the least squares perspective.
        params = np.abs(params)
        i = 0
        for brick in self.system.bricks:
            self.concProfile[brick.name]=params[i:i+len(self.eqspan)]
            i += len(self.eqspan)
            if not brick.uv_known:
                brick.uvvis[:]   = params[i:i+len(brick.uvvis)]
                i += len(brick.uvvis)
        for comp in self.system.components:
            self.concProfile[comp.name]=params[i:i+len(self.eqspan)]
            i += len(self.eqspan)
            if not comp.uv_known:
                comp.uvvis[:]   = params[i:i+len(comp.uvvis)]
                i += len(comp.uvvis)
        # now, all the concentrations and the uv spectra were put back
        # in their respective instances. We can calculate the resultant
        # uv spectrum the usual way.
        # this is done by the function this->observableFromModel_concentrations()
        return (self.exp-self.observableFromModel_concentration()).flatten('K')
            
    def optimize_concentration_root(self):
        #reset the concentration profile
        for brick in self.system.bricks:
            self.concProfile[brick.name] = np.ones_like(self.eqspan)
        for comp  in self.system.components:
            self.concProfile[comp.name]  = np.ones_like(self.eqspan)
        x0 = np.array([])

        for brick in self.system.bricks:
            x0 = np.append(x0, self.concProfile[brick.name])
            if not brick.uv_known:
                uvvis   = brick.uvvis
                x0 = np.append(x0, uvvis)
        for comp in self.system.components:
            x0 = np.append(x0, self.concProfile[comp.name])
            if not comp.uv_known:
                uvvis   = comp.uvvis
                x0 = np.append(x0, uvvis)
        root(self.residuals_concentration_root, x0=x0, method='lm')
        #done.
        self.optstatus = x0
        
    def errorEstimate(self):
        self.optimize(optimize_uv=False, update_values=False)
        
    def plotCurrentModel(self):
        """
        PLOTTING THE USEFUL INFORMATION
        """
        global result, uvs, t1, seq
        eqs  = self.eqspan
        span = self.system.span
        fig  = plt.figure(figsize=(9,7))
        result = self.observableFromModel()
        uvs = self.exp
        
        ax1 = fig.add_subplot(221)
        ax1.set_title("UV-Vis evolution")
        ax1.set_ylim((min(np.min(uvs), np.min(result)), max(np.max(uvs), np.max(result))))
        axcolor   = 'lightgoldenrodyellow'
        i = 0
        axeq      = plt.axes([0.09, 0.9, 0.23, 0.015], facecolor=axcolor)
        seq       = Slider(axeq, 'eq', 0, len(eqs)-1, valinit=0, valstep=1)
        seq.valtext.set_visible(False)
        t1        = plt.text(0.5, 1.2, f'eq: {eqs[i]}')
        expplot,  = ax1.plot(span, uvs[:, i], label='Experimental')
        fitplot,  = ax1.plot(span, result[:,i], label='Fit')
        ax1.legend(loc='upper right')
        def press(event):
            try:
                button = event.button
            except:
                button = 'None'
            if event.key == 'right' or button == 'down':
                if seq.val < len(eqs) - 1:
                    seq.set_val(seq.val + 1)
            elif event.key == 'left' or button == 'up':
                if seq.val > 0:
                    seq.set_val(seq.val - 1)
            eqi0 = int(seq.val)
            t1.set_text(f'eq: {eqs[eqi0]:.02f}')
            # im.set_data(dic_of_images[datetimes[indexvalue]])
            update(seq.val)
            fig.canvas.draw_idle()

        def reset(event):
            seq.reset()
        def update(val):
            eqi0 = int(seq.val)
            t1.set_text(f'eq: {eqs[eqi0]:.02f}')
            expplot.set_ydata(uvs[:,eqi0])
            fitplot.set_ydata(result[:,eqi0])
            fig.canvas.draw_idle()
        ax2 = fig.add_subplot(222,projection='3d')
        ax2.set_title("UV-Vis residuals")
        x,y = np.meshgrid(eqs,span)
        ax2.plot_surface(x,y,result-uvs)
        plt.legend(frameon=False)
        
        ax3 = fig.add_subplot(223)
        ax3.set_title("Concentration profiles")
        for key in list(self.concProfile.keys()):
            ax3.plot(eqs,self.concProfile[key],label=key)
        plt.legend(frameon=False)
        
        
        
        ax4 = fig.add_subplot(224)
        ax4.set_title("UV-Vis spectras")
        toplot = {}
        for brick in self.system.bricks:
            toplot[brick.name] = brick.uvvis
        for comp in self.system.components:
            toplot[comp.name] = comp.uvvis
        for key in list(toplot.keys()):
            ax4.plot(self.system.span,toplot[key],label=key)
        plt.legend(frameon=False)
        plt.tight_layout()
        fig.canvas.mpl_connect('key_press_event', press)
        fig.canvas.mpl_connect('scroll_event', press)
        seq.on_changed(update)
        plt.show()
        
    def printCurrentModel(self, result=None):
        print("############ binding constants:")
        for comp in self.system.components:
            print(f"{comp.name+':':<10} 10^{np.log10(comp.eqconst):.3f}")
        if result is None:
            result    = self.observableFromModel()
        residuals = np.sum((self.exp-result)**2)
        self.printed_residuals = residuals
        print("############ final residuals:")
        print(f"{residuals:.03e}")



    def saveModel(self, filename):
        with open(filename, 'wb') as output:  # Overwrites any existing file.
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
        
def loadModel(filename):
    with open(filename, 'rb') as inp: 
        titration = pickle.load(inp)
    return titration 


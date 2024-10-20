import numpy as np
from pint import UnitRegistry
ureg = UnitRegistry()

class constant():
    def __init__(self,
                 value:float,
                 abbrev:str         = '',
                 name:str           = '', 
                 uncertainty:float  = 0,
                 unit:str           = '',
                 system:str         = '',
                 value_ref:str      = '',
                 value_ref_link:str = '',
                 u_ref:str          = '',
                 u_ref_link:str     = '',
                 **kwargs):
    
        #### User Defined Attributes
        self.abbrev         = abbrev
        self.name           = name
        self.value          = value
        self.u              = uncertainty
        self.unit           = ureg(unit)
        self.system         = system
        self.value_ref      = value_ref
        self.value_ref_link = value_ref_link
        self.u_ref          = u_ref
        self.u_ref_link     = u_ref_link
        self.unit_error     = False
        
    #%% Dunder Methods
    def __repr__(self) -> str:
        return str(self.value)
    
    def __add__(self,val) -> float:
        if type(val) is float:
            new_const = self.value+val
        else:
            new_const       = constant(self.value+val.value)
            new_const.u     = np.sqrt(self.u**2 + val.u**2)
            try:
                new_const.unit  = self.unit+val.unit
            except:
                new_const.unit_error    = True
            
        return new_const
        
    def __radd__(self,val) -> float:
        if type(val) is float:
            new_const = self.value+val
        else:
            new_const       = constant(self.value+val.value)
            new_const.u     = np.sqrt(self.u**2 + val.u**2)
            try:
                new_const.unit  = self.unit+val.unit
            except:
                new_const.unit_error    = True

        return new_const

    def __sub__(self,val) -> float:
        if type(val) is float:
            new_const = self.value-val
        else:
            new_const       = constant(self.value-val.value)
            new_const.u     = np.sqrt(self.u**2 + val.u**2)
            try:
                new_const.unit  = self.unit-val.unit
            except:
                new_const.unit_error    = True
            
        return new_const
        
    def __rsub__(self,val) -> float:
        if type(val) is float:
            new_const = self.value-val
        else:
            new_const       = constant(self.value-val.value)
            new_const.u     = np.sqrt(self.u**2 + val.u**2)
            try:
                new_const.unit  = self.unit-val.unit
            except:
                new_const.unit_error    = True
            
        return new_const
    
    def __mul__(self,val) -> float:
        if type(val) is float:
            new_const = self.value*val
        else:
            new_const       = constant(self.value*val.value)
            new_const.u     = np.sqrt(self.u**2 + val.u**2)
            try:
                new_const.unit  = self.unit*val.unit
            except:
                new_const.unit_error    = True
            
        return new_const
        
    def __rmul__(self,val) -> float:
        if type(val) is float:
            new_const = self.value*val
        else:
            new_const       = constant(self.value*val.value)
            new_const.u     = np.sqrt(self.u**2 + val.u**2)
            try:
                new_const.unit  = self.unit*val.unit
            except:
                new_const.unit_error    = True

        return new_const

    
    def __truediv__(self,val) -> float:
        try:
            return float(self.value/val)
        except:
            pass
        
        try:
            return float(self.value/val.value)
        except:
            return False
        
    def __rtruediv__(self,val) -> float:
        try:
            return float(self.value/val)
        except:
            pass
        
        try:
            return float(self.value/val.value)
        except:
            return False
        
        

        
    #%% Normal Methods
    def get(self) -> float:
        '''
        Returns value of the constant.

        Returns
        -------
        float
            Returns value of the constant.

        '''
        return float(self.value)

#%% Template
if __name__ == "__main__":
    sigma   = constant(
                        abbrev          = 'sigma',
                        name            = 'Stefan-Boltzmann constant',
                        value           = 5.670374419*(10**(-8)),
                        uncertainty     = 0,
                        unit            = 'W/(m^2*K^4)',
                        value_ref       = 'NIST',
                        value_ref_link  = 'https://physics.nist.gov/cgi-bin/cuu/Value?sigma',
                        u_ref           = 'NIST',
                        u_ref_link      = 'https://physics.nist.gov/cgi-bin/cuu/Value?sigma'
                       )
    
    AU   = constant(
                        abbrev          = 'AU',
                        name            = 'astronomical unit',
                        value           = 1.49597870700*(10**11),
                        uncertainty     = 3,
                        unit            = 'm',
                        value_ref       = 'IAU',
                        value_ref_link  = 'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                        u_ref           = 'IAU',
                        u_ref_link      = 'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf'
                       )
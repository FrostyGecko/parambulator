#%% MATH CONSTANTS
#### Unit Conversions
deg2rad = 3.14159265358979/180  # [rad/deg]
rad2deg = 180/3.14159265358979  # [deg/rad]
day2sec = 24*60*60              # [sec/day]
sec2day = 1/day2sec             # [day/sec]

#### Physical Constants
G       = 6.6738*(10**(-20))    # [km^3 kg^-1 s^-2]


__all__ = {
    "earthJ2"
    }

class constant():
    def __init__(self,
                 abbrev:str,
                 name:str, 
                 value:float,
                 unit:str,
                 uncertainty:float,
                 reference:str,
                 system:str,
                 ):
    
        self.abbrev         = abbrev
        self.name           = name
        self.value          = value
        self.unit           = unit
        self.uncertainty    = uncertainty
        self.reference      = reference
        self.system         = system

    def __repr__(self):
        return str(self.value)
    
    def __add__(self,add_val):
        return float(self.value+add_val)
    
    def val(self):
        return float(self.value)
        
        
        
earthJ2 = constant('earthJ2','Earth J2 constant',1,None,None,None,None)
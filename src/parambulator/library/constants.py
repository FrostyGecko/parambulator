import numpy as np

class constant():
    def __init__(self,
                 abbrev:str,
                 name:str, 
                 value:float,
                 uncertainty:float=0,
                 unit:str='',
                 system:str='',
                 value_ref:str='',
                 value_ref_link:str='',
                 u_ref:str='',
                 u_ref_link:str='',
                 **args):
    
        #### User Defined Attributes
        self.abbrev         = abbrev
        self.name           = name
        self.value          = value
        self.u              = uncertainty
        self.unit           = unit
        self.system         = system
        self.value_ref      = value_ref
        self.value_ref_link = value_ref_link
        self.u_ref          = u_ref
        self.u_ref_link     = u_ref_link
        
        #### Units
        self.units_length   = {'mm':0.001, 
                                'cm':0.01, 
                                'm' :1.0, 
                                'km':1000.0, 
                                'AU':149597870700.0 ,
                                'ly':9460730472580800.0,
                                'mile':1/0.000621371,
                                'ft':1/3.28084,
                                'in':1/39.3701}
            
        self.units_angle    = {'arcseconds': 1/3600, 
                                'arcminutes': 1/60, 
                                'deg': 1,
                                'rad': 180/np.pi}
        
        self.units_time     = {'s': 1,  
                                'min': 60, 
                                'hour': 24,
                                'day': 86400}
        
        self.units_mass     = {'mg': 1e-6, 
                                'g': 0.001, 
                                'kg': 1,
                                'solar mass':1.9884158605722266e+30,
                                'lb':1/2.20462,
                                'oz':1/35.274}
        
        self.units_temp    = {'mC':0.001,
                                'cC':0.01,
                                'dC':0.1,
                                'C':1,
                                'daC':10,
                                'hC':100,
                                'kC':1000,
                                'mK':0.001,
                                'cK':0.01,
                                'dK':0.1,
                                'K':1,
                                'daK':10,
                                'hK':100,
                                'kK':1000}
        
        self.units_derived = {'W': ['J/S','N*m/s','kg*m^2/s^3'],
                              'J': ['kg*m^2/s^3'],
                              'N': ['kg*m/s^2'],
                              'Pa':['N/m^2','kg/m*s^2'],
                              'Hz':['1/s'],
                              'Cp':['J/kg*K','m^2/s^2*K'],
                              'k': ['W/m*k','m*kg/s^3*K'],
                              'R': ['1/G','K/W','K*s^3/m^2*kg'],
                              'G': ['1/R','W/K','m^2*kg/K*s^3'],
                              'C': ['J/K','m^2*kg/s^2*K']
                              }
        
        self.metric_conversions = {'m':0.001,
                                'c':0.01,
                                'd':0.1,
                                '1':1,
                                'da':10,
                                'h':100,
                                'k':1000,
                                }
        
        self.SI_units        = {'mass':self.units_mass,
                               'time':self.units_time,
                               'length':self.units_length,
                               'angle':self.units_angle,
                               'temperature':self.units_temp,
                               'derived':self.units_derived,
                               }
                                  
    #%% Dunder Methods
    def __repr__(self) -> str:
        return str(self.value)
    
    def __add__(self,val) -> float:
        try:
            return float(self.value+val)
        except:
            pass
        
        try:
            return float(self.value+val.val())
        except:
            return False

    def __sub__(self,val) -> float:
        try:
            return float(self.value-val)
        except:
            pass
        
        try:
            return float(self.value-val.val())
        except:
            return False
    
    def __mul__(self,val) -> float:
        try:
            return float(self.value*val)
        except:
            pass
        
        try:
            return float(self.value*val.val())
        except:
            return False
    
    def __truediv__(self,val) -> float:
        try:
            return float(self.value/val)
        except:
            pass
        
        try:
            return float(self.value/val.val())
        except:
            return False
        
    def __pow__(self,val) -> float:
        try:
            return float(self.value**val)
        except:
            pass
        
        try:
            return float(self.value**val.val())
        except:
            return False

        
    #%% Normal Methods
    def val(self) -> float:
        '''
        Returns value of the constant.

        Returns
        -------
        float
            Returns value of the constant.

        '''
        return float(self.value)
    
    def get_available_conversions(self,from_unit:str = None):

        if from_unit is None:
            from_unit = self.unit
        
        keys = self.SI_units.keys()
        for key in keys:
            if from_unit in self.SI_units[key].keys():
                print(list(self.SI_units[key].keys()))
    
    #%% Single Unit Methods
    def to_unit(self,value,unit_from,unit_to,unit_conversion_dictionary):
        
        #### Error Check
        if unit_to not in unit_conversion_dictionary: # Check if to unit is in supplied dictionary
            print('End unit not supported')
            return False
        elif unit_from not in unit_conversion_dictionary: # check if from unit is in supplied dictionary
            print('From unit not supported')
            return False
        else:
            pass # If unit existance checks are good, pass and continue onto main function
            
        #### Convert value to new unit    
        new_value   = value*unit_conversion_dictionary[unit_from] / unit_conversion_dictionary[unit_to]
        
        #### Convert uncertainty attribute to new unit if it exists. Only works with attribute
        if self.u is None:
            new_u = False
        else:
            new_u = self.u*unit_conversion_dictionary[unit_from] / unit_conversion_dictionary[unit_to]
        
        return new_value,new_u
        
    def to_temp(self,unit_to:str,
               unit_from:str = None,
               value:str = None,
               units:dict = None,
               **kwargs) -> float:
        
        if unit_from is None:
            unit_from   = self.unit
            
        if value is None:
            value       = self.value 
        
        if unit_from == 'K':
            if unit_to in self.units_temp_K:
                return self.to_unit(value,unit_from,unit_to,self.units_temp_K)
            if unit_to == 'C':
                return value - 273.15
            if unit_to == 'F':
                return ((value-273.15)*(9/5)) + 32
        elif unit_from  == 'C':
            if unit_to in self.units_temp_C:
                return self.to_unit(value,unit_from,unit_to,self.units_temp_C)
            if unit_to == 'K':
                return value + 273.15
            if unit_to == 'F':
                return (value*(9/5)) + 32
        elif unit_from  == 'F':
            if unit_to == 'C':
                return (value-32)*(5/9)
            if unit_to == 'K':
                return (value-32)*(5/9) + 273.15
        else:
            print('problem')
            return False
    
    def convert(self,unit_to:str) -> float:
        '''
        NEED TO ADD UNCERTAINTY CONVERSION
        NEED TO ADD TEMP CONVERSION

        Parameters
        ----------
        unit_to : str
            DESCRIPTION.

        Returns
        -------
        float
            DESCRIPTION.

        '''
        self.value      = self.to(unit_to)
        self.unit       = unit_to
        return self.value
        
    def to(self,unit_to:str,
               unit_from:str = None,
               value:str = None,
               units:dict = None,
               **kwargs) -> float:
        
        #### Check for user inputs        
        if unit_from is None:
            unit_from   = self.unit
            
        if value is None:
            value       = self.value 
            
        if units is not None:
            return self.to_unit(value,unit_from,unit_to,units)

        #### Check which unit type
        if '/' in unit_from or '*' in unit_from or '^' in unit_from or '**' in unit_from:
            return self.to_multi_unit(unit_to)
        
        elif unit_to in self.units_angle.keys():
            return self.to_unit(value,unit_from,unit_to,self.units_angle)
        
        elif unit_to in self.units_length.keys():
            return self.to_unit(value,unit_from,unit_to,self.units_length)
        
        elif unit_to in self.units_mass.keys():
            return self.to_unit(value,unit_from,unit_to,self.units_mass)
        
        elif unit_to in self.units_time.keys():
            return self.to_unit(value,unit_from,unit_to,self.units_time)
        else:
            print('Problem')
            return False
        
    def to_multi_unit(self,unit_to):
            value       = self.value
            unit        = self.unit.replace('(','').replace(')','').replace('**','^')   
            
            num,den     = unit.split('/')
            num_units   = num.split('*')
            den_units   = den.split('*')
            num_unit_list = []
            den_unit_list = []
            for unit in num_units: num_unit_list.append(unit.split('^'))
            for unit in den_units: den_unit_list.append(unit.split('^'))
            
            print(unit)
            
            for sub_list in num_unit_list:
                unit_from = sub_list[0]
                if len(sub_list) == 2:
                    power = float(sub_list[1])
                else:
                    power = 1
                
                if unit_from in self.units_length.keys():
                    
                    factor = self.to_unit(1,unit_from,unit_to,self.units_length)
                    factor = factor**power
                else:
                    factor = 1
                
                value = value*factor
                
            for sub_list in den_unit_list:
                unit_from = sub_list[0]
                if len(sub_list) == 2:
                    power = float(sub_list[1])
                else:
                    power = 1
                
                if unit_from in self.units_length.keys():
                    
                    factor = self.to_unit(1,unit_from,unit_to,self.units_length)
                    factor = factor**power
                else:
                    factor = 1
                    
                value = value/factor
                
            return value


#%% Template
template   = constant(
                    abbrev          = 'template',
                    name            = '',
                    value           = 5.670374419*(10**(-8)),
                    uncertainty     = 0,
                    unit            = '',
                    value_ref       = '',
                    value_ref_link  = '',
                    u_ref           = '',
                    u_ref_link      = ''
                   )

#%% Fundamental Physical Constants
sigma   = constant(abbrev           = 'sigma',
                   name             = 'Stefan-Boltzmann constant',
                   value            = 5.670374419*(10**(-8)),
                   uncertainty      = 0,
                   unit             = 'W/(m^2*K^4)',
                   value_ref        = 'NIST',
                   value_ref_link   = 'https://physics.nist.gov/cgi-bin/cuu/Value?sigma',
                   u_ref            = 'NIST',
                   u_ref_link       = 'https://physics.nist.gov/cgi-bin/cuu/Value?sigma'
                   )

#%% Astronomical Constants
G       = constant(
                    abbrev          = 'G',
                    name            = 'gravitational constant',
                    value           = 6.67428*(10**(-11)),
                    uncertainty     = 6.7*(10**(-15)),
                    unit            = '(m^3)/(kg*s^2)',
                    value_ref       = 'IAU',
                    value_ref_link  = 'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                    u_ref           = 'IAU',
                    u_ref_link      = 'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf'
                   )

c       = constant(
                    abbrev          = 'c',
                    name            = 'speed of light',
                    value           = 299792458.0,
                    uncertainty     = 0,
                    unit            = 'm/s',
                    value_ref       = '',
                    value_ref_link  = '',
                    u_ref           = '',
                    u_ref_link      = ''
                   )

tau_A   = constant(
                    abbrev          = 'tau_A',
                    name            = 'light-time',
                    value           = 499.0047863852,
                    uncertainty     = 4.0*(10**-11),
                    unit            = 's',
                    value_ref       = 'IERS Conventions (2003)',
                    value_ref_link  = 'https://web.archive.org/web/20131219165433/http://www.iers.org/IERS/EN/Publications/TechnicalNotes/tn32.html',
                    u_ref           = 'IERS Conventions (2003)',
                    u_ref_link      = 'https://web.archive.org/web/20131219165433/http://www.iers.org/IERS/EN/Publications/TechnicalNotes/tn32.html'
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

#%% Planetary Values
#%%% Planetary J2 Values
J2_earth    = constant(
                    abbrev          = 'J2_earth',
                    name            = 'J2 constant for Earth',
                    value           = 0.0010826359,
                    uncertainty     = 1*(10**-10),
                    unit            = '',
                    value_ref       = 'IAU',
                    value_ref_link  = 'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                    u_ref           = 'IAU',
                    u_ref_link      = 'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf'
                   )

J2_mars     = constant(
                    abbrev          = 'J2_mars',
                    name            = 'J2 constant for Mars',
                    value           = 0.001964,
                    uncertainty     = None,
                    unit            = '',
                    value_ref       = '',
                    value_ref_link  = 'http://astro.vaporia.com/start/j2.html',
                   )

J2_jupiter  = constant(
                    abbrev          = 'J2_jupiter',
                    name            = 'J2 constant for Jupiter',
                    value           = 0.01475,
                    uncertainty     = None,
                    unit            = '',
                    value_ref       = '',
                    value_ref_link  = 'http://astro.vaporia.com/start/j2.html',
                   )

J2_saturn   = constant(
                    abbrev          = 'J2_saturn',
                    name            = 'J2 constant for Saturn',
                    value           = 0.01656,
                    uncertainty     = None,
                    unit            = '',
                    value_ref       = '',
                    value_ref_link  = 'http://astro.vaporia.com/start/j2.html',
                   )

#%%% Earth System Values
e_J2000 = constant('e_J2000',
                   'Obliquity of the ecliptic at J2000.0',
                   8.4381406*(10**4),
                   1*(10**(-3)),
                   'arcseconds',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

#%%% Planetary Gravitational Parameters
GM_sun  = constant('GM_sun',
                   'Heliocentric graviational constant, TCB-compatible',
                   1.32712442099*(10**20),
                   1*(10**10),
                   'm**3/s**2',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

GM_E    = constant('GM_E',
                   'Geocentric graviational constant, TCB-compatible',
                   3.986004418*(10**14),
                   1*(10**10),
                   'm**3/s**2',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

#%%% Planetary Mass Ratios
Ms_Mme  = constant('Ms_Mme',
                   'Ratio of Sun mass to Mercury mass',
                   6.0236*(10**6),
                   3*(10**2),
                   None,
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

Ms_Mve  = constant('Ms_Mve',
                   'Ratio of Sun mass to Venus mass',
                   4.08523719*(10**5),
                   8*(10**-3),
                   None,
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')


Mm_Me  = constant('Mm_Me',
                   'Ratio of Moon mass to Earth mass',
                   1.23000371*(10**-2),
                   4*(10**-10),
                   None,
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

Ms_Mma  = constant('Ms_Mve',
                   'Ratio of Sun mass to Mars mass',
                   3.09870359*(10**6),
                   2*(10**-2),
                   None,
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

Ms_Mj   = constant('Ms_Mj',
                   'Ratio of Sun mass to Jupiter mass',
                   1.047348644*(10**6),
                   1.7*(10**-5),
                   None,
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

Ms_Msa   = constant('Ms_Msa',
                   'Ratio of Sun mass to Saturn mass',
                   3.4979018*(10**3),
                   1*(10**-4),
                   None,
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

Ms_Mu   = constant('Ms_Mu',
                   'Ratio of Sun mass to Uranus mass',
                   2.290298*(10**4),
                   3*(10**-2),
                   None,
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

Ms_Mn   = constant('Ms_Mn',
                   'Ratio of Sun mass to Neptune mass',
                   1.941226*(10**4),
                   3*(10**-2),
                   None,
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

Ms_Mp   = constant('Ms_Mp',
                   'Ratio of Sun mass to Pluto mass',
                   1.36566*(10**8),
                   2.8*(10**4),
                   None,
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

#%%% Planetary Masses
M_Sun   = constant('M_Sun',
                   'Mass of the sun',
                   (GM_sun/G)[0],
                   (GM_sun/G)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

M_Me    = constant('M_Me',
                   'Mass of Mercury',
                   (M_Sun/Ms_Mme)[0],
                   (M_Sun/Ms_Mme)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   )

M_Ve    = constant('M_Ve',
                   'Mass of Venus',
                   (M_Sun/Ms_Mve)[0],
                   (M_Sun/Ms_Mve)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   )

M_E     = constant('M_E',
                   'Mass of the Earth',
                   (GM_E/G)[0],
                   (GM_E/G)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   )

M_M     = constant('M_M',
                   'Mass of Luna',
                   (Mm_Me*M_E)[0],
                   (Mm_Me*M_E)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   )

M_Ma    = constant('M_Ma',
                   'Mass of Mars',
                   (M_Sun/Ms_Mma)[0],
                   (M_Sun/Ms_Mma)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   )

M_J     = constant('M_J',
                   'Mass of Jupiter',
                   (M_Sun/Ms_Mj)[0],
                   (M_Sun/Ms_Mj)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   )

M_Sa     = constant('M_sa',
                   'Mass of Saturn',
                   (M_Sun/Ms_Msa)[0],
                   (M_Sun/Ms_Msa)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   )

M_U     = constant('M_U',
                   'Mass of Uranus',
                   (M_Sun/Ms_Mu)[0],
                   (M_Sun/Ms_Mu)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   )

M_N     = constant('M_U',
                   'Mass of Neptune',
                   (M_Sun/Ms_Mn)[0],
                   (M_Sun/Ms_Mn)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   )

M_P     = constant('M_U',
                   'Mass of Pluto',
                   (M_Sun/Ms_Mp)[0],
                   (M_Sun/Ms_Mp)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   )

M_charon= constant('M_charon',
                   'Mass of Charon',
                   1.5897*(10**21),
                   0.0045*(10**21),
                   'kg',
                   'Brozović, Marina; Jacobson, Robert A. (May 8, 2024)',
                   'https://doi.org/10.3847%2F1538-3881%2Fad39f0',
                   )

M_Pbc   = constant('M_Pbc',
                   'Mass of Pluto Barycenter',
                   (M_P+M_charon)[0],
                   (M_P+M_charon)[1],
                   'kg',
                   'IAU and Brozović, Marina; Jacobson, Robert A. (May 8, 2024)',
                   )



import numpy as np

class constant():
    def __init__(self,
                 abbrev:str,
                 name:str, 
                 value:float,
                 uncertainty:float=0,
                 unit:str=None,
                 reference:str=None,
                 ref_link:str=None,
                 system:str=None,
                 **args):
    
        #### User Defined Attributes
        self.abbrev         = abbrev
        self.name           = name
        self.value          = value
        self.u              = uncertainty
        self.unit           = unit
        self.reference      = reference
        self.ref_link       = ref_link
        self.system         = system
        
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
        
        self.units_temp_C   = {'mC':0.001,
                                'cC':0.01,
                                'dC':0.1,
                                'C':1,
                                'daC':10,
                                'hC':100,
                                'kC':1000}
        
        self.units_temp_K   = {'mK':0.001,
                                'cK':0.01,
                                'dK':0.1,
                                'K':1,
                                'daK':10,
                                'hK':100,
                                'kK':1000}

        self.derived_units = {'W': ['J/S','(N*m)/s','(kg*m^2)/s^3'],
                              'J': ['(kg*m^2)/s^3']}
                                  
    #%% Dunder Methods
    def __repr__(self) -> str:
        return str(self.value)
    
    def __add__(self,add_val) -> float:
        '''
        Dunder add method.
        
        Parameters
        ----------
        add_val : float
            Dunder method input.

        If dunder input is float, returns self.value + add_val.
        If dunder input is another constant, returns summed value and combined uncertainty
            
        Returns 
        -------
        float: value
        
        OR
        
        float: value
            self.value+add_val
        float: value
            combined uncertainty
            
        '''
        
        try:
            return float(self.value+add_val)
        except:
            add_u       = add_val.u
            
            value       = float(self.value-add_val.val())
            u           = float(np.sqrt(self.u**2 + add_u**2))
            return value,u
    
    def __sub__(self,sub_val) -> float:
        '''
        Dunder subtract method.
        
        Parameters
        ----------
        sub_val : float
            Dunder method input.

        If dunder input is float, returns self.value - sub_val.
        If dunder input is another constant, returns subtracted value and combined uncertainty
            
        Returns 
        -------
        float: value
        
        OR
        
        float: value
            self.value-sub_val
        float: value
            combined uncertainty
            
        '''
        try:
            return float(self.value-sub_val)
        except:
            sub_u       = sub_val.u
            
            value       = float(self.value-sub_val.val())
            u           = float(np.sqrt(self.u**2 + sub_u**2))
            return value,u
    
    def __mul__(self,mul_val) -> float:
        '''
        Dunder multiply method.
        
        Parameters
        ----------
        mul_val : float
            Dunder method input.

        If dunder input is float, returns self.value*mul_val.
        If dunder input is another constant, returns multiplied value and combined uncertainty
            
        Returns 
        -------
        float: value
        
        OR
        
        float: value
            self.value*mul_val
        float: value
            combined uncertainty
            
        '''
        
        try:
            return float(self.value*mul_val)
        except:
            mul_value   = mul_val.val()
            mul_u       = mul_val.u
            value       = float(self.value*mul_value)
            u           = float(value*np.sqrt((self.u/self.value)**2 + (mul_u/mul_value)**2))
            return value,u
    
    def __truediv__(self,div_val) -> float:
        '''
        Dunder divide method.
        
        Parameters
        ----------
        div_val : float
            Dunder method input.

        If dunder input is float, returns self.value/div_val.
        If dunder input is another constant, returns divided value and combined uncertainty
            
        Returns 
        -------
        float: value
        
        OR
        
        float: value
            self.value/div_val
        float: value
            combined uncertainty
            
        '''
        try:
            return float(self.value/div_val)
        except:
            div_value   = div_val.val()
            div_u       = div_val.u
            value       = float(self.value/div_value)
            u           = float(value*np.sqrt((self.u/self.value)**2 + (div_u/div_value)**2))
            return value,u
        
    def __pow__(self,power) -> float:
        '''
        Dunder power method.
        
        Parameters
        ----------
        power : float
            Dunder method input.

        If dunder input is float, returns self.value + add_val.
        If dunder input is another constant, returns powered value and combined uncertainty
            
        Returns 
        -------
        float: value
        
        OR
        
        float: value
            self.value**pow_val
        float: value
            combined uncertainty
            
        '''
        return float(self.value**power)
    
    

        
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
    
    def get_available_conversions(self):
        if self.unit in self.units_angle.keys():
            return print(list(self.units_angle.keys()))
        if self.unit in self.units_length.keys():
            return print(list(self.units_length.keys()))
        if self.unit in self.units_mass.keys():
            return print(list(self.units_mass.keys()))
        if self.unit in self.units_time.keys():
            return print(list(self.units_time.keys()))
        if self.unit in self.units_temp_C.keys():
            return print(list(self.units_temp_C.keys()))
        if self.unit in self.units_temp_K.keys():
            return print(list(self.units_temp_K.keys()))
        if self.unit in self.units_temp_F.keys():
            return print(list(self.units_temp_F.keys()))
    
    #%% Single Unit Methods
    def to_unit(self,value,unit_from,unit_to,unit_conversion_dictionary):
        if unit_to not in unit_conversion_dictionary:
            print('End unit not supported')
            return False
        elif unit_from not in unit_conversion_dictionary:
            print('From unit not in correct system')
            return False
        else:
            pass
        
        new_value = value * unit_conversion_dictionary[unit_from] / unit_conversion_dictionary[unit_to]
        
        
        return new_value
        
    def to_temp(self,unit_out: str) -> float:
        
        value = self.value
        
        if self.unit == 'K':
            if unit_out in self.units_temp_K:
                return self.to_unit(unit_out,self.units_temp_K)
            if unit_out == 'C':
                return value - 273.15
            if unit_out == 'F':
                return ((value-273.15)*(9/5)) + 32
        if self.unit == 'C':
            if unit_out in self.units_temp_C:
                return self.to_unit(unit_out,self.units_temp_C)
            if unit_out == 'K':
                return value + 273.15
            if unit_out == 'F':
                return (value*(9/5)) + 32
        if self.unit == 'F':
            if unit_out == 'C':
                return (value-32)*(5/9)
            if unit_out == 'K':
                return (value-32)*(5/9) + 273.15
    
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
        self.value          = self.to(unit_to)
        self.uncertainty    = 3.15
        self.unit           = unit_to
        
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
                    
                    factor = self._to_unit(1,unit_from,unit_to,self.units_length)
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
                    
                    factor = self._to_unit(1,unit_from,unit_to,self.units_length)
                    factor = factor**power
                else:
                    factor = 1
                    
                value = value/factor
                
            return value

        
#%% Astronomical Constants
G       = constant('G',
                   'gravitational constant',
                   6.67428*(10**(-11)),
                   6.7*(10**(-15)),
                   '(m^3)/(kg*s^2)',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   'SI')

c       = constant('c',
                   'speed of light',
                   299792458.0,
                   0,
                   'm/s',
                   None,
                   None,
                   'SI')

tau_A   = constant('a_e',
                   'Light-time',
                   499.0047863852,
                   4.0*(10**-11),
                   's',
                   'IERS Conventions (2003)',
                   'https://web.archive.org/web/20131219165433/http://www.iers.org/IERS/EN/Publications/TechnicalNotes/tn32.html',
                   'SI')

AU      = constant('AU',
                   'astronomical unit',
                   1.49597870700*(10**11),
                   3,
                   'm',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   'SI')

e_J2000 = constant('e_J2000',
                   'Obliquity of the ecliptic at J2000.0',
                   8.4381406*(10**4),
                   1*(10**(-3)),
                   'arcseconds',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

#%% Planetary Values
#%%% Planetary J2 Values
J2_earth    = constant('J2_earth',
                   'J2 constant for Earth',
                   0.0010826359,
                   1*(10**-10),
                   None,
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

J2_mars     = constant('J2_mars',
                   'J2 constant for Mars',
                   0.001964,
                   0,
                   None,
                   None,
                   'http://astro.vaporia.com/start/j2.html')

J2_jupiter  = constant('J2_jupiter',
                   'J2 constant for Jupiter',
                   0.01475,
                   0,
                   None,
                   None,
                   'http://astro.vaporia.com/start/j2.html')

J2_saturn   = constant('J2_saturn',
                   'J2 constant for Saturn',
                   0.01656,
                   0,
                   None,
                   None,
                   'http://astro.vaporia.com/start/j2.html')

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
                   'SI')


M_Ve    = constant('M_Ve',
                   'Mass of Venus',
                   (M_Sun/Ms_Mve)[0],
                   (M_Sun/Ms_Mve)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   'SI')

M_E     = constant('M_E',
                   'Mass of the Earth',
                   (GM_E/G)[0],
                   (GM_E/G)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   'SI')

M_M     = constant('M_M',
                   'Mass of Luna',
                   (Mm_Me*M_E)[0],
                   (Mm_Me*M_E)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   'SI')

M_Ma    = constant('M_Ma',
                   'Mass of Mars',
                   (M_Sun/Ms_Mma)[0],
                   (M_Sun/Ms_Mma)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   'SI')

M_J     = constant('M_J',
                   'Mass of Jupiter',
                   (M_Sun/Ms_Mj)[0],
                   (M_Sun/Ms_Mj)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   'SI')

M_Sa     = constant('M_sa',
                   'Mass of Saturn',
                   (M_Sun/Ms_Msa)[0],
                   (M_Sun/Ms_Msa)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   'SI')

M_U     = constant('M_U',
                   'Mass of Uranus',
                   (M_Sun/Ms_Mu)[0],
                   (M_Sun/Ms_Mu)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   'SI')

M_N     = constant('M_U',
                   'Mass of Neptune',
                   (M_Sun/Ms_Mn)[0],
                   (M_Sun/Ms_Mn)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   'SI')

M_P     = constant('M_U',
                   'Mass of Pluto',
                   (M_Sun/Ms_Mp)[0],
                   (M_Sun/Ms_Mp)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf',
                   'SI')

M_charon= constant('M_charon',
                   'Mass of Charon',
                   1.5897*(10**21),
                   0.0045*(10**21),
                   'kg',
                   'Brozović, Marina; Jacobson, Robert A. (May 8, 2024)',
                   'https://doi.org/10.3847%2F1538-3881%2Fad39f0',
                   'SI')

M_Pbc   = constant('M_Pbc',
                   'Mass of Pluto Barycenter',
                   (M_P+M_charon)[0],
                   (M_P+M_charon)[1],
                   'kg',
                   'IAU and Brozović, Marina; Jacobson, Robert A. (May 8, 2024)',
                   'SI')



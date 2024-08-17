__all__ = {
    "earthJ2",
    "deg2rad",
    "rad2deg",
    "day2sec",
    "sec2day",
    "G",
    }

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
    
        self.abbrev         = abbrev
        self.name           = name
        self.value          = value
        self.u              = uncertainty
        self.unit           = unit
        self.reference      = reference
        self.ref_link       = ref_link
        self.system         = system

    def __repr__(self):
        return str(self.value)
    
    def __add__(self,add_val):
        try:
            return float(self.value+add_val)
        except:
            add_u       = add_val.u
            
            value       = float(self.value-add_val.val())
            u           = float(np.sqrt(self.u**2 + add_u**2))
            return value,u
    
    def __sub__(self,sub_val):
        try:
            return float(self.value-sub_val)
        except:
            sub_u       = sub_val.u
            
            value       = float(self.value-sub_val.val())
            u           = float(np.sqrt(self.u**2 + sub_u**2))
            return value,u
    
    def __mul__(self,mul_val):
        try:
            return float(self.value*mul_val)
        except:
            mul_value   = mul_val.val()
            mul_u       = mul_val.u
            value       = float(self.value*mul_value)
            u           = float(value*np.sqrt((self.u/self.value)**2 + (mul_u/mul_value)**2))
            return value,u
    
    def __truediv__(self,div_val):
        try:
            return float(self.value/div_val)
        except:
            div_value   = div_val.val()
            div_u       = div_val.u
            value       = float(self.value/div_value)
            u           = float(value*np.sqrt((self.u/self.value)**2 + (div_u/div_value)**2))
            return value,u
    
    def val(self):
        return float(self.value)
        
        
        
#%% Conversion Factors
deg2rad = constant('deg2rad',
                   'Degrees to radians',
                   np.pi/180,
                   0,
                   'rad/deg')

rad2deg = constant('rad2deg','Radians to degrees',
                   180/np.pi,
                   0,
                   'deg/rad')

day2sec = constant('day2sec',
                   'convert days to seconds',
                   24*60*60,
                   0,
                   'sec/day')

sec2day = constant('sec2day',
                   'convert seconds to days',
                   1/(24*60*60),
                   0,
                   'day/sec')

arcsec2deg = constant('arcsec2deg',
                      'convert arcseconds to degrees',
                      1/3600,
                      0)

#%% Astronomical Constants
G       = constant('G',
                   'gravitational constant',
                   6.67428*(10**(-11)),
                   6.7*(10**(-15)),
                   '(m**3)/(kg*s**2)',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

AU      = constant('AU',
                   'astronomical unit',
                   1.49597870700*(10**11),
                   3,
                   'm',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

J2_earth= constant('J2_earth',
                   '',
                   1.0826359*(10**-3),
                   1*(10**-10),
                   None,
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

e_J2000 = constant('e_J2000',
                   'Obliquity of the ecliptic at J2000.0',
                   8.4381406*(10**4),
                   1*(10**(-3)),
                   'arcseconds',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

GM_sun  = constant('GM_sun',
                   'Heliocentric graviational constant, TCB-compatible',
                   1.32712442099*(10**20),
                   1*(10**10),
                   'm**3/s**2'
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

M_sun   = constant('M_sun',
                   'Mass of the sun',
                   (GM_sun/G)[0],
                   (GM_sun/G)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

GM_E    = constant('GM_E',
                   'Geocentric graviational constant, TCB-compatible',
                   3.986004418*(10**14),
                   1*(10**10),
                   'm**3/s**2'
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

M_E     = constant('M_E',
                   'Mass of the Earth',
                   (GM_E/G)[0],
                   (GM_E/G)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')


Mm_Me  = constant('Mm_Me',
                   'Ratio of Moon mass to Earth mass',
                   1.23000371*(10**-2),
                   4*(10**-10),
                   None,
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

M_M     = constant('M_M',
                   'Mass of Luna',
                   (Mm_Me*M_E)[0],
                   (Mm_Me*M_E)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

Ms_Mme  = constant('Ms_Mme',
                   'Ratio of Sun mass to Mercury mass',
                   6.0236*(10**6),
                   3*(10**2),
                   None,
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

M_me    = constant('M_me',
                   'Mass of Mercury',
                   (M_sun/Ms_Mme)[0],
                   (M_sun/Ms_Mme)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')


Ms_Mve  = constant('Ms_Mve',
                   'Ratio of Sun mass to Venus mass',
                   4.08523719*(10**5),
                   8*(10**-3),
                   None,
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

M_ve    = constant('M_ve',
                   'Mass of Venus',
                   (M_sun/Ms_Mve)[0],
                   (M_sun/Ms_Mve)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')


Ms_Mma  = constant('Ms_Mve',
                   'Ratio of Sun mass to Mars mass',
                   3.09870359*(10**6),
                   2*(10**-2),
                   None,
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

M_ma    = constant('M_ma',
                   'Mass of Mars',
                   (M_sun/Ms_Mma)[0],
                   (M_sun/Ms_Mma)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

Ms_Mj   = constant('Ms_Mj',
                   'Ratio of Sun mass to Jupiter mass',
                   1.047348644*(10**6),
                   1.7*(10**-5),
                   None,
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

M_j     = constant('M_j',
                   'Mass of Jupiter',
                   (M_sun/Ms_Mj)[0],
                   (M_sun/Ms_Mj)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

Ms_Msa   = constant('Ms_Msa',
                   'Ratio of Sun mass to Saturn mass',
                   3.4979018*(10**3),
                   1*(10**-4),
                   None,
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

M_Sa     = constant('M_sa',
                   'Mass of Saturn',
                   (M_sun/Ms_Msa)[0],
                   (M_sun/Ms_Msa)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

Ms_Mu   = constant('Ms_Mu',
                   'Ratio of Sun mass to Uranus mass',
                   2.290298*(10**4),
                   3*(10**-2),
                   None,
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

M_U     = constant('M_U',
                   'Mass of Uranus',
                   (M_sun/Ms_Mu)[0],
                   (M_sun/Ms_Mu)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

Ms_Mn   = constant('Ms_Mn',
                   'Ratio of Sun mass to Neptune mass',
                   1.941226*(10**4),
                   3*(10**-2),
                   None,
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

M_N     = constant('M_U',
                   'Mass of Neptune',
                   (M_sun/Ms_Mn)[0],
                   (M_sun/Ms_Mn)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

Ms_Mp   = constant('Ms_Mp',
                   'Ratio of Sun mass to Pluto mass',
                   1.36566*(10**8),
                   2.8*(10**4),
                   None,
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

M_P     = constant('M_U',
                   'Mass of Pluto',
                   (M_sun/Ms_Mp)[0],
                   (M_sun/Ms_Mp)[1],
                   'kg',
                   'IAU',
                   'https://apps.dtic.mil/sti/tr/pdf/ADA551834.pdf')

M_charon= constant('M_charon',
                   'Mass of Charon',
                   1.5897*(10**21),
                   0.0045*(10**21),
                   'kg',
                   'Brozović, Marina; Jacobson, Robert A. (May 8, 2024)',
                   'https://doi.org/10.3847%2F1538-3881%2Fad39f0')

M_Pbc   = constant('M_Pbc',
                   'Mass of Pluto Barycenter',
                   (M_P+M_charon)[0],
                   (M_P+M_charon)[1],
                   'kg',
                   'IAU and Brozović, Marina; Jacobson, Robert A. (May 8, 2024)')



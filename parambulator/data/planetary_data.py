sun     = {
            'name':     'Sun',
            'parent':   'SolarSystemBarycenter',
            'radius':   6378,                  # km
            'u':        398600.432896939,      # km^3/s
            'm':        5972.4E21,             # kg 
    }

earth   = {
            'name':    'Earth',
            'parent':   'Sun',
            'radius':   6378,                  # km
            'u':        398600.432896939,      # km^3/s
            'm':        5972.4E21,             # kg
    }

luna    = {
            'name':     'luna',
            'parent':   'Earth',
    }



from astropy.constants import Constant

R_mean_mars = Constant(
    "R_mean_mars",
    "Mars mean radius",
    3.38950e6,
    "m",
    2000,
    "IAU Working Group on Cartographic Coordinates and Rotational Elements: 2015",
    system="si",
)
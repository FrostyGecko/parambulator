import constants as con

planets = {
    'sun':      {
                'name':     'Sun',
                'parent':   'SolarSystemBarycenter',
                'radius':   6378,                       # km
                'mu':       398600.432896939,           # km^3/s
                'mass':     con.M_sun,                  # kg 
                },
    
    'earth':    {
                'name':     'Earth',
                'parent':   'Sun',
                'radius':   6378,                       # km
                'mu':       398600.432896939,           # km^3/s
                'mass':     con.M_E,                  # kg
                }
            }


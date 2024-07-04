
from satellite_tle import fetch_tle_from_celestrak
import numpy as np


class tle_object():
    from satellite_tle import fetch_tle_from_celestrak
    def __init__(self,norad_id):
        self.norad_id = norad_id
        self.RE     = 6378
        self.mu     = 398600.44189
        self.tle    = self.get_tle(norad_id)
        self.get_keplerian()
        
    def get_tle(self,norad_id):
        self.tle = fetch_tle_from_celestrak(norad_id)

        self.line1 = self.tle[0]
        self.line2 = self.tle[1]
        self.line3 = self.tle[2]

        self.object         = self.line1
        self.line2_items    = list(filter(None, self.line2.split(' ')))
        self.line3_items    = list(filter(None, self.line3.split(' ')))
        
    def print_tle(self):
        print(self.tle)
        
    def get_keplerian(self):
        deg2rad         = np.pi/180
        rad2deg         = 1/deg2rad

        inc             = float(self.line3_items[2])*deg2rad
        RAAN            = float(self.line3_items[3])*deg2rad
        e               = float('.'+self.line3_items[4])
        omega           = float(self.line3_items[5])*deg2rad
        mean_anomaly    = float(self.line3_items[6])*deg2rad
        mean_motion     = float(self.line3_items[7])

        
        n   = mean_motion*(1/86400)*(2*np.pi)
        P   = (2*np.pi)/n
        a   = ((((P/(2*np.pi))**2)*self.mu)**(1/3))

        nu  = 0

        self.kepler_classic  = [a,e,inc*rad2deg,RAAN*rad2deg,nu*rad2deg,omega*rad2deg,nu*rad2deg]
        self.r_a             = a*(1+e)
        self.r_p             = a*(1-e)
        self.alt_a           = self.r_a - self.RE
        self.alt_p           = self.r_p - self.RE
        self.i              = inc*rad2deg
        self.RAAN           = RAAN*rad2deg
        self.e              = e
        self.omega          = omega*rad2deg
        self.mean_anomaly   = mean_anomaly*rad2deg
        self.mean_motion    = mean_motion
        self.period         = P
        self.a              = a
        self.nu             = nu*rad2deg


# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 13:05:57 2024
 
@author: fosterij
"""
#%% Initalize
#### Standard Libraries
import numpy as np

#### Parambulator Libraries
from satellite_tle import fetch_tle_from_celestrak
import parambulator.library.bodies as body
import parambulator.orbit.twobody as twb
import parambulator.utilities.timekeeper as tk

#%% tle
class tle_object():
    def __init__(self,
                 norad_id   = None,
                 Earth_R    = body.planets['earth']['radius'],
                 Earth_mu   = body.planets['earth']['mu']):
        
        self.norad_id   = norad_id
        self.RE         = Earth_R
        self.mu         = Earth_mu
        self.TLE_set    = False
    
    def import_tle(self,filepath):
        
        # self.epoch          = epoch
        # self.INC            = INC
        # self.RAAN           = RAAN
        # self.ECC            = ECC
        # self.AOP            = AOP
        # self.M              = M
        # self.mean_motion    = mean_motion
        
        self.TLE_set        = True
        
    def get_tle(self,norad_id=None):
        if norad_id is None:
            norad_id = self.norad_id
           
        self.tle            = fetch_tle_from_celestrak(norad_id)
 
        self.line1          = self.tle[0]
        self.line2          = self.tle[1]
        self.line3          = self.tle[2]
 
        self.object         = self.line1
        self.line2_items    = list(filter(None, self.line2.split(' ')))
        self.line3_items    = list(filter(None, self.line3.split(' ')))
       
        epoch               = float(self.line2_items[3])
        INC                 = float(self.line3_items[2])
        RAAN                = float(self.line3_items[3])
        ECC                 = float('.'+self.line3_items[4])
        AOP                 = float(self.line3_items[5])
        M                   = float(self.line3_items[6])
        mean_motion         = float(self.line3_items[7])
       
        self.epoch          = epoch
        self.INC            = INC
        self.RAAN           = RAAN
        self.ECC            = ECC
        self.AOP            = AOP
        self.M              = M
        self.mean_motion    = mean_motion
       
        self.TLE_set        = True
        
    def set_tle(self,
                epoch,
                INC,
                RAAN,
                ECC,
                AOP,
                M,
                mean_motion):
       
        self.epoch          = epoch
        self.INC            = INC
        self.RAAN           = RAAN
        self.ECC            = ECC
        self.AOP            = AOP
        self.M              = M
        self.mean_motion    = mean_motion
        self.TLE_set        = True
       
    def convert_tle_to_kep(self):
        if self.TLE_set is False:
            print('No TLE set')
            return False
       
        n                   = self.mean_motion*(1/86400)*(2*np.pi)
        P                   = (2*np.pi)/n
        SMA                 = ((((P/(2*np.pi))**2)*self.mu)**(1/3))
 
        self.period         = P
        self.SMA            = SMA
        self.n              = n
        self.unix_time      = tk.convert_epoch_to_UNIX(self.epoch)
        self.date_utc       = tk.convert_unix_to_datetime_UTC(self.unix_time)
        self.date_local     = tk.convert_unix_to_datetime_local(self.unix_time)
        self.date_modJulian = tk.convert_unix_to_ModJulian_UTC(self.unix_time)
        self.r_a            = self.SMA*(1+self.ECC)
        self.r_p            = self.SMA*(1-self.ECC)
        self.alt_a          = self.r_a - self.RE
        self.alt_p          = self.r_p - self.RE
        self.E              = twb.twb00112_eccentric_anomoly(self.M,self.ECC)
        self.TA             = twb.twb00113_true_anomaly(self.E,self.ECC)
           
    def print_keplerian(self):
        print('--------------------------------------')
        print(f"Date UTC: {self.date_utc}")
        print(f"Date Local: {self.date_local}")
        print(f"UTCModJulian: {self.date_modJulian}")
        print(f"Unix Epoch: {self.unix_time}")
        print('-----------')
        print(f"Epoch: {self.epoch}")
        print(f"SMA: {self.SMA}")  
        print(f"ECC: {self.ECC}")
        print(f"INC: {self.INC}")
        print(f"RAAN: {self.RAAN}")
        print(f"AOP: {self.AOP}")
        print(f"TA: {self.TA}")
        print('--------------------------------------')
       
    def print_modified_keplerian(self):
        print('--------------------------------------')
        print(f"Date UTC: {self.date_utc}")
        print(f"Date Local: {self.date_local}")
        print(f"UTCModJulian: {self.date_modJulian}")
        print(f"Unix Epoch: {self.unix_time}")
        print('-----------')
        print(f"Epoch: {self.epoch}")
        print(f"RadPer: {self.r_p}")  
        print(f"RadApo: {self.r_a}")
        print(f"INC: {self.INC}")
        print(f"RAAN: {self.RAAN}")
        print(f"AOP: {self.AOP}")
        print(f"TA: {self.TA}")
        print('--------------------------------------')

if __name__ == "__main__":
    norad_id = 25544
    iss = tle_object()
    iss.set_tle(
                epoch       = 24256.52757035,
                INC         = 51.6367,
                RAAN        = 242.7229,
                ECC         = 0.0007556,
                AOP         = 344.7811,
                M           = 113.2888,
                mean_motion = 15.48994222472098
                )
   
    iss.convert_tle_to_kep()
    iss.print_keplerian()
    print(tk.convert_datetime_to_UTCModJulian(iss.date_utc))


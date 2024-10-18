# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 13:05:57 2024
 
@author: fosterij
"""
#%% Initalize
#### Standard Libraries
import numpy as np

#### Downloaded Libraries
from satellite_tle import fetch_tle_from_celestrak

#### Parambulator Libraries
import library.bodies as body
import orbit.twobody as twb
import core.clock as clock

#%% tle
class tle_object():
    def __init__(self,
                 norad_id   = None,
                 Earth_R    = body.planets['earth']['radius'],
                 Earth_mu   = body.planets['earth']['mu'],
                 **kwargs
                 ):
        
        self.norad_id   = norad_id
        self.RE         = Earth_R
        self.mu         = Earth_mu
        self.TLE_set    = False
        self.Kep_set    = False
        
    #%% Convert Functions
    def convert_tle_to_kep(self):
        
        #### Test if TLE_set is true or false
        if self.TLE_set is False:
            print('-----tle:convert_tle_to_kep-----')
            print('ERROR: No TLE set')
            return False
       
        #### Set time information
        self.tle_clock      = clock.clock()
        self.tle_clock.set_local_tz('America/Denver')
        self.tle_clock.set_epoch(self.epoch)
        self.date_tai       = self.tle_clock.Time
        self.unix_time      = self.tle_clock.UTCunix
        self.date_utc       = self.tle_clock.datetime_utc
        self.date_local     = self.tle_clock.datetime_local
        self.date_modJulian = self.tle_clock.UTCModJulian
        
        #### Set orbital parameters
        self.n              = self.mean_motion*(1/86400)*(2*np.pi)
        self.P              = (2*np.pi)/self.n
        self.SMA            = ((((self.P/(2*np.pi))**2)*self.mu)**(1/3))
        self.RadApo         = self.SMA*(1+self.ECC)
        self.RadPer         = self.SMA*(1-self.ECC)
        self.alt_a          = self.RadApo - self.RE
        self.alt_p          = self.RadPer - self.RE
        self.E              = twb.twb00112_eccentric_anomoly(self.M,self.ECC)
        self.TA             = twb.twb00113_true_anomaly(self.E,self.ECC)
        
        self.Kep_set        = True
    
    #%% Set Functions
    def set_TLE_from_file(self,filepath):
        
        # self.epoch          = epoch
        # self.INC            = INC
        # self.RAAN           = RAAN
        # self.ECC            = ECC
        # self.AOP            = AOP
        # self.M              = M
        # self.mean_motion    = mean_motion
        
        self.TLE_set        = True
      
    def set_tle_from_celestrak(self,norad_id=None):
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
        
        print(self.tle)
        
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
        
    #%% Get Functions
    def get_keplerian(self):
        self.convert_tle_to_kep()
        kep = {'Epoch':self.epoch,
               'SMA':self.SMA,
               'ECC':self.ECC,
               'INC':self.INC,
               'RAAN':self.RAAN,
               'AOP':self.AOP,
               'TA':self.TA,
               'RadPer':self.RadPer,
               'RadApo':self.RadApo
            }        
        return kep        
    
    #%% Print Functions
    def print_time_summary(self):
        print('--------------------------------------')
        print(f"Date TAI: {self.date_tai}")
        print(f"Date UTC: {self.date_utc}")
        print(f"Date Local: {self.date_local}")
        print(f"UTCModJulian: {self.date_modJulian}")
        print(f"Unix Epoch: {self.unix_time}")
        print(f"Epoch: {self.epoch}")
        print('-----------')
        
    def print_keplerian(self):
        self.print_time_summary()
        print(f"Epoch: {self.epoch}")
        print(f"SMA: {self.SMA}")  
        print(f"ECC: {self.ECC}")
        print(f"INC: {self.INC}")
        print(f"RAAN: {self.RAAN}")
        print(f"AOP: {self.AOP}")
        print(f"TA: {self.TA}")
        print('--------------------------------------')
       
    def print_modified_keplerian(self):
        self.print_time_summary()
        print(f"Epoch: {self.epoch}")
        print(f"RadPer: {self.RadPer}")  
        print(f"RadApo: {self.RadApo}")
        print(f"INC: {self.INC}")
        print(f"RAAN: {self.RAAN}")
        print(f"AOP: {self.AOP}")
        print(f"TA: {self.TA}")
        print('--------------------------------------')
        
    def print_tle(self):
        print('--------------------------------------')
        print(f"epoch: {self.epoch}")
        print(f"INC: {self.INC}")
        print(f"RAAN: {self.RAAN}")
        print(f"ECC: {self.ECC}")
        print(f"AOP: {self.AOP}")
        print(f"M: {self.M}")
        print(f"mean_motion: {self.mean_motion}")
        print('--------------------------------------')

if __name__ == "__main__":
    norad_id = 25544
    iss = tle_object()
    # iss.set_tle(
    #             epoch       = 24256.52757035,
    #             INC         = 51.6367,
    #             RAAN        = 242.7229,
    #             ECC         = 0.0007556,
    #             AOP         = 344.7811,
    #             M           = 113.2888,
    #             mean_motion = 15.48994222472098
    #             )
   
    iss.set_tle_from_celestrak(norad_id)
    iss.convert_tle_to_kep()
    iss.print_keplerian()


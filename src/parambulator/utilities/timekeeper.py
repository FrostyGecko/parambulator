# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 18:58:04 2024

@author: isaacfoster
"""
#%% Initialize
#### Standard Libraries
import datetime
import time
from astropy.time import Time

#### Parambulator Libraries
import utilities.defaults as default

#%% timekeeper
def convert_epoch_to_UNIX(epoch:float):
          
    # get year 2 digit and floating seconds days
    y_d, nbs = str(epoch).split('.')
    
    # parse to datetime (since midnight and add the seconds) %j Day of the year as a zero-padded decimal number.
    d = datetime.datetime.strptime(y_d, "%y%j") + datetime.timedelta(seconds=float("." + nbs) * 24 * 60 * 60)
    # 1.0 => 1 day
    # from time tuple get epoch time.
    unix_timestamp = time.mktime(d.timetuple())
   
    return unix_timestamp
   
def convert_unix_to_datetime_UTC(unix_time):
    return time.strftime(default.GMAT_date_format, time.gmtime(unix_time))
   
def convert_unix_to_datetime_local(unix_time):
    return datetime.datetime.fromtimestamp(unix_time).strftime("%d %b %Y %H:%M:%S")
   
def convert_unix_to_ModJulian_UTC(unix_time):
    return (unix_time/86400 + 2440587.5)-2400000.5

def convert_unix_to_Julian_UTC(unix_time):
    return (unix_time/86400 + 2440587.5)
   
def convert_datetime_to_UTCModJulian(date):
    date = datetime.datetime.strptime(date, default.GMAT_date_format).strftime('%Y-%m-%dT%H:%M:%S')
    t = Time(date, format='isot')
    return t.mjd
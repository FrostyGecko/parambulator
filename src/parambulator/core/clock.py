# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 18:58:04 2024

@author: isaacfoster
"""
#%% Initialize
#### Standard Libraries
from datetime import datetime
from zoneinfo import ZoneInfo
import time
import copy
from astropy.time import Time, TimeDelta

#### Parambulator Libraries
import parambulator.core.defaults as default

#%% timekeeper
def convert_epoch_to_UNIX(epoch:float):
          
    # get year 2 digit and floating seconds days
    y_d, nbs = str(epoch).split('.')
    
    # parse to datetime (since midnight and add the seconds) %j Day of the year as a zero-padded decimal number.
    d = datetime.strptime(y_d, "%y%j") + datetime.timedelta(seconds=float("." + nbs) * 24 * 60 * 60)
    # 1.0 => 1 day
    # from time tuple get epoch time.
    unix_timestamp = time.mktime(d.timetuple())
   
    return unix_timestamp
   
def convert_unix_to_datetime_UTC(unix_time):
    return time.strftime(default.GMAT_date_format, time.gmtime(unix_time))
   
def convert_datetime_to_UTCModJulian(date):
    date = datetime.strptime(date, default.GMAT_date_format).strftime('%Y-%m-%dT%H:%M:%S')
    t = Time(date, format='isot')
    return t.mjd


class clock():
    def __init__(self,
                 year:int=None,
                 month:int=None,
                 day:int=None,
                 hour:int=None,
                 minute:int=None,
                 second:int=None,
                 microsecond:int=None,
                 format = 'datetime',
                 scale='tai',
                 local_tz='UTC',
                 **kargs):
        
        
        if year         is None: year           = 1970
        if month        is None: month          = 1
        if day          is None: day            = 1
        if hour         is None: hour           = 0
        if minute       is None: minute         = 0
        if second       is None: second         = 0
        if microsecond  is None: microsecond    = 0
        
        self.SCALES                 = copy.deepcopy(Time.SCALES)
        self.FORMATS                = copy.deepcopy(Time.FORMATS)
        self.local_tz               = local_tz
        
        #### Set Time
        input_datetime          = datetime(year,
                                           month,
                                           day,
                                           hour,
                                           minute,
                                           second,
                                           microsecond,
                                           tzinfo=ZoneInfo(self.local_tz))
        
        utc_datetime            = input_datetime.astimezone(ZoneInfo('UTC'))
        
        self.Time               = Time(utc_datetime,format='datetime',scale=scale)
        self.StartTime          = Time(utc_datetime,format='datetime',scale=scale)
        self.timestamp          = 0
        
        #### Set Local Parameters
        self.local_DST_status   = self.get_local_DST_status()
        self.local_timezone     = self.get_local_timezone()
            
    #%% Dunder Methods
    
    def __repr__(self):
        return str(self.Time.datetime.replace(tzinfo=ZoneInfo('UTC')))
    
    def __iadd__(self,value):
        self.timestamp = self.timestamp + value
        self.Time = self.Time + TimeDelta(value,format='sec')
        return self
    
    def __add__(self,add):
        return self.Time 
    
    def __sub__(self,sub):
        return self.Time

    #%% Property Functions
    #### Datetime Representations
    @property
    def LocalDatetime(self):
        newdatetime = self.Time.datetime.replace(tzinfo=ZoneInfo('UTC'))
        return newdatetime.astimezone(ZoneInfo(self.local_tz))
    @property
    def UTCdatetime(self):
        return self.Time.datetime.replace(tzinfo=ZoneInfo('UTC'))
    
    #### Astronomical Representations
    @property
    def UTCModJulianGMAT(self):
        jd = self.Time.jd
        mjd = jd - 2430000.0
        return float(mjd)
    
    @property
    def UTCModJulian(self):
        return float(self.Time.mjd)
    
    @property
    def UTCJulian(self):
        return float(self.Time.jd)
    
    @property
    def UTCunix(self):
        return float(self.Time.unix)
    
    #%% Primary Functions
    def add(self,add,format):
        return self.Time + TimeDelta(add,format=format)
    
    def sub(self,sub,format):
        return self.Time - TimeDelta(sub,format=format)
    
    def increment(self,value,format):
        self.Time = self.Time + TimeDelta(value,format=format)
        return str(self.Time.datetime.replace(tzinfo=ZoneInfo('UTC')))

    #%% Supporting Functions
    def TZDatetime(self,timezone:str):
        return self.Time.datetime.replace(tzinfo=ZoneInfo('UTC')).astimezone(ZoneInfo(timezone))
        
    def UTC_offset(self,dt):
        seconds = dt.utcoffset().seconds
        days    = dt.utcoffset().days
        
        return days*24*3600 + seconds
        
    def local_utc_offset(self):
        offset_sec  = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
        offset_min  = offset_sec/60
        offset_hour = offset_min/60
        
        return offset_hour
        
    def get_local_timezone(self):
        now = datetime.now()
        local_now = now.astimezone()
        local_tz = local_now.tzinfo
        local_tzname = local_tz.tzname(local_now)
        return local_tzname
    
    def get_local_DST_status(self):
        if time.localtime().tm_isdst == 1:
            return True
        else:
            return False

t1 = clock(2000,1,1,0,0,0,local_tz='UTC',scale='tai',format='datetime')


print(t1.UTCdatetime)
print(t1.Time.utc)
print(t1.UTCunix)



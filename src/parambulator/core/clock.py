# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 18:58:04 2024

@author: isaacfoster
"""
#%% Initialize
#### Standard Libraries
import datetime as dt
import zoneinfo
import time
import copy
from astropy.time import Time, TimeDelta


#%% Clock
class clock():
    def __init__(self,
                 year:int           = None,
                 month:int          = None,
                 day:int            = None,
                 hour:int           = None,
                 minute:int         = None,
                 second:int         = None,
                 microsecond:int    = None,
                 tz                 ='UTC',
                 local_tz           ='UTC',
                 **kargs):
        
        self.SCALES             = copy.deepcopy(Time.SCALES)
        self.FORMATS            = copy.deepcopy(Time.FORMATS)
        self.localDSTstatus     = self.get_local_DST_status()
        self.tz                 = tz
        self.local_tz           = local_tz
        
        self.set_datetime(
                     year=year,
                     month=month,
                     day=day,
                     hour=hour,
                     minute=minute,
                     second=second,
                     microsecond=microsecond,
                     tz=tz)
            
        self.timestamp          = 0
        
        # Site for testing: https://currentmillis.com/?1729242633280&seconds
        # site for tai conversion: https://astroconverter.com/clocks.html
        
        
    #%% Dunder Methods
    def __repr__(self):
        return str(self.Time.datetime)
    
    def __iadd__(self,value):
        self.Time       = self.Time + TimeDelta(value,format='sec')
        return self
    
    def __add__(self,value):
        return self.Time + TimeDelta(value,format='sec')
    
    def __sub__(self,value):
        return self.Time - TimeDelta(value,format='sec')

    #%% Property Functions
    #### Datetime Representations
    @property
    def datetime_local(self):
        return self.Time.utc.datetime.replace(tzinfo=zoneinfo.ZoneInfo('UTC')).astimezone(zoneinfo.ZoneInfo(self.local_tz))
    
    @property
    def datetime_utc(self):
        return self.Time.utc.datetime.replace(tzinfo=zoneinfo.ZoneInfo('UTC'))
    
    @property
    def datetime_tai(self):
        return self.Time.datetime
    
    #### Astronomical Representations
    @property
    def UTCModJulianGMAT(self):
        jd = self.Time.utc.jd
        mjd = jd - 2430000.0
        return float(mjd)
    
    @property
    def UTCModJulian(self):
        return float(self.Time.utc.mjd)
    
    @property
    def UTCJulian(self):
        return float(self.Time.utc.jd)
    
    @property
    def UTCunix(self):
        return float(self.Time.utc.unix)
    
    #### Other Representations
    @property
    def now(self):
        return dt.datetime.now()
    
    
    #%% Get Time Functions
    def get_datetime_tai(self,timezone:str=None):
        if timezone is None:
            timezone = self.tz
        return self.Time.datetime.replace(tzinfo=zoneinfo.ZoneInfo('UTC')).astimezone(zoneinfo.ZoneInfo(timezone))
    
    def get_datetime_utc(self,timezone:str=None):
        if timezone is None:
            timezone = self.tz
        return self.Time.utc.datetime.replace(tzinfo=zoneinfo.ZoneInfo('UTC')).astimezone(zoneinfo.ZoneInfo(timezone))
    
    #%% Primary Functions
    def add(self,add,add_format='sec'):
        return self.Time + TimeDelta(add,format=add_format)
    
    def sub(self,sub,sub_format='sec'):
        return self.Time - TimeDelta(sub,format=sub_format)
    
    def increment(self,value,increment_format='sec'):
        self.Time = self.Time + TimeDelta(value,format=increment_format)
 
    #%% Set Functions
    def set_local_tz(self,local_tz:str):
        self.local_tz = local_tz
    
    def set_datetime(self,
                 year:int           = None,
                 month:int          = None,
                 day:int            = None,
                 hour:int           = None,
                 minute:int         = None,
                 second:int         = None,
                 microsecond:int    = None,
                 tz                 = 'UTC',
                 **kargs):
        
        #### Set Defaults
        if year         is None: year           = 1970
        if month        is None: month          = 1
        if day          is None: day            = 1
        if hour         is None: hour           = 0
        if minute       is None: minute         = 0
        if second       is None: second         = 0
        if microsecond  is None: microsecond    = 0
        
        self.tz                 = tz
        
        #### Set Time
        self.input_datetime     = dt.datetime(year,
                                           month,
                                           day,
                                           hour,
                                           minute,
                                           second,
                                           microsecond,
                                           tzinfo=zoneinfo.ZoneInfo(self.tz))
        
        self.input_utc_datetime = self.input_datetime.astimezone(zoneinfo.ZoneInfo('utc'))
        self.Time               = Time(self.input_utc_datetime,format='datetime',scale='utc').tai
        
    def set_epoch(self,epoch:float):
        date = self.convert_epoch_to_datetime(epoch)
        self.set_datetime(
                     year=date.year,
                     month=date.month,
                     day=date.day,
                     hour=date.hour,
                     minute=date.minute,
                     second=date.second,
                     microsecond=date.microsecond,
                     tz=self.tz)
    
    #%% Convert Functions
    def convert_epoch_to_datetime(self,epoch:float):
        # get year 2 digit and floating seconds days
        y_d, nbs = str(epoch).split('.')
        
        # parse to datetime (since midnight and add the seconds) %j Day of the year as a zero-padded decimal number.
        d = dt.datetime.strptime(y_d, "%y%j") + dt.timedelta(seconds=float("." + nbs) * 24 * 60 * 60)
        return d
    
    #%% Get Functions
    def get_formats(self):
        return self.FORMATS
    
    def get_scales(self):
        return self.SCALES
    
    def get_timezones(self):
        self.tz_names = sorted(list(zoneinfo.available_timezones()))
        return self.tz_names
    
    def get_local_timezone(self):
        now             = dt.datetime.now()
        local_now       = now.astimezone()
        local_tz        = local_now.tzinfo
        local_tzname    = local_tz.tzname(local_now)
        return local_tzname
    
    def get_local_DST_status(self):
        if time.localtime().tm_isdst == 1:
            return True
        else:
            return False

    def get_UTC_offset(self,dt):
        seconds = dt.utcoffset().seconds
        days    = dt.utcoffset().days
        
        return days*24*3600 + seconds
        
    def get_local_utc_offset(self):
        offset_sec  = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
        offset_min  = offset_sec/60
        offset_hour = offset_min/60
        
        return offset_hour
    
if __name__ == "__main__":
    epoch = 24292.38232888
    t1 = clock()
    t1.set_local_tz('America/Denver')
    t1.set_epoch(epoch)
    
    print(f"Tai:   {t1.Time}")
    print(f"UTC:   {t1.datetime_utc}")
    print(f"Local: {t1.datetime_local}")
    print(f"Unix:  {t1.UTCunix}")
    print(f"JD:    {t1.UTCJulian}")
    print(f"MJD:   {t1.UTCModJulian}")
    print(f"GMJD:  {t1.UTCModJulianGMAT}")
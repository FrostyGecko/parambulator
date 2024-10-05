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

def convert_epoch_to_UNIX(epoch:float):
          
    # get year 2 digit and floating seconds days
    y_d, nbs = str(epoch).split('.')
    
    # parse to datetime (since midnight and add the seconds) %j Day of the year as a zero-padded decimal number.
    d = dt.datetime.strptime(y_d, "%y%j") + dt.timedelta(seconds=float("." + nbs) * 24 * 60 * 60)
    # 1.0 => 1 day
    # from time tuple get epoch time.
    unix_timestamp = time.mktime(d.timetuple())
   
    return unix_timestamp
   
def convert_unix_to_datetime_UTC(unix_time):
    return time.strftime(default.GMAT_date_format, time.gmtime(unix_time))
   
# def convert_datetime_to_UTCModJulian(date):
#     date = datetime.strptime(date, default.GMAT_date_format).strftime('%Y-%m-%dT%H:%M:%S')
#     t = Time(date, format='isot')
#     return t.mjd

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
        
        #### Set Attributes
        self.SCALES             = copy.deepcopy(Time.SCALES)
        self.FORMATS            = copy.deepcopy(Time.FORMATS)
        self.tz                 = tz
        self.localDSTstatus     = self.get_local_DST_status()
        
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
        self.timestamp          = 0
            
    #%% Dunder Methods
    def __repr__(self):
        return str(self.Time.datetime.replace(tzinfo=zoneinfo.ZoneInfo('UTC')))
    
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
    def LocalDatetime(self):
        newdatetime = self.Time.datetime.replace(tzinfo=zoneinfo.ZoneInfo('UTC'))
        return newdatetime.astimezone(zoneinfo.ZoneInfo(self.local_tz))
    @property
    def UTCdatetime(self):
        return self.Time.utc.datetime
    
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
    def add(self,add,add_format='sec'):
        return self.Time + TimeDelta(add,format=add_format)
    
    def sub(self,sub,sub_format='sec'):
        return self.Time - TimeDelta(sub,format=sub_format)
    
    def increment(self,value,increment_format='sec'):
        self.Time = self.Time + TimeDelta(value,format=increment_format)
        # str(self.Time.datetime.replace(tzinfo=ZoneInfo('UTC')))

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
        
    #%% Supporting Functions
    def TZDatetime(self,timezone:str):
        return self.Time.datetime.replace(tzinfo=zoneinfo.ZoneInfo('UTC')).astimezone(zoneinfo.ZoneInfo(timezone))
        
    def UTC_offset(self,dt):
        seconds = dt.utcoffset().seconds
        days    = dt.utcoffset().days
        
        return days*24*3600 + seconds
        
    def local_utc_offset(self):
        offset_sec  = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
        offset_min  = offset_sec/60
        offset_hour = offset_min/60
        
        return offset_hour
        


t1 = clock(2024,10,1,0,0,0,scale='utc',tz='America/Denver')


print(t1.Time)
print(t1.UTCdatetime)
print(t1.UTCunix)


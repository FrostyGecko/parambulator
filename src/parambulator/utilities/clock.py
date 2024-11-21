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
                 timezone           = 'UTC',
                 **kargs):
        
        self.SCALES             = copy.deepcopy(Time.SCALES)
        self.FORMATS            = copy.deepcopy(Time.FORMATS)
        self.localDSTstatus     = self.get_local_DST_status()
        self.timezone           = timezone
        
        # self.SetDatetime(
        #              year=year,
        #              month=month,
        #              day=day,
        #              hour=hour,
        #              minute=minute,
        #              second=second,
        #              microsecond=microsecond,
        #              timezone=timezone)
        
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
    def DatetimeLocal(self):
        return self.DatetimeTZ(self.timezone)
    
    @property
    def DatetimeUTC(self):
        return self.Time.utc.datetime.replace(tzinfo=zoneinfo.ZoneInfo('UTC'))
    
    @property
    def DatetimeTAI(self):
        return self.Time.datetime
    
    @property
    def DatetimeTAI_gmat(self):
        return self.Time.datetime.strftime("%d %b %Y %H:%M:%S.%f")
    
    @property
    def DatetimeUTC_gmat(self):
        return self.Time.utc.datetime.strftime("%d %b %Y %H:%M:%S.%f")
    
    @property
    def DatetimeUTC_ISO8601(self):
        return self.Time.utc.datetime.strftime("%Y-%M-%dT%H:%M:%SZ")    
    
    #### Astronomical Representations
    @property
    def UTCModJulianGMAT(self):
        jd = self.Time.utc.jd
        mjd = jd - 2430000.0
        return float(mjd)
    
    @property
    def UTCEpochJ2000(self):
        return self.ConvertDatetimeToEpoch(self.Time.utc.datetime.replace(tzinfo=zoneinfo.ZoneInfo('UTC')))
        
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
    
    #%% Primary Functions
    def add(self,add,add_format='sec'):
        return self.Time + TimeDelta(add,format=add_format)
    
    def sub(self,sub,sub_format='sec'):
        return self.Time - TimeDelta(sub,format=sub_format)
    
    def increment(self,value,increment_format='sec'):
        self.Time = self.Time + TimeDelta(value,format=increment_format)
 
    def DatetimeTZ(self,timezone):
        return self.Time.utc.datetime.replace(tzinfo=zoneinfo.ZoneInfo('UTC')).astimezone(zoneinfo.ZoneInfo(timezone))
        
    #%% Set Functions
    def SetTimezone(self,timezone:str):
        self.timezone = timezone
    
    def SetDatetime(self,
                 year:int           = None,
                 month:int          = None,
                 day:int            = None,
                 hour:int           = None,
                 minute:int         = None,
                 second:int         = None,
                 microsecond:int    = None,
                 timezone           = 'UTC',
                 **kargs):
        
        #### Set Defaults
        if year         is None: year           = 1970
        if month        is None: month          = 1
        if day          is None: day            = 1
        if hour         is None: hour           = 0
        if minute       is None: minute         = 0
        if second       is None: second         = 0
        if microsecond  is None: microsecond    = 0
        
        #### Set Time
        self.input_datetime     = dt.datetime(year,
                                           month,
                                           day,
                                           hour,
                                           minute,
                                           second,
                                           microsecond,
                                           tzinfo=zoneinfo.ZoneInfo(timezone))
        
        self.input_utc_datetime = self.input_datetime.astimezone(zoneinfo.ZoneInfo('utc'))
        self.Time               = Time(self.input_utc_datetime,format='datetime',scale='utc').tai
        
    def SetEpoch(self,epoch:float):
        date = self.ConvertEpochToDatetime(epoch)
        self.SetDatetime(
                     year=date.year,
                     month=date.month,
                     day=date.day,
                     hour=date.hour,
                     minute=date.minute,
                     second=date.second,
                     microsecond=date.microsecond,
                     timezone='utc')
        
    def SetUnix(self,unix):
        date = self.ConvertUnixToDatetime(unix)
        self.SetDatetime(
                     year=date.year,
                     month=date.month,
                     day=date.day,
                     hour=date.hour,
                     minute=date.minute,
                     second=date.second,
                     microsecond=date.microsecond,
                     timezone='utc')
    
    #%% Convert Functions
    def ConvertEpochToDatetime(self,epoch:float):
        # get year 2 digit and floating seconds days
        y_d, nbs = str(epoch).split('.')
        
        # parse to datetime (since midnight and add the seconds) %j Day of the year as a zero-padded decimal number.
        date = dt.datetime.strptime(y_d, "%y%j") + dt.timedelta(seconds=float("." + nbs) * 24 * 60 * 60)
        return date
    
    def ConvertDatetimeToEpoch(self, date) -> float:
        # Extract the year and convert it to a two-digit format
        year = date.year % 100  # Get the last two digits of the year
        
        # Compute the day of the year
        day_of_year = date.timetuple().tm_yday
        
        # Calculate the fractional part of the day
        seconds_since_midnight = date.hour * 3600 + date.minute * 60 + date.second + date.microsecond / 1e6
        fractional_day = seconds_since_midnight / (24 * 3600)
        
        # Combine the components into the epoch format: YYDDD.FFFFFFFF
        epoch = float(f"{year:02d}{day_of_year:03d}") + fractional_day
        return epoch

    def ConvertUnixToDatetime(self,unix:float or int):
        date = dt.datetime.fromtimestamp(unix,dt.timezone.utc)
        return date
    
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
    
    t1 = clock()
    t1.SetTimezone('America/Denver')
    t1.SetDatetime(year=2024,month=10,day=17,hour=18,minute=0,second=0,timezone='America/Denver')
    print('----------- using SetDatetime -----------')
    print(f"TAI:   {t1.Time}")
    print(f"UTC:   {t1.DatetimeUTC}")
    print(f"Local: {t1.DatetimeLocal}")
    print(f"Epoch: {t1.UTCEpochJ2000}")
    print(f"Unix:  {t1.UTCunix}")
    print(f"JD:    {t1.UTCJulian}")
    print(f"MJD:   {t1.UTCModJulian}")
    print(f"GMJD:  {t1.UTCModJulianGMAT}")
    print('----------- End using SetDatetime -----------')

    t2 = clock()
    t2.SetTimezone('America/Denver')
    t2.SetEpoch(24292.0)
    print('----------- using SetEpoch -----------')
    print(f"TAI:   {t2.Time}")
    print(f"UTC:   {t2.DatetimeUTC}")
    print(f"Local: {t2.DatetimeLocal}")
    print(f"Epoch: {t2.UTCEpochJ2000}")
    print(f"Unix:  {t2.UTCunix}")
    print(f"JD:    {t2.UTCJulian}")
    print(f"MJD:   {t2.UTCModJulian}")
    print(f"GMJD:  {t2.UTCModJulianGMAT}")
    print('----------- End using SetEpoch -----------')

    t3 = clock()
    t3.SetTimezone('America/Denver')
    t3.SetUnix(1729209600.0)
    print('----------- using SetDatetime -----------')
    print(f"TAI:   {t3.Time}")
    print(f"UTC:   {t3.DatetimeUTC}")
    print(f"Local: {t3.DatetimeLocal}")
    print(f"Epoch: {t3.UTCEpochJ2000}")
    print(f"Unix:  {t3.UTCunix}")
    print(f"JD:    {t3.UTCJulian}")
    print(f"MJD:   {t3.UTCModJulian}")
    print(f"GMJD:  {t3.UTCModJulianGMAT}")
    print('----------- End using SetDatetime -----------')
from enum import Enum, IntEnum


class TempUnit(Enum):
    C = 'C'  # Celsius
    F = 'F'  # Fahrenheit


# end class

class RainFlag(Enum):
    DRY = '0'
    LAST_MINUTE = '1'
    RAINING = '2'


# end class

class WetFlag(Enum):
    DRY = '0'
    LAST_MINUTE = '1'
    WET = '2'


# end class

class VelocityUnit(Enum):
    K = 'K'  # Km/hr
    M = 'M'  # Miles/hr


# end case

class WindSpeedErrorCode(Enum):
    C = "-1"  # TODO


# end class

class CloudCondition(Enum):
    Unknown = '0'
    Clear = '1'
    Cloudy = '2'
    VeryCloudy = '3'


# end class

class WindCondition(Enum):
    Unknown = '0'
    Calm = '1'
    Windy = '2'
    VeryWindy = '3'


# end class

class RainCondition(Enum):
    Unknown = '0'
    Dry = '1'
    Wet = '2'  # sensor has water on it
    Rain = '3'  # falling rain drops detected


# end class

class DayCondition(Enum):
    Unknown = '0'
    # Below are based upon thresholds set in the setup window.
    Dark = '1'
    Light = '2'
    VeryLight = '3'


# end class

class DomeClose(Enum):
    NotRequested = '0'
    Requested = '1'


class WeatherData:
    def __init__(self):
        self.date = ""
        self.time = ""
        self.tempUnit = TempUnit.C
        self.velocityUnits = VelocityUnit.K
        self.skyAmbientTemp = 0
        self.ambientTemp = 0
        self.sensorCaseTemp = 0
        self.windSpeed = 0
        self.relativeHumPercent = 0
        self.dewPointPercent = 0
        self.heaterTemp = 0
        self.rainFlag = RainFlag.RAINING
        self.wetFlag = WetFlag.WET
        self.sinceLastReadingSeconds = 0
        self.lastFileWrite = ""
        self.cloudCondition = CloudCondition.Unknown
        self.windCondition = WindCondition.Unknown
        self.rainCondition = RainCondition.Unknown
        self.dayCondition = DayCondition.Unknown
        self.domeCloseRequested = True
        self.alert = True

    def __str__(self):
        return "date: " + self.date + " time:" + self.time + " tempUnit:" + self.tempUnit.name

# end class

# 17.1.1 New Format
# This recommended format gives access to all of the data Cloud Sensor II can provide. The data is similar
# to the display fields in the Clarity II window. The format has been split across two lines to make it fit on
# this page:
# Date Time T V SkyT AmbT SenT Wind Hum DewPt Hea
# 2005-06-03 02:07:23.34 C K -28.5 18.7 22.5 45.3 75 10.3 3
# R W Since Now() Day's c w r d C A
# 0 0 00004 038506.08846 1 2 1 0 0 0
# The header line is here just for illustration. It does not actually appear anywhere.
# The fields mean:
#  Heading Col’s Meaning
#  Date 1-10 local date yyyy-mm-dd
#  Time 12-22 local time hh:mm:ss.ss (24 hour clock)
#  T 24 temperature units displayed and in this data, 'C' for Celsius or 'F' for Fahrenheit
#  V 26 wind velocity units displayed and in this data, ‘K’ for km/hr or ‘M’ for mph or
# 'm' for m/s
#  SkyT 28-33 sky-ambient temperature, 999. for saturated hot, -999. for saturated cold, or –998.
# for wet
#  AmbT 35-40 ambient temperature
#  SenT 41-47 sensor case temperature, 999. for saturated hot, -999. for saturated cold. Neither
# saturated condition should ever occur.
#  Wind 49-54 wind speed or:
# -1. if still heating up,
# -2. if wet,
# -3. if the A/D from the wind probe is bad (firmware <V56 only) ,
# -4. if the probe is not heating (a failure condition),
# -5. if the A/D from the wind probe is low (shorted, a failure condition) (firmware
# >=V56 only),
# -6. if the A/D from the wind probe is high (no probe plugged in or a failure)
# (firmware >=V56 only).
#  Hum 56-58 relative humidity in %
#  DewPt 60-65 dew point temperature
#  Hea 67-69 heater setting in %
#  R 71 rain flag, =0 for dry, =1 for rain in the last minute, =2 for rain right now
#  W 73 wet flag, =0 for dry, =1 for wet in the last minute, =2 for wet right now
#  Since 75-79 seconds since the last valid data
#  Now() Day's 81-92 date/time given as the VB6 Now() function result (in days) when Clarity II last
# wrote this file
#  c 94 cloud condition (see the Cloudcond enum in section 20)
# Cloud Sensor II User’s Manual
#  V0029 46
#  w 96 wind condition (see the Windcond enum in section 20)
#  r 98 rain condition (see the Raincond enum in section 20)
#  d 100 daylight condition (see the Daycond enum in section 20)
#  C 102 roof close, =0 not requested, =1 if roof close was requested on this cycle
#  A 104 alert, =0 when not alerting, =1 when alerting

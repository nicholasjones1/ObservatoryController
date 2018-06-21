import configparser

import ephem
import datetime

class Sun:
    def __init__(self, configPath):
        self.configPath = configPath
        self.config = configparser.ConfigParser()
        self.config.read(configPath)
        self.longitude = self.config['observatory']['longitude']
        self.latitude = self.config['observatory']['latitude']
        self.sun = ephem.Sun()
        self.observer = ephem.Observer()
        self.observer.elevation = 537
        self.observer.horizon = '-18'
        self.observer.pressure = 0
        self.observer.lat = self.latitude
        self.observer.lon = self.longitude
        self.delayDarknessStart = self.config['sun']['delayDarknessStart']
        self.advanceDarknessEnd = self.config['sun']['advanceDarknessEnd']



    def isDay(self, dateTime):
         return (self.isNight(dateTime) == False)

    def isNight(self, dateTime):
        self.dateTime = dateTime
        self.observer.date = dateTime

        night = False

        previous_rising = ephem.localtime(self.observer.previous_rising(ephem.Sun(), use_center=True))
        next_rising = ephem.localtime(self.observer.next_rising(ephem.Sun(), use_center=True))

        previous_setting = ephem.localtime(self.observer.previous_setting(ephem.Sun(), use_center=True))
        next_setting = ephem.localtime(self.observer.next_setting(ephem.Sun(), use_center=True))

        if ( dateTime.hour < 12):
            if (dateTime < previous_rising and previous_rising.day == dateTime.day):
                print('Before astronomical dark end at %s' % previous_rising)
                night = True
            else:
                print('After astronomical dark end of %s' % previous_rising)
                night = False
            #end if
        else:
            if (dateTime > previous_setting and dateTime < next_setting):
                print('After astronomical start of %s' % next_setting)
                night = True
            else:
                print('Before astronomical dark start of %s' % next_setting)
                night = False
            #end if
        #end if



        return night
    #end def

    def isAdjustedNight(self, dateTime):
        self.dateTime = dateTime
        self.observer.date = dateTime

        night = False

        previous_rising = ephem.localtime(self.observer.previous_rising(ephem.Sun(), use_center=True))
        next_rising = ephem.localtime(self.observer.next_rising(ephem.Sun(), use_center=True))

        previous_setting = ephem.localtime(self.observer.previous_setting(ephem.Sun(), use_center=True))
        next_setting = ephem.localtime(self.observer.next_setting(ephem.Sun(), use_center=True))

        if ( dateTime.hour < 12):
            previous_rising = previous_rising - datetime.timedelta(minutes = int(self.advanceDarknessEnd))
            if (dateTime < previous_rising and previous_rising.day == dateTime.day):
                night = True
            else:
                night = False
            #end if
        else:
            previous_setting = previous_setting + datetime.timedelta(minutes=int(self.delayDarknessStart))
            if (dateTime > previous_setting and dateTime < next_setting):
                night = True
            else:
                night = False
            #end if
        #end if
        return night
    #end def

#end class
import csv


from com.astroterip.weather.WeatherData import WeatherData, RainFlag, WetFlag, VelocityUnit, CloudCondition, \
    WindCondition, RainCondition, DayCondition, TempUnit
from com.astroterip.weather.WeatherSensor import WeatherSensor

class WeatherSensorReadError(Exception):

    def __init__(self, message):
        self.message = message

# Returns the data specified in th Cloud Sensor II User’s Manual as a WeatherData object
class BoltwooldWeatherSensor(WeatherSensor):
    def __init__(self, inputFileLocation):
        self.inputFileLocation = inputFileLocation

    # raises WeatherSensorReadError
    def getWeatherData(self):
        weatherData = WeatherData()

        dateElements = []

        with open(self.inputFileLocation, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            str= ""
            for row in reader:
                for str in row:
                    if len(str) > 0:
                        dateElements.append(str)

        if len(dateElements) != 21:
            raise WeatherSensorReadError("Unexpected Boldwood data. Expect 21 columns as per Cloud Sensor II User’s Manual")

        weatherData.date = dateElements[0]
        weatherData.time = dateElements[1]
        weatherData.tempUnit = TempUnit(dateElements[2])
        weatherData.velocityUnits = VelocityUnit(dateElements[3])   # VelocityUnit.K
        weatherData.skyAmbientTemp = float(dateElements[4])
        weatherData.ambientTemp = float(dateElements[5])
        weatherData.sensorCaseTemp = float(dateElements[6])
        weatherData.windSpeed = float(dateElements[7])
        weatherData.relativeHumPercent = float(dateElements[8])
        weatherData.dewPointPercent = float(dateElements[9])
        weatherData.heaterTemp = float(dateElements[10])
        weatherData.rainFlag = RainFlag(dateElements[11])    # RainFlag.RAINING
        weatherData.wetFlag = WetFlag(dateElements[12]) # WetFlag.WET
        weatherData.sinceLastReadingSeconds = int(dateElements[13])
        weatherData.lastFileWrite = dateElements[14]
        weatherData.cloudCondition = CloudCondition(dateElements[15])   # CloudCondition.Unknown
        weatherData.windCondition = WindCondition(dateElements[16])    # WindCondition.Unknown
        weatherData.rainCondition = RainCondition(dateElements[17])    # RainCondition.Unknown
        weatherData.dayCondition = DayCondition(dateElements[18])     # DayCondition.Unknown
        weatherData.domeCloseRequested = (dateElements[19] == '1')
        weatherData.alert = (dateElements[20] == '1')

        return weatherData
    #end method

#end class





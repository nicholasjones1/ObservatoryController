from abc import ABC, abstractmethod


class WeatherSensor(ABC):

    @abstractmethod
    def getWeatherData(self):
        pass

#end class
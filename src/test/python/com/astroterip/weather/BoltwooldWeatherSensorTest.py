import csv
import os
import unittest

import logging

from com.astroterip.weather.BoltwooldWeatherSensor import BoltwooldWeatherSensor, WeatherSensorReadError
from com.astroterip.weather.WeatherData import TempUnit, VelocityUnit, RainFlag, WetFlag, CloudCondition, WindCondition, \
    RainCondition, DayCondition


class BoltwooldWeatherSensorTest(unittest.TestCase):

    def test_normal(self):
        logging.basicConfig(filename='ObservatoryControllerTesting.log', level=logging.DEBUG)

        filePath = os.path.join('../../../../', 'resources/aag-cloudwatcher/aag_sld.dat')

        sensor = BoltwooldWeatherSensor(filePath)
        weatherData = sensor.getWeatherData()
        print("Received weather data from Boltwood weather sensor: %s " % weatherData)

        self.assertEqual('2018-05-24', weatherData.date)
        self.assertEqual('07:24:06.00', weatherData.time)
        self.assertEqual(TempUnit.C, weatherData.tempUnit)
        self.assertEqual(VelocityUnit.K, weatherData.velocityUnits)
        self.assertEqual(1.3, weatherData.skyAmbientTemp)
        self.assertEquals(17.0, weatherData.ambientTemp)
        self.assertEquals(17.0, weatherData.sensorCaseTemp)
        self.assertEquals(0, weatherData.windSpeed)
        self.assertEquals(62, weatherData.relativeHumPercent)
        self.assertEquals(9.7, weatherData.dewPointPercent)
        self.assertEquals(10, weatherData.heaterTemp)
        self.assertEquals(RainFlag.DRY, weatherData.rainFlag)
        self.assertEquals(WetFlag.DRY, weatherData.wetFlag)
        self.assertEquals(0, weatherData.sinceLastReadingSeconds)
        self.assertEquals("043244.30840", weatherData.lastFileWrite)
        self.assertEquals(CloudCondition.VeryCloudy, weatherData.cloudCondition)
        self.assertEquals(WindCondition.Calm, weatherData.windCondition)
        self.assertEquals(RainCondition.Dry, weatherData.rainCondition)
        self.assertEquals(DayCondition.VeryLight, weatherData.dayCondition)
        self.assertEquals(False, weatherData.domeCloseRequested)
        self.assertEquals(False, weatherData.alert)
     #end class


    def test_alert(self):
        logging.basicConfig(filename='ObservatoryControllerTesting.log', level=logging.DEBUG)

        filePath = os.path.join('../../../../', 'resources/aag-cloudwatcher/aag_sld_alert.dat')

        sensor = BoltwooldWeatherSensor(filePath)
        weatherData = sensor.getWeatherData()
        print("Received weather data from Boltwood weather sensor: %s " % weatherData)
        self.assertEquals(True, weatherData.alert)
        self.assertEquals(False, weatherData.domeCloseRequested)
    #end class

    def test_closedome(self):
        logging.basicConfig(filename='ObservatoryControllerTesting.log', level=logging.DEBUG)

        filePath = os.path.join('../../../../', 'resources/aag-cloudwatcher/aag_sld_alert.dat')

        sensor = BoltwooldWeatherSensor(filePath)
        weatherData = sensor.getWeatherData()
        print("Received weather data from Boltwood weather sensor: %s " % weatherData)
        self.assertEquals(False, weatherData.alert)
        self.assertEquals(True, weatherData.domeCloseRequested)
    #end class

    def test_bad_data(self):
        logging.basicConfig(filename='ObservatoryControllerTesting.log', level=logging.DEBUG)

        filePath = os.path.join('../../../../', 'resources/aag-cloudwatcher/aag_sld_bad_data.dat')

        sensor = BoltwooldWeatherSensor(filePath)

        with self.assertRaises(WeatherSensorReadError):
            sensor.getWeatherData()

    #end class


if __name__ == '__main__':
    unittest.main()
import unittest
from datetime import timezone, datetime, tzinfo
from com.astroterip.ephem.Sun import Sun


class SunTest(unittest.TestCase):

    def test_isLight_is_true_during_evening_astro_twilight(self):
        sun = Sun("observatory.ini")
        dateTime3 = datetime(2018, 6, 20, 18, 21, 5, 1)
        night = sun.isNight(dateTime3)
        self.assertFalse(night, "should not be night yet")

    def test_isLight_is_true_during_morning_astro_twilight(self):
        sun = Sun("observatory.ini")
        # after astronomical twilight
        dateTime3 = datetime(2018, 6, 20, 6, 58, 5, 1)
        night = sun.isNight(dateTime3)
        self.assertFalse(night, "should not be night yet")

    def test_isDark_is_true_when_before_midnight(self):
        sun = Sun("observatory.ini")
        dateTime1 = datetime(2018, 6, 20, 19, 21, 5, 1)
        night = sun.isNight(dateTime1)
        self.assertTrue(night, "it is night")

    def test_isDark_is_true_when_after_midnight(self):
        sun = Sun("observatory.ini")
        dateTime2 = datetime(2018, 6, 21, 6, 3, 5, 7777)
        night = sun.isNight(dateTime2)
        self.assertTrue(night, "it is dark in the early morning")

    def test_isLight_is_true_when_in_astro_twlight(self):
        sun = Sun("observatory.ini")
        # just before astronomical twilight starts
        dateTime2 = datetime(2018, 6, 21, 6, 8, 5, 7777)
        # dateTime2 = datetime(2018, 6, 21, 5, 50, 5, 7777, tzinfo=timezone.utc)

        day = sun.isDay(dateTime2)
        self.assertTrue(day, "should be light now")

    def test_isNightAdjusted_is_true_when_morning_dark(self):
        sun = Sun("observatory.ini")
        # just before astronomical twilight starts
        dateTime2 = datetime(2018, 6, 21, 5, 8, 5, 7777)
        # dateTime2 = datetime(2018, 6, 21, 5, 50, 5, 7777, tzinfo=timezone.utc)

        night = sun.isAdjustedNight(dateTime2)
        self.assertTrue(night, "should be night now now")

    def test_isNightAdjusted_when_before_advanceDarknessEnd(self):
        sun = Sun("observatory.ini")
        dateTime2 = datetime(2018, 6, 21, 5, 8, 5, 7777)
        night = sun.isAdjustedNight(dateTime2)
        self.assertTrue(night, "should be night now now")

    def test_isNightAdjusted_when_after_delayDarknessStart(self):
        sun = Sun("observatory.ini")
        dateTime2 = datetime(2018, 6, 20, 19, 21, 5, 1)
        night = sun.isAdjustedNight(dateTime2)
        self.assertTrue(night, "should be night now now")

if __name__ == '__main__':
    unittest.main()
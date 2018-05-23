


# functions
from enum import Enum


class Environmment() :
    def __init__(self):
        # pessimistic defaults,
        self.clear = False
        self.night = False
        self.calm = False
        self.dry = False
#end class

class WeatherEvent(Enum):
    CLEAR = 1
    CLOUDY = 2
    DRY = 3
    RAIN = 4
    DAY = 5
    NIGHT = 6
    CALM = 7
    WINDY = 8
#end class enum



class ObservatoryController():
    def __init__(self):
        self.environmnent = Environmment()

        # a dictionary that maps Events to Function objects (points to functions)
        self.event_to_action = {}

        self.event_to_action.update({WeatherEvent.CALM: self.calm_event_func})
        self.event_to_action.update({WeatherEvent.WINDY: self.windy_event_func})

        self.event_to_action.update({WeatherEvent.DRY: self.dry_event_func})
        self.event_to_action.update({WeatherEvent.RAIN: self.rain_event_func})
        self.event_to_action.update({WeatherEvent.DAY: self.day_event_func})
        self.event_to_action.update({WeatherEvent.NIGHT: self.calm_event_func})
        self.event_to_action.update({WeatherEvent.CLEAR: self.clear_event_func})
        self.event_to_action.update({WeatherEvent.CLOUDY: self.cloudy_event_func})

    def receive_event(self, WeatherEvent):
        f = self.event_to_action[WeatherEvent]
        f()


    def calm_event_func(self):
        print("I is calm")

    def cloudy_event_func(self):
        print("Clouds")

    def clear_event_func(self):
        print("It'clear")

    def windy_event_func(self):
        print("Too windy")

    def rain_event_func(self):
        print("I is calm")

    def dry_event_func(self):
        print("It is fine, no rain")

    def day_event_func(self):
        print("Too windy")

    def night_event_func(self):
        print("It is calm")

if __name__ == '__main__':

    controller = ObservatoryController()
    controller.receive_event(WeatherEvent.CALM);
    controller.receive_event(WeatherEvent.CLEAR);
    controller.receive_event(WeatherEvent.DRY);
    controller.receive_event(WeatherEvent.NIGHT);
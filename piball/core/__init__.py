import abc
import logging
from gpiozero import Button, DigitalOutputDevice

logger = logging.getLogger(__name__)


class LeafSwitch(Button):
    """ Represents any of the various leaf switches on the playfield (GPIO) """

    def __init__(self, *args, **kwargs):
        kwargs.pop('pull_up', None)
        super().__init__(*args, pull_up=False, **kwargs)


class Relay(DigitalOutputDevice):
    """ Represents one of the Relay output signals sent from the pi (GPIO) """


class PlayfieldDevice(metaclass=abc.ABCMeta):
    BASE_POINTS = 1
    BASE_MULTIPLIER = 1

    @classmethod
    def find_element_device(cls, element):
        for subclass in cls.__subclasses__():
            if subclass.__name__ == element.type:
                return subclass.from_element(element)

    @classmethod
    @abc.abstractmethod
    def from_element(cls, element):
        return NotImplemented

    def __init__(self, points, multiplier, name):
        logger.debug(f'Instantiated PlayfieldDevice {self}')
        self.name = name
        self.points = points or self.BASE_POINTS
        self.multiplier = multiplier or self.BASE_MULTIPLIER
        self.point_cache = 0
        self.trigger_count = 0

    def __str__(self):
        return f'{self.__class__.__name__} {self.name} (pts={self.points},mult={self.multiplier})'

    def read_score(self):
        current_score = self.point_cache
        self.point_cache = 0
        return current_score

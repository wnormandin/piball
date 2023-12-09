import logging
from . import LeafSwitch, Relay, PlayfieldDevice
from ..db.models import ElementModel

logger = logging.getLogger(__name__)


class Bumper(PlayfieldDevice):
    """ Represents 1 bumper type device on the playfield, controls a Relay and uses a leaf switch to trigger """

    BASE_POINTS = 25
    BASE_MULTIPLIER: int = 1

    @classmethod
    def from_element(cls, element: ElementModel):
        return cls(
            leaf_switch_pin=element.input_gpio_pin,
            relay_pin=element.output_gpio_pin,
            name=element.input_label.split('_')[0]
        )

    def __init__(self, leaf_switch_pin: int, relay_pin: int, name: str, points: int = None, multiplier: int = None):
        super().__init__(points=points, multiplier=multiplier, name=name)

        self.trigger_switch = LeafSwitch(pin=leaf_switch_pin)
        self.power = Relay(pin=relay_pin)
        self.duty_cycle = 0.02
        self.duty_cycle_remaining = 0
        self.cool_down = 0.2
        self.cool_down_remaining = 0

    @property
    def powered(self):
        return self.power.is_active

    @property
    def triggered(self):
        return self.trigger_switch.is_active

    @property
    def cooling_down(self):
        return self.cool_down_remaining > 0

    @property
    def firing(self):
        return self.duty_cycle_remaining > 0

    def fire(self):
        if self.firing:
            logger.debug(f'{self} is already fired, not firing')
            return
        if self.cooling_down:
            logger.debug(f'{self} is cooling down, not firing')
            return

        logger.debug(f'Firing {self}')
        self.power.on()
        self.duty_cycle_remaining = self.duty_cycle
        self.point_cache += self.points * self.multiplier
        self.trigger_count += 1
        assert self.firing

    def start_cool_down(self):
        if self.cooling_down:
            logger.debug(f'{self} is already cooling down, ignoring')
            return

        self.power.off()
        logger.debug(f'{self} is cooling down')
        self.cool_down_remaining = self.cool_down
        assert self.cooling_down

    def handle_time(self, elapsed):
        if self.duty_cycle_remaining > 0:
            self.duty_cycle_remaining -= elapsed
            logger.debug(f'Duty cycle remaining: {self.duty_cycle_remaining}')
            if not self.firing:
                self.start_cool_down()
                return
        if self.cool_down_remaining > 0:
            self.cool_down_remaining -= elapsed
            logger.debug(f'Cooldown remaining: {self.cool_down_remaining}')

    def on_loop(self, elapsed):
        self.handle_time(elapsed)
        if not self.powered and self.triggered:
            self.fire()


class PopBumper(Bumper):
    """ Pop bumper element on the playfield """


class SlingShot(Bumper):
    """ Slingshot element on the playfield """

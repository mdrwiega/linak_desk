""" The Linak desk height sensor platform"""

from homeassistant.helpers.entity import Entity

from .linak_desk import LinakDesk

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([LinakDeskSensor()])

class LinakDeskSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Linak Desk Height'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return 'm'

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        desk = LinakDesk('DD:6D:C2:F4:39:7F')
        height, speed = desk.read_desk_height_speed()
        self._state = height
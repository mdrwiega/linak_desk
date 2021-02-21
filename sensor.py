""" The Linak desk height sensor platform"""

import logging
import json
import voluptuous as vol

from homeassistant.helpers.entity import Entity
from homeassistant.helpers import config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_MAC

from .linak_desk import LinakDesk

_LOGGER = logging.getLogger(__name__)

DEFAULT_MIN_HEIGHT = 0.62
DEFAULT_MAX_HEIGHT = 1.28

DOMAIN = 'linak_desk'

CONF_MIN_HEIGHT = 'min_height_m'
CONF_MAX_HEIGHT = 'max_height_m'

MAC_REGEX = "(?i)^(?:[0-9A-F]{2}[:]){5}(?:[0-9A-F]{2})$"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_MAC): cv.matches_regex(MAC_REGEX),
    vol.Optional(CONF_MIN_HEIGHT, default=DEFAULT_MIN_HEIGHT): cv.positive_float,
    vol.Optional(CONF_MAX_HEIGHT, default=DEFAULT_MAX_HEIGHT): cv.positive_float,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""

    _LOGGER.debug("Initializing Linak SENSOR: %s", config)

    if not config[CONF_MAC]:
        _LOGGER.error('Missing MAC address in configuration')
        return False

    add_entities([LinakDeskSensor(config[CONF_MAC], config[CONF_MIN_HEIGHT], config[CONF_MAX_HEIGHT])])

    return True

class LinakDeskSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, mac, min_height, max_height):
        """Initialize the sensor."""
        self._state = None
        self._mac = mac
        self._min_height = min_height
        self._max_height = max_height

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
        desk = LinakDesk(self._mac, self._min_height, self._max_height)
        height, speed = desk.read_desk_height_speed()
        self._state = height
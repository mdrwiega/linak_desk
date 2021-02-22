""" The Linak desk height sensor platform"""

import logging
import voluptuous as vol

from homeassistant.helpers.entity import Entity
from homeassistant.helpers import config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_MAC

from .linak_desk import LinakDesk
from .const import (
    DOMAIN,
    CONF_MIN_HEIGHT,
    CONF_MAX_HEIGHT,
    DEFAULT_MIN_HEIGHT,
    DEFAULT_MAX_HEIGHT,
    MAC_REGEX
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_MAC): cv.matches_regex(MAC_REGEX),
    vol.Optional(CONF_MIN_HEIGHT, default=DEFAULT_MIN_HEIGHT): cv.positive_float,
    vol.Optional(CONF_MAX_HEIGHT, default=DEFAULT_MAX_HEIGHT): cv.positive_float,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""

    _LOGGER.debug("Initializing Linak sensor: %s", config)

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
        """Fetch new state data for the sensor."""
        try:
            desk = LinakDesk(self._mac, self._min_height, self._max_height)
            height, speed = desk.read_desk_height_speed()
            self._state = height
        except ConnectionError as e:
            _LOGGER.error("Connection error: " + str(e))

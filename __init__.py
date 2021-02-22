"""The linak_desk component."""

import logging
import asyncio
import voluptuous as vol

from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
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

@asyncio.coroutine
async def async_setup(hass, config):

    @callback
    def service_set_height(call):
        """ Handle the service call. """
        _LOGGER.error("Linak Desk Service called")

        mac = 'AA:BB:CC:DD:EE'
        min_height = DEFAULT_MIN_HEIGHT
        max_height = DEFAULT_MAX_HEIGHT
        target_height = call.data.get('height', 1.0)

        desk = LinakDesk(mac, min_height, max_height)
        desk.move_to(target_height)

    hass.services.async_register(DOMAIN, 'set_height', service_set_height)

    return True

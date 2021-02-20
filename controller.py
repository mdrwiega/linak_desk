"""Platform for sensor integration."""

DOMAIN = 'linak_desk_controller'

ATTR_NAME = "name"
DEFAULT_NAME = "World"

def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""

    def handle_hello(call):
        """Handle the service call."""
        name = call.data.get(ATTR_NAME, DEFAULT_NAME)

        hass.states.set("hello_service.hello", name)

    hass.services.register(DOMAIN, "hello", handle_hello)

    return True

def setup(hass, config):
    hass.data[DOMAIN] = {
        'temperature': 23
    }

    hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)

    return True
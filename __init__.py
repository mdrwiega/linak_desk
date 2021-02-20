"""The linak_desk_controller component."""

DOMAIN = 'linak_desk_controller'

def async_setup(hass, config):

    def service_get_height(call):
        """Handle the service call."""
       

        hass.states.set("linak_desk_controller.current_height", 10.0)

    hass.services.register(DOMAIN, "get_height", get_height)

    return True


class LinakDeskController:
    def get_height(self):
        return 10.0
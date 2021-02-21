import logging
import struct
import threading
from bluepy.btle import Peripheral, DefaultDelegate
from datetime import datetime, timedelta

_LOGGER = logging.getLogger(__name__)


class LinakDesk:
    """ It connects to the desk driver and requests the current desk height    
        The desk height is calculated as a min_height + offset received from the controller
    """

    UUID_HEIGHT_SPEED = '99FA0021-338A-1024-8A49-009C0215F78A'
    UUID_CONTROL  = '99FA0002-338A-1024-8A49-009C0215F78A'
    UUID_MOVE_TO  = '99FA0031-338A-1024-8A49-009C0215F78A'

    def __init__(self, mac, min_height = 0.635, max_height = 1.28):
        _LOGGER.debug("LinakDesk initialization.")

        self.min_height = min_height

        try:
            self.peripheral = Peripheral(mac, "random")
        except Exception as e:
            _LOGGER.error("LinakDesk connection error: " + str(e))

    def read_desk_height_speed(self):
        """ Read the desk height and the speed from the Linak device """
        try:
            data = self._read_characteristic(self.UUID_HEIGHT_SPEED)
            height = self._extract_height(data)
            speed = self._extract_speed(data)
        finally:
            self.disconnect()
        return height, speed
    
    def disconnect(self):
        self.peripheral.disconnect()

    def _get_handle(self, uuid):
        return self.peripheral.getCharacteristics(uuid=uuid)[0].getHandle()

    def _read_characteristic(self, uuid, handle=None):
        if handle is None:
            handle = self._get_handle(uuid)
        return self.peripheral.readCharacteristic(handle)

    def _extract_height(self, data):
        """ Extract the height of the desk from raw data """
        raw_offset = struct.unpack('<H', data[0:2])[0]
        if raw_offset == None:
            return None
        return self.min_height + raw_offset / 10000.0

    def _extract_speed(self, data):
        """ Extract the speed of the desk from raw data """
        return struct.unpack('H', data[2:4])[0] & 0x0FFF


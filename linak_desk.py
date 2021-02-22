# Created by Michal Drwiega, 2020

import logging
import struct
import threading
import asyncio
from bluepy.btle import Peripheral, DefaultDelegate
from datetime import datetime, timedelta
import time

_LOGGER = logging.getLogger(__name__)

class LinakDesk:
    """ It connects to the desk driver and requests the current desk height    
        The desk height is calculated as a min_height + offset received from the controller
    """

    UUID_HEIGHT_SPEED = '99FA0021-338A-1024-8A49-009C0215F78A'
    UUID_CONTROL  = '99FA0002-338A-1024-8A49-009C0215F78A'
    UUID_MOVE_TO  = '99FA0031-338A-1024-8A49-009C0215F78A'

    class NotificationsHandler(DefaultDelegate):
        def __init__(self, _peripheral, _callback):
            DefaultDelegate.__init__(self)
            self.peripheral = _peripheral
            self.peripheral.withDelegate(self)
            self.callback = _callback
            self.thread = None
            self.running = True

        def start_thread(self):
            self.thread = threading.Thread(target=self._run)
            self.thread.start()

        def stop_thread(self):
            self.running = False
            if self.thread is not None:
                self.thread.join()
                self.thread = None

        def _run(self):
            while self.running:
                self.per.waitForNotifications(0.1)

        def handleNotification(self, cHandle, data):
            self.callback(data)

    def __init__(self, mac, min_height = 0.635, max_height = 1.28):
        _LOGGER.debug("LinakDesk initialization.")

        self.min_height = min_height
        self.max_height = max_height
        self.height = 0
        self.speed = 0
        self.connected = False

        for i in range(2):
            try:
                self.peripheral = Peripheral(mac, "random")
                self.connected = True
                break
            except btle.BTLEException as e:
                _LOGGER.debug("LinakDesk connection error: " + str(e))
                time.sleep(0.5)            

        if not self.connected:
            _LOGGER.error("LinakDesk connection error: " + str(e))

        self.notification_handler = self.NotificationsHandler(self.peripheral, self.update)
        self.height_speed_handle = self._get_handle(self.UUID_HEIGHT_SPEED)

    def __del__(self):
        self.disconnect()

    def update(self, data):
        """Update the main information about the desk based on the raw data received"""
        self.height = self._extract_height(data)
        self.speed = self._extract_speed(data)        
        print("Height: " + str(self.height) + ", speed: " + str(self.speed))

    def read_desk_height_speed(self):
        """ Read the desk height and the speed from the Linak device """
        if not self.connected:
            return None, None

        try:
            data = self._read_characteristic(self.UUID_HEIGHT_SPEED, self.height_speed_handle)
            height = self._extract_height(data)
            speed = self._extract_speed(data)
            return height, speed
        except Exception as e:
            _LOGGER.error("Exception during desk height reading: " + str(e))
            return None, None
    
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

    def _command(self, data):
        return 

    def subscribe(self):
        self.notification_handler.start_thread()
        cmd = struct.pack('BB', 1, 0)
        _LOGGER.debug("Writing request %s to %s", self.to_hex_string(cmd), self.UUID_HEIGHT_SPEED)
        self.peripheral.writeCharacteristic(self.height_speed_handle + 1, cmd, withResponse=True)

    def unsubscribe(self):
        self.notification_handler.stop_thread()

    def to_hex_string(self, data):
        return " ".join("0x{:02X}".format(x) for x in data)

    def _write(self, uuid, command, handle=None):
        if handle is None:
            handle = self._get_handle(uuid)

        cmd = struct.pack('<H', command)
        _LOGGER.debug("Writing request %s to %s", self.to_hex_string(cmd), uuid)

        self.peripheral.writeCharacteristic(handle, cmd, withResponse=True)

    def move_to(self, target_height):
        if not self.connected:
            _LOGGER.warning('Not connected to the device')
            return None, None

        raw_value = int((target_height - self.min_height) * 10000.0)

        height, speed = self.read_desk_height_speed()        
        _LOGGER.debug('Start move_to %.2f (init height: %.2f, raw_value: %d)' %(target_height, height, raw_value))

        move_to_handle = self._get_handle(self.UUID_MOVE_TO)

        for i in range(40):
            _LOGGER.debug("Height: {:.2f}m Target: {:.2f}m Speed: {:.2f}mm/s".format(height, target_height, speed))
            self._write(self.UUID_MOVE_TO, raw_value, move_to_handle)
            time.sleep(0.25)

        height, speed = self.read_desk_height_speed() 
        _LOGGER.debug("Final height: {:.2f}m, Target height: {:.2f}m".format(height, target_height))
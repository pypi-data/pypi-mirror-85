import abc
import logging
import time
from typing import Callable

from bluepy import btle
from bluepy.btle import DefaultDelegate

_LOGGER = logging.getLogger(__name__)


class TionDelegation(DefaultDelegate):
    def __init__(self):
        self._data = None
        DefaultDelegate.__init__(self)

    def handleNotification(self, handle: int, data: bytes):
        self._data = data
        _LOGGER.debug("Got data in %d response %s", handle, bytes(data).hex())

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            _LOGGER.debug("Discovered device %s", dev.addr)
        elif isNewData:
            _LOGGER.debug("Received new data from %s", dev.addr)

    @property
    def data(self) -> bytes:
        return self._data


class TionException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class tion:
    statuses = ['off', 'on']
    modes = ['recirculation', 'mixed']  # 'recirculation', 'mixed' and 'outside', as Index exception
    uuid_notify: str = ""
    uuid_write: str = ""

    def __init__(self, mac: str):
        self._mac = mac
        self._btle: btle.Peripheral = btle.Peripheral(None)
        self._delegation = TionDelegation()
        self._fan_speed = 0

        #states
        self._in_temp: int = 0
        self._out_temp: int = 0
        self._target_temp: int = 0
        self._fan_speed: int = 0

    @abc.abstractmethod
    def _send_request(self, request: bytearray) -> bytearray:
        """ Send request to device

        Args:
          request : array of bytes to send to device
        Returns:
          array of bytes with device response
        """
        pass

    @abc.abstractmethod
    def _decode_response(self, response: bytearray) -> dict:
        """ Decode response from device

        Args:
          response: array of bytes with data from device, taken from _send_request
        Returns:
          dictionary with device response
        """
        pass

    @abc.abstractmethod
    def _encode_request(self, request: dict) -> bytearray:
        """ Encode dictionary of request to byte array

        Args:
          request: dictionry with request
        Returns:
          Byte array for sending to device
        """
        pass

    @abc.abstractmethod
    def get(self, keep_connection: bool = False) -> dict:
        """ Get device information
        Returns:
          dictionay with device paramters
        """
        pass

    @property
    def mac(self):
        return self._mac

    def decode_temperature(self, raw: bytes) -> int:
        """ Converts temperature from bytes with addition code to int
        Args:
          raw: raw temperature value from Tion
        Returns:
          Integer value for temperature
        """
        barrier = 0b10000000
        if (raw < barrier):
            result = raw
        else:
            result = -(~(result - barrier) + barrier + 1)

        return result

    def _process_status(self, code: int) -> str:
        try:
            status = self.statuses[code]
        except IndexError:
            status = 'unknown'
        return status

    @property
    def connection_status(self):
        connection_status = "disc"
        try:
            connection_status = self._btle.getState()
        except btle.BTLEInternalError as e:
            if str(e) == "Helper not started (did you call connect()?)":
                pass
            else:
                raise e
        except btle.BTLEDisconnectError as e:
            pass
        except BrokenPipeError as e:
            self._btle = btle.Peripheral(None)

        return connection_status

    def _connect(self):
        if self.mac == "dummy":
            _LOGGER.info("Dummy connect")
            return

        if self.connection_status == "disc":
            try:
                self._btle.connect(self.mac, btle.ADDR_TYPE_RANDOM)
                for tc in self._btle.getCharacteristics():
                    if tc.uuid == self.uuid_notify:
                        self.notify = tc
                    if tc.uuid == self.uuid_write:
                        self.write = tc
            except btle.BTLEDisconnectError as e:
                _LOGGER.warning("Got %s exception", str(e))
                time.sleep(2)
                raise e

    def _disconnect(self):
        if self.connection_status != "disc":
            if self.mac != "dummy":
                self._btle.disconnect()

    def _try_write(self, request: bytearray):
        if self.mac != "dummy":
            _LOGGER.debug("Writing %s to %s", bytes(request).hex(), self.write.uuid)
            return self.write.write(request)
        else:
            _LOGGER.info("Dummy write")
            return "dummy write"

    def _do_action(self, action: Callable, max_tries: int = 3, *args, **kwargs):
        tries: int = 0
        while tries < max_tries:
            _LOGGER.debug("Doing " + action.__name__ + ". Attempt " + str(tries + 1) + "/" + str(max_tries))
            try:
                if action.__name__ != '_connect':
                    self._connect()

                response = action(*args, **kwargs)
                break
            except Exception as e:
                tries += 1
                _LOGGER.warning("Got exception while " + action.__name__ + ": " + str(e))
                pass
        else:
            if action.__name__ == '_connect':
                message = "Could not connect to " + self.mac
            elif action.__name__ == '__try_write':
                message = "Could not write request + " + kwargs['request'].hex()
            elif action.__name__ == '__try_get_state':
                message = "Could not get updated state"
            else:
                message = "Could not do " + action.__name__

            raise TionException(action.__name__, message)

        return response

    def _enable_notifications(self):
        if self.mac != "dummy":
            _LOGGER.debug("Enabling notification")
            setup_data = b"\x01\x00"

            _LOGGER.debug("Notify handler is %s", self.notify.getHandle())
            notify_handle = self.notify.getHandle() + 1

            _LOGGER.debug("Will write %s to %s handle", setup_data, notify_handle)
            result = self._btle.writeCharacteristic(notify_handle, setup_data, withResponse=True)
            _LOGGER.debug("Result is %s", result)
            self._btle.withDelegate(self._delegation)
            self.notify.read()
        else:
            result = True
        return result

    @property
    def fan_speed(self):
        return self._fan_speed

    @fan_speed.setter
    def fan_speed(self, new_speed: int):
        if 0 <= new_speed <= 6:
            self._fan_speed = new_speed

        else:
            _LOGGER.warning("Incorrect new fan speed. Will use 1 instead")
            self._fan_speed = 1

        # self.set({"fan_speed": new_speed})

    def _process_mode(self, mode_code: int) -> str:
        try:
            mode = self.modes[mode_code]
        except IndexError:
            mode = 'outside'
        return mode

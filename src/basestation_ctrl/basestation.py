from bluepy import btle
import logging
import time

logger = logging.getLogger("basestation-ctrl")


class Basestation:
    # LHv2 GATT service
    LHV2_GATT_SERVICE_UUID = btle.UUID('00001523-1212-efde-1523-785feabcd124')
    LHV2_GATT_CHAR_POWER_CTRL_UUID = btle.UUID('00001525-1212-efde-1523-785feabcd124')
    LHV2_GATT_CHAR_MODE_UUID = btle.UUID('00001524-1212-efde-1523-785feabcd124')

    # Power management
    POWER_ON = b'\x01'
    POWER_OFF = b'\x00'

    def __init__(self, mac_addr, hci_interface):
        self.dev = btle.Peripheral()
        self.mac_addr = mac_addr
        self.hci_interface = hci_interface
        self.characteristics = None
        self.name = None

    def power_on(self, max_tries, try_pause):
        self._connect(max_tries, try_pause)
        logger.debug(f'Powering on {self.mac_addr}')
        self._write_characteristic(self.LHV2_GATT_CHAR_POWER_CTRL_UUID, self.POWER_ON)
        self._disconnect()

    def power_off(self, max_tries, try_pause):
        self._connect(max_tries, try_pause)
        logger.debug(f'Powering off {self.mac_addr}')
        self._write_characteristic(self.LHV2_GATT_CHAR_POWER_CTRL_UUID, self.POWER_OFF)
        self._disconnect()

    def _connect(self, max_tries, try_pause):
        tries = 0
        logger.info(f'Connecting to {self.mac_addr}')
        while True:
            logger.debug(f'Try ({tries+1}/{max_tries})')
            try:
                self.dev.connect(self.mac_addr, iface=self.hci_interface,
                                 addrType=btle.ADDR_TYPE_RANDOM)

                logger.debug(f'Device state: {self.dev.getState()}')

                if self.dev.getState() != 'conn':
                    logger.debug(f'Device state is not "conn"')
                    continue

                chars = self.dev.getCharacteristics()
                self.characteristics = dict([(c.uuid, c) for c in chars])
                self.name = self.characteristics[btle.AssignedNumbers.device_name].read().decode()
                mode = self.characteristics[self.LHV2_GATT_CHAR_MODE_UUID].read()
                logger.info(f'Connected to {self.name} ({self.dev.addr}, mode={mode.hex()})')

                break

            except btle.BTLEDisconnectError as e:
                logger.debug(f'Exception: {e}')

                tries += 1
                if tries < max_tries:
                    logger.info(f'Failed to connect. Retrying in {try_pause}s...')
                    time.sleep(try_pause)
                    continue
                else:
                    logger.error(f'Reached maximum number of tries. Exiting.')
                    raise RuntimeError(f"Failed to connect to {self.mac_addr}")

    def _disconnect(self):
        logger.info(f'Disconnecting from {self.name}')
        self.dev.disconnect()

    def _write_characteristic(self, uuid, val):
        charc = self.characteristics[uuid]
        charc.write(val, withResponse=True)
        logger.debug(f'Writing {val.hex()} to {charc.uuid.getCommonName()}')

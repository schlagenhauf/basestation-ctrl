from bluepy import btle
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

    def connect(self, try_count, try_pause):
        for tries in range(try_count):
            try:
                logger.info(f'Connecting to {self.mac_addr}')
                self.dev.connect(self.mac_addr, iface=self.hci_interface,
                                 addrType=btle.ADDR_TYPE_RANDOM)
                logger.info(f'Device state: {self.dev.getState()}')

                chars = self.dev.getCharacteristics()
                self.characteristics = dict([(c.uuid, c) for c in chars])

                self.name = self.characteristics[btle.AssignedNumbers.device_name].read().decode()

                mode = self.characteristics[self.LHV2_GATT_CHAR_MODE_UUID].read()
                logger.info(f'Connected to {self.name} ({self.dev.addr}, mode={mode.hex()})')

                break

            except btle.BTLEDisconnectError as e:
                logger.info(e)
                logger.warning(
                    f'Failed to connect ({tries+1}/{try_count}). Retrying in {try_pause}s...')
                time.sleep(try_pause)
                continue

    def disconnect(self):
        logger.info(f'Diconnecting from {self.name}')
        self.dev.disconnect()

    def write_characteristic(self, uuid, val):
        charc = self.characteristics[uuid]
        charc.write(val, withResponse=True)
        logger.info(f'Writing {val.hex()} to {charc.uuid.getCommonName()}')

    def power_on(self):
        self.write_characteristic(self.LHV2_GATT_CHAR_POWER_CTRL_UUID, self.POWER_ON)

    def power_off(self):
        self.write_characteristic(self.LHV2_GATT_CHAR_POWER_CTRL_UUID, self.POWER_OFF)

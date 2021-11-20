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

    # Defaults
    TRY_COUNT = 5
    TRY_PAUSE = 2
    GLOBAL_TIMEOUT = 0

    def __init__(self, macAddr, hciIface):
        self.dev = btle.Peripheral()
        self.macAddr = macAddr
        self.hciIface = hciIface
        self.characteristics = None
        self.name = None

    def connect(self, try_count, try_pause):
        for tries in range(try_count):
            try:
                logger.info(f'Connecting to {self.macAddr}')
                self.dev.connect(self.macAddr, iface=self.hciIface, addrType=btle.ADDR_TYPE_RANDOM)
                logger.info(f'Device state: {self.dev.getState()}')

                if self.characteristics is None:
                    chars = self.dev.getCharacteristics()
                    self.characteristics = dict([(c.uuid, c) for c in chars])

                if self.name is None:
                    self.name = self.getCharacteristic(
                        btle.AssignedNumbers.device_name).read().decode()

                mode = self.getCharacteristic(self.LHV2_GATT_CHAR_MODE_UUID).read()
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

    def getCharacteristic(self, uuid):
        return self.characteristics[uuid]

    def writeCharacteristic(self, uuid, val):
        charc = self.getCharacteristic(uuid)
        charc.write(val, withResponse=True)
        logger.info(f'Writing {val.hex()} to {charc.uuid.getCommonName()}')

    def getName(self):
        return self.name

    def powerOn(self):
        self.writeCharacteristic(self.LHV2_GATT_CHAR_POWER_CTRL_UUID, self.POWER_ON)

    def powerOff(self):
        self.writeCharacteristic(self.LHV2_GATT_CHAR_POWER_CTRL_UUID, self.POWER_OFF)
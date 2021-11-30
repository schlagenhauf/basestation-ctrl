from basestation_ctrl.basestation import Basestation
from bluepy import btle
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BasestationCtrl:
    MAX_NUMBER_OF_TRIES = 3
    TRIES_PAUSE_SECS = 5

    # adtype of the filed "Complete Local Name", see "Generic Access Profile" in the Bluetooth Specs
    LOCALNAME_ADTYPE = 0x09

    def __init__(self, interface=0):
        self.interface = interface

    @staticmethod
    def scan(timeout_secs: float = 10., print_all: bool = False):
        scanner = btle.Scanner()
        devices = scanner.scan(timeout_secs)

        results = {}
        for dev in devices:
            localname = dev.getValueText(BasestationCtrl.LOCALNAME_ADTYPE)
            if print_all or localname.startswith("LHB-"):
                results[localname] = dev.addr

        return results

    def sleep(self, macs, max_tries=MAX_NUMBER_OF_TRIES, try_pause=TRIES_PAUSE_SECS):
        for mac in macs:
            base = Basestation(mac, self.interface)
            logger.info(f'Shutting down {base.name}')
            try:
                base.power_off(max_tries, try_pause)
            except RuntimeError as e:
                logger.error(e)

    def wake(self, macs, max_tries=MAX_NUMBER_OF_TRIES, try_pause=TRIES_PAUSE_SECS):
        for mac in macs:
            base = Basestation(mac, self.interface)
            logger.info(f'Waking up {base.name}')
            try:
                base.power_on(max_tries, try_pause)
            except RuntimeError as e:
                logger.error(e)

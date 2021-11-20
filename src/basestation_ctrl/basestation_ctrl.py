from basestation_ctrl.basestation import Basestation
from bluepy import btle
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BasestationCtrl:
    def __init__(self, interface=0):
        self.interface = interface

    @staticmethod
    def scan(timeout_secs: float = 10., print_all: bool = False):
        scanner = btle.Scanner()
        devices = scanner.scan(timeout_secs)

        # adtype of the filed "Complete Local Name", see "Generic Access Profile" in the Bluetooth Specs
        localname_adtype = 0x09

        for dev in devices:
            #print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
            if dev.getValueText(localname_adtype).startswith("LHB-"):
                print(f"Found a Lighthouse Base Station: {dev.addr}")
            elif print_all:
                print(f"Found a device that is probably not a Lighthouse Base Station: {dev.addr}")

    def sleep(self, macs, tries=10, tries_pause=2):
        for mac in macs:
            lhv2 = Basestation(mac, self.interface)
            lhv2.connect(tries, tries_pause)
            logger.info(f'Shutting down {lhv2.getName()}')
            lhv2.powerOff()
            lhv2.disconnect()

    def wake(self, macs, tries=2, tries_pause=5):
        for mac in macs:
            lhv2 = Basestation(mac, self.interface)
            lhv2.connect(tries, tries_pause)
            logger.info(f'Waking up {lhv2.getName()}')
            lhv2.powerOn()
            lhv2.disconnect()

    def identify(self):
        pass

    def status(self):
        pass

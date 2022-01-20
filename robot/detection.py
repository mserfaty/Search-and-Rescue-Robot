"""
License: You are free to use any part of code in this project as long as you mention original authors of this program:
Alpha Team composed of: Nirmalraj JEYANATHAN Joseph - SERFATY Milan - YE Hang - ZHANG Yujia

Supervised by Aurore (aurore.isep@gmail.com) and Hugo (myrobotswillconquertheworld@gmail.com)
IE.3510 (System Modeling) - ISEP 2022
"""

from ev3dev2.port import LegoPort
from ev3dev2.sensor import Sensor


class MetalDetector(Sensor):
    """
    Metal Detector (based on the LEGO NXT Sound Sensor)
    """
    SYSTEM_DEVICE_NAME_CONVENTION = Sensor.SYSTEM_DEVICE_NAME_CONVENTION

    def __init__(self, address, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        p1 = LegoPort(address)
        p1.mode = 'nxt-analog'
        p1.set_device = 'lego-nxt-sound'
        super(MetalDetector, self).__init__(address, name_pattern, name_exact, driver_name='lego-nxt-sound', **kwargs)

    @property
    def analog_read(self):
        return int(self.value() < 350)

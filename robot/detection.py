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
        return self.value()

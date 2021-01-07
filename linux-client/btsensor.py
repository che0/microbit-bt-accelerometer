#!/usr/bin/env python3
import bluepy
import struct
import os


MICROBIT_ACCELEROMETER_PERIOD_UUID = 'e95dfb24-251d-470a-a062-fa1922dfa9a8'
MICROBIT_ACCELEROMETER_DATA_UUID = 'e95dca4b-251d-470a-a062-fa1922dfa9a8'


class AccelerometerDelegate(bluepy.btle.DefaultDelegate):
    def __init__(self, accelerometerDataHandle):
        super(AccelerometerDelegate, self).__init__()
        self.accelerometerDataHandle = accelerometerDataHandle

    def handleNotification(self, cHandle, data):
        if cHandle != self.accelerometerDataHandle:
            return

        x, y, z = struct.unpack('<hhh', data)
        print(x, y, z)


def main():
    mac = os.getenv('MICROBIT_MAC')
    if not mac:
        print('We need micro:bit Bluetooth MAC address in MICROBIT_MAC\n'
            'You can try `bluetoothctl scan on` or similar tools to find it')
        return

    microbit = bluepy.btle.Peripheral(mac, 'random')

    accelerometer = microbit.getServiceByUUID('e95d0753-251d-470a-a062-fa1922dfa9a8')
    acc_data_descriptor = accelerometer.getDescriptors(MICROBIT_ACCELEROMETER_DATA_UUID)[0]
    microbit.setDelegate(AccelerometerDelegate(acc_data_descriptor.handle))

    client_characteristics = accelerometer.getDescriptors('00002902-0000-1000-8000-00805f9b34fb')[0]
    client_characteristics.write(struct.pack('<H', 1), withResponse=True)

    while True:
        microbit.waitForNotifications(1.0)


if __name__ == '__main__':
    main()

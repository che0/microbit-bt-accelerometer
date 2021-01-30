#!/usr/bin/env python3
import bluepy
import struct
import os

CLIENT_CHARACTERISTICS_CONF_UUID = '00002902-0000-1000-8000-00805f9b34fb'
MB_ACCELEROMETER_SERVICE_UUID = 'e95d0753-251d-470a-a062-fa1922dfa9a8'
MB_ACCELEROMETER_DATA_UUID = 'e95dca4b-251d-470a-a062-fa1922dfa9a8'
MB_ACCELEROMETER_PERIOD_UUID = 'e95dfb24-251d-470a-a062-fa1922dfa9a8'


class AccelerometerDelegate(bluepy.btle.DefaultDelegate):
    def __init__(self, accelerometerDataHandle, dataCallback):
        super(AccelerometerDelegate, self).__init__()
        self.accelerometerDataHandle = accelerometerDataHandle
        self.dataCallback = dataCallback

    def handleNotification(self, cHandle, data):
        if cHandle != self.accelerometerDataHandle:
            return

        x, y, z = struct.unpack('<hhh', data)
        self.dataCallback(x, y, z)


class MicrobitAccelerometer:
    def __init__(self, mac):
        self.mac = mac
        self.microbit = None

    def processData(self, x, y, z):
        print(x, y, z)

    def setNotifications(self):
        self.microbit = bluepy.btle.Peripheral(self.mac, 'random')

        acc_service = self.microbit.getServiceByUUID(MB_ACCELEROMETER_SERVICE_UUID)
        acc_data = acc_service.getDescriptors(MB_ACCELEROMETER_DATA_UUID)[0]
        self.microbit.setDelegate(
            AccelerometerDelegate(acc_data.handle, self.processData))

        # enable gatt notifications for accelerometer data
        ccc = acc_service.getDescriptors(CLIENT_CHARACTERISTICS_CONF_UUID)[0]
        ccc.write(struct.pack('<H', 1), withResponse=True)

    def waitForNotifications(self, timeout):
        self.microbit.waitForNotifications(timeout)


def main():
    mac = os.getenv('MICROBIT_MAC')
    if not mac:
        print('We need micro:bit Bluetooth MAC address in MICROBIT_MAC\n'
              'You can try `bluetoothctl scan on` or similar tools to find it')
        return

    accelerometer = MicrobitAccelerometer(mac)
    accelerometer.setNotifications()

    while True:
        accelerometer.waitForNotifications(1.0)


if __name__ == '__main__':
    main()

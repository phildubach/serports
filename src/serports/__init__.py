#!/usr/bin/env python3

import argparse
import pyudev
import sys

class SerialDevice():
    def __init__(self, device):
        self.dev = device.properties['DEVNAME']
        self.vendor = device.properties['ID_VENDOR']
        self.model = device.properties['ID_MODEL']
        self.serial = device.properties.get('ID_SERIAL_SHORT', '')
        self.initialized = device.properties.asint('USEC_INITIALIZED')

    def __str__(self):
        return f'{self.dev:16} {self.vendor:32} {self.model:32} {self.serial:16}'

    def __lt__(self, other):
        return self.initialized < other.initialized

def printDevice(dev):
    for prop in dev.properties:
        print('>>>', prop, dev.properties[prop])

class SerialDevices():

    def __init__(self):
        self.context = pyudev.Context()
        self.devices = []
        for device in self.context.list_devices(subsystem='tty'):
            if device.properties.get('ID_BUS', None) == 'usb':
                # printDevice(device)
                sd = SerialDevice(device)
                self.devices.append(sd)
        self.devices.sort()

    def list(self):
        for device in self.devices:
            print(device)
        return 0

    def follow(self):
        self.list()
        monitor = pyudev.Monitor.from_netlink(self.context)
        monitor.filter_by('tty')
        while True:
            device = monitor.poll()
            if device.action == 'add':
                sd = SerialDevice(device)
                print(sd)
            elif device.action == 'remove':
                print(device.properties['DEVNAME'], 'removed')

    def last(self):
        if len(self.devices) == 0:
            return -1
        found = self.devices[0]
        for device in self.devices:
            if found.initialized < device.initialized:
                found = device
        print(found.dev)
        return 0

    def wait(self):
        monitor = pyudev.Monitor.from_netlink(self.context)
        monitor.filter_by('tty')
        while True:
            device = monitor.poll()
            if device.action == 'add':
                print(device.properties['DEVNAME'])
                return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--last', help='Only print last added device name', action='store_true')
    parser.add_argument('-f', '--follow', help='Print devices as they get added', action='store_true')
    parser.add_argument('-w', '--wait', help='Wait for new device and return name', action='store_true')
    args = parser.parse_args()
    serial_devices = SerialDevices()
    if args.last:
        ret = serial_devices.last()
    elif args.follow:
        try:
            serial_devices.follow()
            ret = 0
        except KeyboardInterrupt:
            ret = 1
    elif args.wait:
        try:
            serial_devices.wait()
            ret = 0
        except KeyboardInterrupt:
            ret = 1
    else:
        ret = serial_devices.list()
    sys.exit(ret)

if __name__ == "__main__":
    main()

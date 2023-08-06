#!/usr/bin/env python3
import datetime
import asyncio
import argparse
import sys

import bleak

CHARACTERISTIC_UUID = "49535343-1e4d-4bd9-ba61-23c647249616"

class DataPrinter:
    def __init__(self):
        self.last_bpm = -1
        self.last_spo2 = -1
        self.last_pleth = -1

    def multiline(self, pleth, bpm, spo2):
        if bpm != self.last_bpm or spo2 != self.last_spo2:
            print_bpm = '---' if bpm == 255 else str(bpm).rjust(3)
            print_spo2 = '---' if spo2 == 127 else str(spo2).rjust(3)
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            print("[{}]\tBPM: {}\tSpO2: {}".format(timestamp, print_bpm, print_spo2))
            self.last_bpm, self.last_spo2 = bpm, spo2

    def oneline(self, pleth, bpm, spo2):
        if pleth != self.last_pleth or bpm != self.last_bpm or spo2 != self.last_spo2:
            print_bpm = '---' if bpm == 255 else str(bpm).rjust(3)
            print_spo2 = '---' if spo2 == 127 else str(spo2).rjust(3)
            print_pleth = ('*' * (pleth // 10)).ljust(10)
            sys.stdout.write("BPM:{}  [{}]  SpO2:{}\r".format(print_bpm, print_pleth, print_spo2))
            self.last_pleth, self.last_bpm, self.last_spo2 = pleth, bpm, spo2

def make_handler(user_handler):
    def raw_handler(sender, data):
        pleth = data[1]
        bpm = data[3] | ((data[2] & 64) << 1)
        spo2 = data[4]
        user_handler(pleth, bpm, spo2)
    return raw_handler

async def discover():
    devices = await bleak.discover()
    for d in devices:
        if d.name == "BerryMed" or d.address.startswith("00:A0:50"):
            return d

async def read_data(address, done, handler):
    async with bleak.BleakClient(address) as client:
        x = await client.is_connected()
        print("Connected: {0}".format(x))

        notification_handler = make_handler(handler)
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        await done.wait()
        print('Disconnecting ...')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--device", help="Device address")
    parser.add_argument("--multiline", help="Multiline data output", action="store_true")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()

    if not args.device:
        dev = loop.run_until_complete(discover())
        if dev is None:
            print("No device found")
            sys.exit(1)
        print("Found: {} ({})".format(dev.address, dev.name))
        address = dev.address
    else:
        address = args.device

    dp = DataPrinter()
    printer = dp.multiline if args.multiline else dp.oneline

    done = asyncio.Event()
    task = loop.create_task(read_data(address, done, printer))
    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        done.set()

    loop.run_until_complete(task)

if __name__ == "__main__":
    main()

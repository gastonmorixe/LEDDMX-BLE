import asyncio
from bleak import BleakScanner, BleakClient
# from bleak.backends.device import BLEDevice
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--status', choices=['on', 'off'], help='Turn on or off the command')
args = parser.parse_args()

# 2024-01-02 01:51:12,441 - INFO - >>> Connecting to LED Lamp: LEDDMX-00-0000 (E01D26BF-4364-FF2E-E41D-5E2EC36D44BC)
# 2024-01-02 01:51:12,552 - INFO - >>> Connecting to LED Lamp: LEDDMX-00-0000 (99C45940-4588-5668-9F4F-7006FFD7A10F)

# Constants for the LED lamp
LED_SERVICE_UUID = "FFB0"
TURN_OFF_COMMAND = bytearray.fromhex("7BFF0400FFFFFFFFBF")
TURN_ON_COMMAND =  bytearray.fromhex("7BFF0401FFFFFFFFBF")
# CHARACTERISTIC_HANDLE = 0x0003
SERVICE_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
KNOWN_DEVICE_ADDRESSES = [
    "99C45940-4588-5668-9F4F-7006FFD7A10F",
    "E01D26BF-4364-FF2E-E41D-5E2EC36D44BC",
    # "E01D26BF-4364-FF2E-E41D-AE2EC36D44BC",
    # "99C45940-4588-5668-9F4F-A006FFD7A10F",
]

async def connect_and_write(device, command):
    logging.debug("---------------------- #connect_and_write")
    logging.info(f">>> Connecting to LED Lamp: {device}")
    async with BleakClient(device, timeout=10.0) as client:
        logging.debug(f">>> Connected to client {client}")
        # await asyncio.wait_for(
        #     client.write_gatt_char(CHARACTERISTIC_UUID, command, response=False),
        #     timeout=30.0
        # )
        await client.write_gatt_char(CHARACTERISTIC_UUID, command, response=False)
        await asyncio.sleep(0.3)

async def fallback_discover(command):
    logging.debug("---------------------- #fallback_discover")
    # scanner = BleakScanner(service_uuids=[LED_SERVICE_UUID])
    # discovered_devices = await scanner.discover(timeout=10.0)
    discovered_devices = await BleakScanner.discover(service_uuids=[LED_SERVICE_UUID])
    if not discovered_devices:
        logging.info(">>> No additional LED lamps found.")
        return
    # Create tasks for newly discovered devices
    additional_tasks = [connect_and_write(discovered_device, command) for discovered_device in discovered_devices]
    await asyncio.gather(*additional_tasks)

async def main():
    command = TURN_OFF_COMMAND if args.status == 'off' else TURN_ON_COMMAND

    tasks = [connect_and_write(device, command) for device in KNOWN_DEVICE_ADDRESSES]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    if all(isinstance(result, Exception) for result in results):
        await asyncio.sleep(1.0)
        logging.error(f"Error connecting to device.... fallback")
        await fallback_discover(command)

asyncio.run(main())

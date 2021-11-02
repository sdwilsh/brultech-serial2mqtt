import asyncio

from brultech_serial2mqtt import BrultechSerial2MQTT

if __name__ == "__main__":
    bs2m = BrultechSerial2MQTT()
    asyncio.get_event_loop().run_until_complete(bs2m.start())
    asyncio.get_event_loop().run_forever()

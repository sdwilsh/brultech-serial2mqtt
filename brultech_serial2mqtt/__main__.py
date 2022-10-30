import asyncio

from brultech_serial2mqtt import BrultechSerial2MQTT

if __name__ == "__main__":
    bs2m = BrultechSerial2MQTT()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bs2m.start())
    loop.run_forever()

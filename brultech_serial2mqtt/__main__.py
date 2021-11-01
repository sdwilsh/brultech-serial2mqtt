import asyncio
import logging

from brultech_serial2mqtt import BrultechSerial2MQTT

logger = logging.getLogger("brultech_serial2mqtt")

if __name__ == "__main__":
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
        logging.Formatter("'%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(stream_handler)

    bs2m = BrultechSerial2MQTT()
    asyncio.get_event_loop().run_until_complete(bs2m.start())
    asyncio.get_event_loop().run_forever()

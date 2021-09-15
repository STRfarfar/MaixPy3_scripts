#!/usr/bin/env python

from evdev import InputDevice
import asyncio

packet = {
    'selected': "main",
    'status': 0
}

asyncio.set_event_loop(asyncio.new_event_loop())
keys = InputDevice('/dev/input/event0')

async def keys_events(packet, device):
    async for event in device.async_read_loop():
        if event.value == 1 and event.code == 0x02:  # 右键
            print("you push left!")
        elif event.value == 1 and event.code == 0x03:  # 左键
            print("you push right!")



for device in [keys]:
    asyncio.ensure_future(keys_events(packet, device))

async def main(packet):
    if packet["selected"] == "main":  # 分类
        print("hello:",packet["status"])
        packet["status"] += 1
        await asyncio.sleep(1)
    asyncio.ensure_future(main(packet))



if __name__ == "__main__":
    import signal
    def handle_signalm(signum,frame):
        print("father over")
        exit(0)
    signal.signal(signal.SIGINT,handle_signalm)    

    asyncio.ensure_future(main(packet))
    loop = asyncio.get_event_loop()
    loop.run_forever()

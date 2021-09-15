#!/usr/bin/env python3

from evdev import InputDevice
from select import select


keys = InputDevice('/dev/input/event0')

def key_select_sleep():
    r,w,x = select([keys], [], [])
    if r:
        for event in keys.read():
            if event.value == 1 and event.code == 0x02:     # 右键
                print("you push left!")
            elif event.value == 1 and event.code == 0x03:   # 左键
                print("you push left!")

def key_select_no_sleep():
    r,w,x = select([keys], [], [],0)
    if r:
        for event in keys.read():
            if event.value == 1 and event.code == 0x02:     # 右键
                print("you push left!")
            elif event.value == 1 and event.code == 0x03:   # 左键
                print("you push left!")


if __name__ == "__main__":
    import signal
    def handle_signalm(signum,frame):
        print("father over")
        exit(0)
    signal.signal(signal.SIGINT,handle_signalm)    
    while True:
        key_select_no_sleep()






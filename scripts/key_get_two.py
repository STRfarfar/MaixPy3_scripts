#!/usr/bin/env python
# MaixPy3读取读取按键信息同步版本
# 功能说明：读取按键事件
# 时间：2021年9月16日
# 作者：dianjixz
from evdev import InputDevice
from select import select


keys = InputDevice('/dev/input/event0')


def key_select_sleep():                 #阻塞读取案件事件
    r,w,x = select([keys], [], [])
    if r:
        for event in keys.read():
            if event.value == 1 and event.code == 0x02:     # 右键
                print("you push left!")
            elif event.value == 1 and event.code == 0x03:   # 左键
                print("you push right!")


def key_select_no_sleep():              #不阻塞读取案件事件
    r,w,x = select([keys], [], [],0)
    if r:
        for event in keys.read():
            if event.value == 1 and event.code == 0x02:     # 右键
                print("you push left!")
            elif event.value == 1 and event.code == 0x03:   # 左键
                print("you push right!")


if __name__ == "__main__":
    import signal
    def handle_signalm(signum,frame):
        print("father over")
        exit(0)
    signal.signal(signal.SIGINT,handle_signalm)    
    while True:
        key_select_no_sleep()






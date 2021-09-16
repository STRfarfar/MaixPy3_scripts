
#!/usr/bin/env python
# MaixPy3拍照保存脚本
# 功能说明：通过V831上的按键进行拍照
# 使用说明：按下一次右键拍一张图片,按着左键不松开,将会连续拍照.
# 时间：2021年9月16日
# 作者：dianjixz
from PIL import Image, ImageFont, ImageDraw
from maix import display,camera
import os
import time


class funation:
    keys = None
    mk = 0
    def __init__(self,device=None):
      self.event = self.run
      self.device = device
      self.font = ImageFont.truetype("/home/res/baars.ttf", 20, encoding="unic")
    def __del__(self):
      pass        
    def run(self):
        key_val = self.device.get_key()
        if key_val == 1:
            print("cap ones...",self.mk)
            self.mk += 1
            img = camera.capture()
            srcc = "/mnt/UDISK/" + str(int(time.time())) + str(self.mk) + ".jpg"
            img.save(srcc, quality=95)
            os.system("sync")
            time.sleep(0.05)
        elif key_val == 3:
            print("cap ones...",self.mk)
            self.mk += 1
            img = camera.capture()
            srcc = "/mnt/UDISK/" + str(int(time.time())) + str(self.mk) + ".jpg"
            img.save(srcc, quality=95)
            os.system("sync")
            time.sleep(0.05)
        else:
            img = camera.read()
        draw = display.get_draw()
        draw.text((10, 10), "push left ,get one", (255, 0, 0), self.font)  # bgr
        draw.text((10, 30), "push right aways,aways get", (255, 0, 0), self.font)  # bgr
        draw.text((10, 50), "you get pic:{}".format(self.mk), (255, 0, 0), self.font)  # bgr
        display.show()


if __name__ == "__main__":
    import signal
    def handle_signal_z(signum,frame):
        print("erzi over")
        exit(0)
    signal.signal(signal.SIGINT,handle_signal_z)
    camera.config(size=(640,480))
    from evdev import InputDevice
    from select import select
    class devices:
        def __init__(self):
            self.keys = InputDevice('/dev/input/event0')
        def get_key(self):
            r,w,x = select([self.keys], [], [],0)
            if r:
                for event in self.keys.read(): 
                    if event.value == 1 and event.code == 0x02:     # 右键
                        return 1
                    elif event.value == 1 and event.code == 0x03:   # 左键
                        return 2
                    elif event.value == 2 and event.code == 0x03:   # 左键连按
                        return 3
    dev = devices()
    start = funation(dev)
    while True:
        start.event()




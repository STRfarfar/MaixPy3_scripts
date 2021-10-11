
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
import key_get_two as key


class funation:
    pic_number = 0
    def __init__(self,device=None):
      self.event = self.run                                                                 #定义统一调用接口,相当于函数指针           
      self.font = ImageFont.truetype("/home/res/baars.ttf", 20, encoding="unic")
      self.keys = InputDevice('/dev/input/event0')                                          #打开按键设备
    def __del__(self):
      pass        
    def run(self):
        key_val = key.key_select_no_sleep()
        if key_val == 1:
            print("cap ones...",self.pic_number)
            self.pic_number += 1
            img = camera.capture()
            srcc = "/mnt/UDISK/" + str(int(time.time())) + str(self.pic_number) + ".jpg"
            img.save(srcc, quality=95)
            os.system("sync")
            time.sleep(0.05)
        elif key_val == 3:
            print("cap ones...",self.pic_number)
            self.pic_number += 1
            img = camera.capture()
            srcc = "/mnt/UDISK/" + str(int(time.time())) + str(self.pic_number) + ".jpg"
            img.save(srcc, quality=95)
            os.system("sync")
            time.sleep(0.05)
        else:
            img = camera.read()
        draw = display.get_draw()
        draw.text((10, 10), "push left ,get one", (255, 0, 0), self.font)  # bgr
        draw.text((10, 30), "push right aways,aways get", (255, 0, 0), self.font)  # bgr
        draw.text((10, 50), "you get pic:{}".format(self.pic_number), (255, 0, 0), self.font)  # bgr
        display.show()


if __name__ == "__main__":
    import signal
    def handle_signal_z(signum,frame):
        print("APP OVER")
        exit(0)
    signal.signal(signal.SIGINT,handle_signal_z)
    camera.config(size=(640,480))                   #设置照片大小
    start = funation()
    while True:
        start.event()




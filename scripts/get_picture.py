
#!/usr/bin/env python

from PIL import Image, ImageFont, ImageDraw
from maix import display,camera
from evdev import InputDevice
from select import select
import time
from maix import display
class funation:
    keys = None
    mk = 0
    def __init__(self):
        camera.config(size=(640,480))
        self.keys = InputDevice('/dev/input/event0')
        self.font = ImageFont.truetype("/home/res/baars.ttf", 20, encoding="unic")
    def run(self):
        r,w,x = select([self.keys], [], [],0)
        if r:
            for event in self.keys.read(): 
                if event.value == 1 and event.code == 0x02:     # 右键
                    print("cap ones...",self.mk)
                    self.mk += 1
                    img = camera.capture()
                    srcc = "/mnt/UDISK/" + str(int(time.time())) + str(self.mk) + ".jpg"
                    img.save(srcc, quality=95)
                    time.sleep(0.05)
                elif event.value == 1 and event.code == 0x03:   # 左键
                    pass
                elif event.value == 2 and event.code == 0x03:   # 左键连按
                    print("cap ones...",self.mk)
                    self.mk += 1
                    img = camera.capture()
                    srcc = "/mnt/UDISK/" + str(int(time.time())) + str(self.mk) + ".jpg"
                    img.save(srcc, quality=95)
                    time.sleep(0.05)
        else:
            img = camera.read()
            draw = display.get_draw()
            draw.text((10, 10), "push left ,get one", (255, 0, 0), self.font)  # bgr
            draw.text((30, 10), "push right aways,aways get", (255, 0, 0), self.font)  # bgr
            display.show()



if __name__ == "__main__":
    import signal
    def handle_signalm(signum,frame):
        print("father over")
        exit(0)
    signal.signal(signal.SIGINT,handle_signalm)
    start = funation()
    while True:
        start.run()




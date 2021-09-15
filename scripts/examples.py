#!/usr/bin/env python3
import os
import sys
import importlib
from evdev import InputDevice
from select import select
from PIL import Image, ImageFont, ImageDraw
from maix import display
import gc
from maix import camera
camera.config(size=(224,224))
# tmp = camera.read()
class_lable = ["find_blob_lab","find_ball","find_face","find_line","find_magic","find_qr","get_blob_hsv","play_mp4","resnet","self_learn_classifier","self_learn_save_load"]
class SMART:
    modules_name = []
    keys = None
    status_old = None
    status = "default"
    fun_status = 0
    def __init__(self):
        font = ImageFont.truetype("./res/baars.ttf", 20, encoding="unic")
        canvas = Image.new("RGB", (240, 240), "#2c3e50")
        with Image.open('./res/logo.png') as logo:
            canvas.paste(logo, (50, 40, 50 + logo.size[0], 40 + logo.size[1]), logo)
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 195), u'MaixPy.Sipeed.COM', "#bdc3c7", font)
        draw.text((0, 0), u'<exit', "#7f8c8d", font)
        draw.text((160, 0), u'demo> ', "#16a085", font)
        display.show(canvas)
        del draw
        del canvas
        del font
        self.keys = InputDevice('/dev/input/event0')
    def default(self):
        r,w,x = select([self.keys], [], [])
        if r:
            for event in self.keys.read():
                if event.value == 1 and event.code == 0x02:     # 右键
                    self.status = "fun_choose"
                elif event.value == 1 and event.code == 0x03:   # 左键
                    canvas = Image.new("RGB", (240, 240), "#2c3e50")
                    display.show(canvas)
                    exit(0)
    def fun_choose(self):
        self.fun_status = 0
        font = ImageFont.truetype("./res/baars.ttf", 20, encoding="unic")
        canvas = Image.new("RGB", (240, 240), "#2c3e50")
        with Image.open('./res/logo.png') as logo:
                canvas.paste(logo, (50, 40, 50 + logo.size[0], 40 + logo.size[1]), logo)
        draw = ImageDraw.Draw(canvas)
        draw.text((0, 0),"next", "#bdc3c7", font)
        draw.text((190, 0),"enter", "#bdc3c7", font)
        draw.text((80, 5),class_lable[self.fun_status], "#bdc3c7", font)
        display.show(canvas)
        r,w,x = select([self.keys], [], [], 0)
        if r:
            for event in self.keys.read():
                pass
        while True:
            r,w,x = select([self.keys], [], [])
            if r:
                for event in self.keys.read():
                    if event.value == 1 and event.code == 0x02:     # 右键
                        if self.fun_status >= len(class_lable):
                            self.status = "default"
                        else:
                            self.status = "fun_run"
                        del draw
                        del canvas
                        del font
                        gc.collect()
                        return

                    elif event.value == 1 and event.code == 0x03:   # 左键
                        if self.fun_status >= len(class_lable):
                            self.fun_status = 0
                        else:
                            self.fun_status += 1
                        canvas = Image.new("RGB", (240, 240), "#2c3e50")
                        with Image.open('./res/logo.png') as logo:
                            canvas.paste(logo, (50, 40, 50 + logo.size[0], 40 + logo.size[1]), logo)
                        draw = ImageDraw.Draw(canvas)
                        draw.text((0, 0),"next", "#bdc3c7", font)
                        draw.text((190, 0),"enter", "#bdc3c7", font)
                        if self.fun_status >= len(class_lable):
                            draw.text((80, 5),'exit', "#bdc3c7", font)
                            display.show(canvas)
                        else:
                            draw.text((80, 5),class_lable[self.fun_status], "#bdc3c7", font)
                            display.show(canvas)
    def fun_run(self): 
        num_times = 0
        print(class_lable[self.fun_status],"----------")
        fun_moudle = importlib.import_module(class_lable[self.fun_status])
        startxx = fun_moudle.funation()
        key_val = 0
        while True:
            r,w,x = select([self.keys], [], [],0)
            if r:
                for event in self.keys.read():
                    if event.value == 2 and event.code == 0x03:   # 左键连按
                        num_times += 1
                        if num_times == 10:
                            self.status = "default"
                            # del sys.modules[class_lable[self.fun_status]]
                            # del locals()[class_lable[self.fun_status]]
                            gc.collect()
                            return
                    elif event.value == 1 and event.code == 0x03:   # 左键
                        key_val = 2
                    elif event.value == 1 and event.code == 0x02:     # 右键
                        key_val = 1
            else:
                startxx.run(key_val)
                key_val = 0


    def switch(self):
        if self.status == "default":
            font = ImageFont.truetype("./res/baars.ttf", 20, encoding="unic")
            canvas = Image.new("RGB", (240, 240), "#2c3e50")
            with Image.open('./res/logo.png') as logo:
                canvas.paste(logo, (50, 40, 50 + logo.size[0], 40 + logo.size[1]), logo)
            draw = ImageDraw.Draw(canvas)
            draw.text((10, 195), u'MaixPy.Sipeed.COM', "#bdc3c7", font)
            draw.text((0, 0), u'<exit', "#7f8c8d", font)
            draw.text((160, 0), u'demo> ', "#16a085", font)
            display.show(canvas)
            del draw
            del canvas
            del font
            gc.collect()
        self.status_old = self.status

smart = SMART()
funation = {
    "default":smart.default,
    "fun_choose":smart.fun_choose,
    "fun_run":smart.fun_run
}

if __name__ == "__main__":
    import signal
    def handle_signalm(signum,frame):
        print("father over")
        exit(0)
    signal.signal(signal.SIGINT,handle_signalm)    
    while True:
        if(smart.status_old != smart.status):
            smart.switch() 
        funation[smart.status]()






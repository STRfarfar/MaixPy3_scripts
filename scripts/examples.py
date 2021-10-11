#!/usr/bin/env python
# MaixPy3调用示例脚本
# 功能说明：统一调用示例,做示例调用
# 时间：2021年9月17日
# 作者：dianjixz
import os
import sys
import importlib
from PIL import Image, ImageFont, ImageDraw
from maix import display
import gc
from maix import camera
import key_get_two as key


class DEVICES:  
    funaction_status = 0


class EXAMPLES_FUN:
    class_lable = {"find_blob" : "maix_cv_find_blob",\
                    "find_ball": "maix_cv_find_ball",\
                    "find_face": "nn_find_face",\
                    "find_line": "maix_cv_find_line",\
                    "find_magic": "maix_cv_find_magic",\
                    "find_qr": "zbarlight_find_qr",\
                    "play_mp4": "play_mp4",\
                    "resnet": "nn_resnet",\
                    "learn_classifier": "nn_self_learn_classifier",\
                    "learn_save_load": "nn_self_learn_save_load",\
                    "face_recognition":"nn_face_recognition"\
    }
    def __init__(self):
        camera.config(size=(224,224))
        self.font = ImageFont.truetype("./res/baars.ttf", 20, encoding="unic")
        self.start_logo()
        self.device = DEVICES()
        self.event = self.default
    def __del__(self):
        pass
    def start_logo(self):
        canvas = Image.new("RGB", (240, 240), "#2c3e50")
        with Image.open('./res/logo.png') as logo:
            canvas.paste(logo, (50, 40, 50 + logo.size[0], 40 + logo.size[1]), logo)
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 195), u'MaixPy.Sipeed.COM', "#bdc3c7", self.font)
        draw.text((0, 0), u'<exit', "#7f8c8d", self.font)
        draw.text((160, 0), u'demo> ', "#16a085", self.font)
        display.show(canvas)
    def default(self):
        canvas = Image.new("RGB", (240, 240), "#2c3e50")
        with Image.open('./res/logo.png') as logo:
            canvas.paste(logo, (50, 40, 50 + logo.size[0], 40 + logo.size[1]), logo)
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 195), u'MaixPy.Sipeed.COM', "#bdc3c7", self.font)
        draw.text((0, 0), u'<exit', "#7f8c8d", self.font)
        draw.text((160, 0), u'demo> ', "#16a085", self.font)
        display.show(canvas)
        gc.collect()
        key_val = key.key_select_no_sleep()
        if key_val == 1:
            self.event = self.fun_choose
        elif key_val == 2:
            canvas = Image.new("RGB", (240, 240), "#2c3e50")
            display.show(canvas)
            os.system("sleep 3 && killall python &")
            print("examples exit ...")
            exit(0)
    def fun_choose(self):
        self.fun_status = 0
        font = ImageFont.truetype("./res/baars.ttf", 20, encoding="unic")
        canvas = Image.new("RGB", (240, 240), "#2c3e50")
        with Image.open('./res/logo.png') as logo:
                canvas.paste(logo, (50, 40, 50 + logo.size[0], 40 + logo.size[1]), logo)
        draw = ImageDraw.Draw(canvas)
        draw.text((0, 0),"next", "#bdc3c7", self.font)
        draw.text((190, 0),"enter", "#bdc3c7", self.font)
        draw.text((60, 5),list(self.class_lable)[self.fun_status], "#bdc3c7", self.font)
        display.show(canvas)
        while True:
            key_val = key.key_select_no_sleep()
            if key_val == 1:     # 右键
                if self.fun_status == len(self.class_lable):
                    self.event = self.default
                else:
                    self.event = self.fun_run
                    self.device.funaction_status = 1
                return
            elif key_val == 2:   # 左键
                if self.fun_status == len(self.class_lable):
                    self.fun_status = 0
                else:
                    self.fun_status += 1
                canvas = Image.new("RGB", (240, 240), "#2c3e50")
                with Image.open('./res/logo.png') as logo:
                    canvas.paste(logo, (50, 40, 50 + logo.size[0], 40 + logo.size[1]), logo)
                draw = ImageDraw.Draw(canvas)
                draw.text((0, 0),"next", "#bdc3c7", self.font)
                draw.text((190, 0),"enter", "#bdc3c7", self.font)
                if self.fun_status >= len(self.class_lable):
                    draw.text((80, 5),'exit', "#bdc3c7", self.font)
                else:
                    draw.text((60, 5),list(self.class_lable)[self.fun_status], "#bdc3c7", self.font)
                display.show(canvas)
    def fun_run(self): 
        num_times = 0
        print(self.class_lable[list(self.class_lable)[self.fun_status]],"----------")
        fun_moudle = importlib.import_module(self.class_lable[list(self.class_lable)[self.fun_status]])
        startxx = fun_moudle.funation(self.device)
        while True:
            if self.get_key() == 3:
                num_times += 1
                if num_times > 15:
                    self.device.funaction_status = -1
                    del startxx
                    self.event = self.default
                    return 
            startxx.event()


if __name__ == "__main__":
    import signal
    def handle_signalm(signum,frame):
        print("APP OVER")
        exit(0)
    signal.signal(signal.SIGINT,handle_signalm)    
    funation = EXAMPLES_FUN()
    while True:
        funation.event()



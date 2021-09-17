#!/usr/bin/python3
# MaixPy3自学习脚本二
# 功能说明：将自学习脚本一中保存的特征文件加载到环境中，继续预测物体类别
# 时间：2021年9月15日
# 作者：Neutree dianjixz

from maix import nn
from PIL import Image, ImageFont, ImageDraw
from maix import camera, display
import time
from maix.nn.app.classifier import Classifier
from maix.nn.app.classifier import load
from evdev import InputDevice
from select import select
import threading


class funation:
    model = {
        "param": "./res/resnet.param",
        "bin": "./res/resnet.bin"
    }
    options = {
        "model_type":  "awnn",
        "inputs": {
            "input0": (224, 224, 3)
        },
        "outputs": {
            "190": (1, 1, 512)      # "190": (1, 1, 1000)
        },
        "mean": [127.5, 127.5, 127.5],
        "norm": [0.0176, 0.0176, 0.0176],
    }
    fun_status = 0
    def __init__(self,device=None):
        self.fun = [self.wait_run,self.run,self.err]
        self.event = self.fun[self.fun_status]
        threading.Thread(target=self.load_mode).start()
        self.font = ImageFont.truetype("./res/baars.ttf",20, encoding="unic")
    def __del__(self):
        if self.fun_status != 2:
            del self.classifier
            del self.m
            print("nn self learn save load  exit!")
        else:
            print("nn self learn save load  exit!")
    def load_mode(self):
        import os.path
        if os.path.isfile("./module.bin"):
            print("-- load model:", self.model)
            self.m = nn.load(self.model, opt=self.options)
            print("-- load ok")
            print("-- load classifier")
            self.classifier = load(self.m,"./module.bin")
            print("-- load ok")
            self.fun_status += 1
            self.event = self.fun[self.fun_status]
        else:
            self.fun_status = 2
            self.event = self.fun[self.fun_status]
    def err(self):
        tmp = camera.read(video_num = 1)
        draw = display.get_draw()
        draw.text((10, 10), "no classifier,", (255, 0, 0), self.font)  
        draw.text((10, 30), "please run self learn,", (255, 0, 0), self.font)  
        display.show()
        print("no classifier,please run self learn")
    def wait_run(self):
        tmp = camera.read(video_num = 1)
        display.show()
    def run(self):
        img = camera.read(video_num = 1)
        if not img:
            time.sleep(0.02)
            return
        idx, distance = self.classifier.predict(img)
        msg = "predict class: " + str(idx+1) + ", conf: " + str(100-distance)
        draw = display.get_draw()
        draw.text((10, 10), msg, (255, 0, 0), self.font)  
        print("predict class: {}, distance: {}".format(idx, distance))
        display.show()


if __name__ == "__main__":
    import signal
    def handle_signal_z(signum,frame):
        print("erzi over")
        exit(0)
    signal.signal(signal.SIGINT,handle_signal_z)
    camera.config(size=(224,224))
    start = funation()
    while True:
        start.event()















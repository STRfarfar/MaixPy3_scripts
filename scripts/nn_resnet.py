#!/usr/bin/python3
# 分类例程
# 用于物体分类
# 时间:2021年9月16日
# 作者：Neutree dianjixz
from maix import nn
from PIL import Image, ImageFont, ImageDraw
from maix import display
import time
from maix import camera
import threading
try:
    from classes_label import labels
except:
    import os
    os.system("cp ./res/classes_label.py ./")
    from classes_label import labels

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
            "output0": (1, 1, 1000)
        },
        "first_layer_conv_no_pad": False,
        "mean": [127.5, 127.5, 127.5],
        "norm": [0.00784313725490196, 0.00784313725490196, 0.00784313725490196],
    }
    fun_status = 0
    def __init__(self,device=None):
        self.fun = [self.wait_run,self.run]
        self.event = self.fun[self.fun_status]
        self.font = ImageFont.truetype("./res/baars.ttf",30, encoding="unic")
        threading.Thread(target=self.load_mode).start()
        print("resnet start!")
    def __del__(self):
        del self.m
        print("resent exit")
    def load_mode(self):
        print("-- load model:", self.model)
        self.m = nn.load(self.model, opt=self.options)
        print("-- load ok")
        self.fun_status += 1
        self.event = self.fun[self.fun_status]
    def wait_run(self):
        tmp = camera.read(video_num = 1)
        display.show()
    def run(self):
        img = camera.read(video_num = 1)
        t = time.time()
        out = self.m.forward(img, quantize=True)
        t = time.time() - t
        print("-- forward time: {}s".format(t))
        t = time.time()
        out2 = nn.F.softmax(out)
        t = time.time() - t
        print("-- softmax time: {}s".format(t))
        msg = "{:.2f}: {}".format(out.max(), labels[out.argmax()])
        print(msg)
        draw = display.get_draw()
        draw.text((0, 0), msg, (255, 0, 0), self.font)
        display.show()


if __name__ == "__main__":
    import signal
    def handle_signal_z(signum,frame):
        print("APP OVER")
        exit(0)
    signal.signal(signal.SIGINT,handle_signal_z)
    camera.config(size=(224,224))
    start = funation()
    while True:
        start.event()
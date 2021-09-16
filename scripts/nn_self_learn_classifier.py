#!/usr/bin/python3
# MaixPy3自学习脚本一
# 功能说明：通过V831上的按键控制学习物体，并保存特征文件
# 使用说明：开机后，前三次每次按下一次右键拍照保存一张图片到算法中，保存三个类别后，再按右键拍照则进行添加相似图片，
# 相似图片添加15张。添加完成后将会自动进行训练。训练结束后会进入预测阶段。程序会打印出算法结果
# 按下左键将会保存模型到本地文件。
# 时间：2021年9月15日
# 作者：Neutree dianjixz
from maix import nn
from PIL import Image, ImageFont, ImageDraw
from maix import camera, display
import time
from maix.nn.app.classifier import Classifier
from evdev import InputDevice
from select import select
import threading
from evdev import InputDevice
from select import select


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
            "190": (1, 1, 512)
        },
        "mean": [127.5, 127.5, 127.5],
        "norm": [0.0176, 0.0176, 0.0176],
    }
    class_num = 3
    sample_num = 15
    curr_class = 0
    curr_sample = 0
    fun_status = 0
    def __init__(self,device=None):
        self.device = device
        self.keys = InputDevice('/dev/input/event0')
        threading.Thread(target=self.load_mode).start()
        self.fun = [self.wait_run,self.train,self.predict]
        self.event = self.fun[self.fun_status]   
        self.font = ImageFont.truetype("./res/baars.ttf",20, encoding="unic")     
    def __del__(self):
        del self.classifier
        del self.m
        print("-- del model")
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
    def load_mode(self):
        print("-- load model:", self.model)
        self.m = nn.load(self.model, opt=self.options)
        print("-- load ok")
        print("-- load classifier")
        self.classifier = Classifier(self.m, self.class_num, self.sample_num, 512, 224, 224)
        print("-- load ok")
        self.fun_status += 1
        self.event = self.fun[self.fun_status]
    def wait_run(self):
        tmp = camera.read(video_num = 1)
        display.show()
    def train(self):
        img = camera.read(video_num = 1)
        if not img:
            time.sleep(0.02)
            return
        key = self.get_key()
        draw = display.get_draw()
        if self.curr_class < self.class_num:
            if key == 1:
                print("add class")
                self.classifier.add_class_img(img)
                self.curr_class += 1
            draw.text((10, 10), "please add class", (255, 0, 0), self.font) 
            draw.text((10, 30), "{} object".format(self.curr_class+1), (255, 0, 0), self.font) 
        elif self.curr_sample < self.sample_num:
            if key == 1:
                print("add sample")
                self.classifier.add_sample_img(img)
                self.curr_sample += 1
                if self.curr_sample == self.sample_num:
                    draw.text((10, 10), "train ...", (255, 0, 0), self.font) 
                    print("train ...")
                    self.classifier.train()
                    self.status = 1
                    print("train end ...")
                    self.fun_status += 1
                    self.event = self.fun[self.fun_status]
                    self.classifier.save("./module.bin")
                    print("save success!")
            draw.text((10, 0), "add Sample:{}".format(self.curr_sample), (255, 0, 0), self.font)
        display.show()
            

    def predict(self):
        img = camera.read(video_num = 1)
        idx, distance = self.classifier.predict(img)
        msg = "predict class: " + str(idx+1) + ", conf: " + str(100-distance)
        print(msg)
        draw = display.get_draw()
        draw.text((10, 10), msg, (255, 0, 0), self.font)  
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















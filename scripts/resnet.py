#!/usr/bin/python3
#在v831运行的1000分类代码
# from maix import nn
from maix import nn
from PIL import Image, ImageFont, ImageDraw
from maix import display
from classes_label import labels
import time
from maix import camera

class funation:
    model = None
    options = None
    m = None
    font = None
    def __init__(self):
        camera.config(size=(224, 224))
        self.model = {
            "param": "./res/resnet.param",
            "bin": "./res/resnet.bin"
        }
        self.options = {
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
        print("-- load model:", self.model)
        self.m = nn.load(self.model, opt=self.options)
        print("-- load ok")
        self.font = ImageFont.truetype("./res/baars.ttf",30, encoding="unic")

    def run(self):
        img = camera.capture()
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
        print("erzi over")
        exit(0)
    signal.signal(signal.SIGINT,handle_signal_z)
    start = funation()
    while True:
        start.run()
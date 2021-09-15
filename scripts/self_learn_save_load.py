# MaixPy3自学习脚本二
# 功能说明：将自学习脚本一中保存的特征文件加载到环境中，继续预测物体类别
# 时间：2021年9月15日
# 作者：Neutree dianjixz

from maix import nn
from PIL import Image, ImageDraw
from maix import camera, display
import time
from maix.nn.app.classifier import Classifier
from maix.nn.app.classifier import load
from evdev import InputDevice
from select import select


class funation:
    def __init__(self):
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
        print("-- load model:", model)
        self.m = nn.load(model, opt=options)
        print("-- load ok")
        camera.config(size=(224, 224))
        print("-- load classifier")
        self.classifier = load(self.m,"./module.bin")
        print("-- load ok")
    def run(self):
        img = camera.capture()
        if not img:
            time.sleep(0.02)
            return
        idx, distance = self.classifier.predict(img)
        print("predict class: {}, distance: {}".format(idx, distance))


if __name__ == "__main__":
    import signal
    def handle_signal_z(signum,frame):
        print("erzi over")
        exit(0)
    signal.signal(signal.SIGINT,handle_signal_z)
    start = funation()
    while True:
        start.run()















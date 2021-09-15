from maix import nn
from PIL import Image, ImageDraw
from maix import camera, display
import time
from maix.nn.app.classifier import Classifier
from maix.nn.app.classifier import load
from evdev import InputDevice
from select import select


class funation:
    class_num = 3
    sample_num = 15
    curr_class = 0
    curr_sample = 0
    status = 0
    def __init__(self):
        feature_len = 512
        input_w = 224
        input_h = 224
        model = {
            "param": "./res/resnet.param",
            "bin": "./res/resnet.bin"
        }

        options = {
            "model_type":  "awnn",
            "inputs": {
                "input0": (input_w, input_h, 3)
            },
            "outputs": {
                "190": (1, 1, feature_len)
            },
            "mean": [127.5, 127.5, 127.5],
            "norm": [0.0176, 0.0176, 0.0176],
        }


        print("-- load model:", model)
        self.m = nn.load(model, opt=options)
        print("-- load ok")
        camera.config(size=(224, 224))
        # self.classifier = Classifier(self.m, self.class_num, self.sample_num, feature_len, input_w, input_h)
        print("-- load model two:")
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















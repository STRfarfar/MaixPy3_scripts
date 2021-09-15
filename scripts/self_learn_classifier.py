from maix import nn
from PIL import Image, ImageDraw
from maix import camera, display
import time
from maix.nn.app.classifier import Classifier
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
        self.keys = InputDevice('/dev/input/event0')

        print("-- load model:", model)
        self.m = nn.load(model, opt=options)
        print("-- load ok")
        camera.config(size=(224, 224))
        self.classifier = Classifier(self.m, self.class_num, self.sample_num, feature_len, input_w, input_h)
    def __exit__(self):
        del self.classifier
        del self.m



    def key_pressed(self):
        # TODO: is button pressed
        r,w,x = select([self.keys], [], [],0)
        if r:
            for event in self.keys.read():
                if event.value == 1 and event.code == 0x02:     # 右键
                    return 1
                elif event.value == 1 and event.code == 0x03:   # 左键
                    return 2
            return 0
        return 0

    def run(self):
        img = camera.capture()
        if not img:
            time.sleep(0.02)
            return
        key_val = self.key_pressed()
        if key_val == 1:
            if self.curr_class < self.class_num:
                print("add class")
                self.classifier.add_class_img(img)
                self.curr_class += 1
            elif self.curr_sample < self.sample_num:
                print("add sample")
                self.classifier.add_sample_img(img)
                self.curr_sample += 1
                if self.curr_sample == self.sample_num:
                    print("train ...")
                    self.classifier.train()
                    self.status = 1
                    print("train end ...")
        elif key_val == 2:
            self.classifier.save("./module.bin")
            print("save success!")
            time.sleep(3)
        if self.status:
            idx, distance = self.classifier.predict(img)
            print("predict class: {}, distance: {}".format(idx, distance))


if __name__ == "__main__":
    start = funation()
    import signal
    def handle_signal_z(signum,frame):
        print("erzi over")
        exit(0)
    signal.signal(signal.SIGINT,handle_signal_z)
    
    while True:
        start.run()















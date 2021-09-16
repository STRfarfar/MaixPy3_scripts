#!/usr/bin/env python
# 人脸检测例程
# 用于人脸检测
# 时间:2021年9月16日
# 作者：Neutree dianjixz
from maix import nn
from maix.nn import decoder
from maix import display, camera
from maix.nn import decoder
from PIL import Image, ImageFont, ImageDraw
import time
import threading

class funation:
    labels = ["person"]
    anchors = [1.19, 1.98, 2.79, 4.59, 4.53, 8.92, 8.06, 5.29, 10.32, 10.65]
    model = {
        "param": "/home/res/yolo2_face_int8.param",
        "bin": "/home/res/yolo2_face_int8.bin"
    }
    options = {
        "model_type":  "awnn",
        "inputs": {
            "input0": (224, 224, 3)
        },
        "outputs": {
            "output0": (7, 7, (1+4+1)*5)
        },
        "mean": [127.5, 127.5, 127.5],
        "norm": [0.0078125, 0.0078125, 0.0078125],
    }
    fun_status = 0
    def __init__(self,device=None):
        self.fun = [self.wait_run,self.run]
        self.event = self.fun[self.fun_status]
        threading.Thread(target=self.load_mode).start()
        print("face start!")
    def __del__(self):
        del self.m
        del self.yolo2_decoder
        print("face exit")
    def load_mode(self):
        self.m = nn.load(self.model, opt=self.options)
        self.yolo2_decoder = decoder.Yolo2(len(self.labels), self.anchors, net_in_size=(224, 224), net_out_size=(7, 7))
        self.fun_status += 1
        self.event = self.fun[self.fun_status]
    def map_face(self,x,y,w,h):
        rx = int(x/224*240)
        ry = int(y/224*240)
        rw = int(w/224*240)
        rh = int(h/224*240)
        return rx,ry,rw,rh
    def draw_rectangle_with_title(self,draw, box, disp_str, bg_color=(255, 0, 0), font_color=(255, 255, 255)):
        font = ImageFont.load_default()
        font_w, font_h = font.getsize(disp_str)
        x,y,w,h = self.map_face(box[0],box[1],box[2],box[3])
        draw.rectangle((x, y, x+w, y+h), fill=None, outline=bg_color, width=2)
        draw.rectangle((x, y - font_h, x + font_w, y), fill=bg_color)
        draw.text((x, y - font_h), disp_str, fill=font_color, font=font)
    def wait_run(self):
        img = camera.read(video_num = 1)
        display.show()
    def run(self):
        img = camera.read(video_num = 1)
        t = time.time()
        out = self.m.forward(img, quantize=True, layout="hwc")
        print("-- forward: ", time.time() - t )
        t = time.time()
        boxes, probs = self.yolo2_decoder.run(out, nms=0.3, threshold=0.5, img_size=(224, 224))
        print("-- decode: ", time.time() - t )
        print(len(boxes))
        draw = display.get_draw()
        if len(boxes):
            for i, box in enumerate(boxes):
                class_id = probs[i][0]
                prob = probs[i][1][class_id]
                disp_str = "{}:{:.2f}%".format(self.labels[class_id], prob*100)
                self.draw_rectangle_with_title(draw, box, disp_str)
            display.show()
        else:
            display.show()


if __name__ == "__main__":
    import signal
    def handle_signal_z(signum,frame):
        print("erzi over")
        exit(0)
    signal.signal(signal.SIGINT,handle_signal_z)
    camera.config(size=(224, 224))
    start = funation()
    while True:
        start.event()
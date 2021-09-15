#!/usr/bin/env python
from _maix_opencv import _v83x_opencv
from maix import camera
from PIL import Image, ImageDraw
from maix import display
import time
cv = _v83x_opencv()
class funation:

    m_gree = [(46,-64,16,79,-34,49)]
    m_yellow = [(56,-32,37,99,-7,96)]
    m_blue = [(13,6,-77,40,42,-35)]
    m_cheng = [(23,26,43,82,78,71)]
    m_sred = [(17,27,-10,40,61,41)]
    m_white = [(49,-13,-46,100,19,3)]
    thr = [m_gree,m_yellow,m_blue,m_cheng,m_sred,m_white]
    color_list = ["red", "yellow", "green", "blue", "white", "black"]

    def run(self):
        ma = []
        for i in range(3):
            tmp = camera.read()
            ma.append(cv.find_blob_lab(tmp, self.thr[2 * i]))
            ma.append(cv.find_blob_lab(tmp, self.thr[2 * i + 1]))
        # print(ma)
        draw = display.get_draw()
        for idx, blob in enumerate(ma):
            if blob:
                for b in blob:
                    if b["pixels"] > 100 and b["pixels"] < 4000:
                        draw.rectangle((b["x"], b["y"], b["x"] + b["w"], b["y"] + b["h"]), outline=self.color_list[idx], width=1)
        display.show()
if __name__ == "__main__":
    import signal
    def handle_signalm(signum,frame):
        print("father over")
        exit(0)
    signal.signal(signal.SIGINT,handle_signalm)
    start = funation()
    while True:
        start.run()

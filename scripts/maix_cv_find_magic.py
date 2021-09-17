#!/usr/bin/env python
# MaixPy3魔方面颜色图案获取示例
# 功能说明：获取魔方面颜色图案信息
# 时间：2021年9月16日
# 作者：dianjixz
from maix import camera
from PIL import Image, ImageDraw
from maix import display
import time
try:
  from maix import maix_cv
except:
  from _maix_opencv import _v83x_opencv
  maix_cv = _v83x_opencv()


class funation:
    m_gree = [(46,-64,16,79,-34,49)]
    m_yellow = [(56,-32,37,99,-7,96)]
    m_blue = [(13,6,-77,40,42,-35)]
    m_cheng = [(23,26,43,82,78,71)]
    m_sred = [(17,27,-10,40,61,41)]
    m_white = [(49,-13,-46,100,19,3)]
    thr = [m_gree,m_yellow,m_blue,m_cheng,m_sred,m_white]
    color_list = ["green", "yellow", "blue", "blue", "black", "white"]
    def __init__(self,device=None):
      self.event = self.run
    def __del__(self):
      pass
    def run(self):
        ma = []
        for i in range(3):
            tmp = camera.read(video_num = 0)
            ma.append(maix_cv.find_blob_lab(tmp, self.thr[2 * i]))
            ma.append(maix_cv.find_blob_lab(tmp, self.thr[2 * i + 1]))
        draw = display.get_draw()
        for idx, blob in enumerate(ma):
            if blob:
                for b in blob:
                    if b["pixels"] > 100 and b["pixels"] < 4000:
                        draw.rectangle((b["x"], b["y"], b["x"] + b["w"], b["y"] + b["h"]), outline=self.color_list[idx], width=1)
        display.show()


if __name__ == "__main__":
    import signal
    def handle_signal_z(signum,frame):
        print("erzi over")
        exit(0)
    signal.signal(signal.SIGINT,handle_signal_z)
    camera.config(size=(240,240))
    start = funation()
    while True:
        start.event()

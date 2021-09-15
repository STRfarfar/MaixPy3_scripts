#!/usr/bin/env python

# cv.find_line(pic)函数说明
# 功能:在道路图片pic中寻找线
# 输入：pic，240*240尺寸的图片bytes数据
# 返回值：字典类型，rect：矩形的四个顶点，pixels：矩形的面积，cx、cy:矩形的中心坐标，rotation：矩形的倾斜角
#{'rect': [9, 229, 9, 9, 145, 9, 145, 229], 'pixels': 12959, 'cx': 77, 'cy': 119, 'rotation': -1.570796251296997}

from maix import camera
from _maix_opencv import _v83x_opencv
from PIL import Image ,ImageDraw
from maix import display
cv = _v83x_opencv()
import time

class funation:
    red_hsv   = (176,76,0,255,255,255)
    green_hsv = (72,92,62,93,255,255) 
    blue_hsv  = (95,219,0,255,255,255)
    yello_hsv = (18,122,176,33,255,255)
    def __init__(self):
      #跳过一些帧
      tmp = camera.read()
      tmp = camera.read()
      tmp = camera.read()
      tmp = camera.read()
      tmp = camera.read()
      tmp = camera.read()
      tmp = camera.read()
      tmp = camera.read()
      tmp = camera.read()
      del tmp
    def run(self):
      tmp = camera.read()
      if tmp:
        t = time.time()
        ma = cv.find_line(tmp)
        t = time.time() - t
        print("-- forward time: {}s".format(t))
        # print(ma)
        draw = display.get_draw()
        draw.line([(ma["rect"][0], ma["rect"][1]), (ma["rect"][2], ma["rect"][3])],fill='white',width=1)
        draw.line([(ma["rect"][2], ma["rect"][3]), (ma["rect"][4], ma["rect"][5])],fill='white',width=1)
        draw.line([(ma["rect"][4], ma["rect"][5]), (ma["rect"][6], ma["rect"][7])],fill='white',width=1)
        draw.line([(ma["rect"][6], ma["rect"][7]), (ma["rect"][0], ma["rect"][1])],fill='white',width=1)
        draw.ellipse(((ma["cx"]-2, ma["cy"]-2), (ma["cx"]+2, ma["cy"]+2)), fill=None, width=1)
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

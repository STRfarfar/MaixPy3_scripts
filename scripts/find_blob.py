#!/usr/bin/env python

# cv.find_blob(pic,hsv,tilt=0)函数说明
# 功能:在图片pic中寻找符合hsv颜色区域的色块
# 输入：pic，240*240尺寸的图片bytes数据
#     hsv,hsv阈值数组，前三个是最小值，后三个是最大值
#     tilt斜度选项
#tilt = 0斜度选项 返回值：[{'x': 232, 'y': 32, 'w': 8, 'h': 49, 'pixels': 200, 'cx': 236, 'cy': 56}]，色块列表
#x,y,w,h 色块外框信息
#pixels 色块面积
#cx 色框中心x
#cy 色框中心y
#tilt = 1斜度选项 返回值： [{'x': 236, 'y': 206, 'w': 4, 'h': 7, 'pixels': 16, 'cx': 238, 'cy': 209, 'tilt_Rect': (236.0, 212.0, 236.0, 206.0, 239.0, 206.0, 239.0, 212.0), 'rotation': -1.570796251296997}]
#tilt_Rect 斜框四个顶点
#rotation 斜框斜度

from maix import camera
from _maix_opencv import _v83x_opencv
from PIL import Image, ImageDraw
from maix import display
import time
cv = _v83x_opencv()
class funation:
    red_hsv   = (176,76,0,255,255,255)
    green_hsv = (72,92,62,93,255,255) 
    blue_hsv  = (95,219,0,255,255,255)
    yello_hsv = (18,122,176,33,255,255)
    test = (63,147,161,79,195,195)
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
            ma = cv.find_blob(tmp, self.test)
            t = time.time() - t
            print("-- forward time: {}s".format(t))
            # print(ma)
            draw = display.get_draw()
            if ma:
                for i in ma:
                    draw.rectangle((i["x"], i["y"], i["x"] + i["w"], i["y"] + i["h"]), outline='red', width=1)
                display.show()
            else:
                display.clear()



if __name__ == "__main__":
    import signal
    def handle_signal_z(signum,frame):
        print("erzi over")
        exit(0)
    signal.signal(signal.SIGINT,handle_signal_z)
    start = funation()
    while True:
        start.run()

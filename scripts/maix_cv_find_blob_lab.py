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
# 时间：2021年9月16日
# 作者：dianjixz
from maix import maix_cv
from maix import camera
from PIL import Image, ImageDraw
from maix import display
import time

class funation:
    green = [(28,-36,-14,68,-5,15)]  #绿色
    red = [(20,22,-3,55,52,42)]    #红色
    yellow = [(35,-6,22,88,5,81)]   #黄色
    bull = [(14,12,-63,44,33,-21)]  #蓝色
    white = [(41,6,-32,74,11,-12)]  #白色
    black = [(10,-3,-28,50,10,-4)]  #黑色
    def __init__(self,device=None):
        self.event = self.run
    def __del__(self):
      print("maix_cv_find_blob_lab will exit!")
    def run(self):
        tmp = camera.read(video_num = 0)
        if tmp:
            t = time.time()
            ma = maix_cv.find_blob_lab(tmp, self.bull)
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
        else:
            print('tmp err')


if __name__ == "__main__":
    import signal
    def handle_signalm(signum,frame):
        print("father over")
        exit(0)
    signal.signal(signal.SIGINT,handle_signalm)
    camera.config(size=(224,224))
    start = funation()
    while True:
        start.event()

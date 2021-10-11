#!/usr/bin/env python
# maix_cv.find_line(pic)函数说明
# 功能:在道路图片pic中寻找线
# 输入：pic，240*240尺寸的图片bytes数据
# 返回值：字典类型，rect：矩形的四个顶点，pixels：矩形的面积，cx、cy:矩形的中心坐标，rotation：矩形的倾斜角
#{'rect': [9, 229, 9, 9, 145, 9, 145, 229], 'pixels': 12959, 'cx': 77, 'cy': 119, 'rotation': -1.570796251296997}
# 时间:2021年9月16日
# 作者：dianjixz
from maix import camera
from PIL import Image ,ImageDraw
from maix import display
import time
from maix import vision as maix_cv


class funation:
    def __init__(self,device=None):
      self.event = self.run
    def __del__(self):
      pass
    def run(self):
      tmp = camera.read(video_num = 0)
      if tmp:
        t = time.time()
        ma = maix_cv.find_line(tmp)
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
        print("APP OVER")
        exit(0)
    signal.signal(signal.SIGINT,handle_signal_z)
    camera.config(size=(240,240))
    start = funation()
    while True:
        start.event()


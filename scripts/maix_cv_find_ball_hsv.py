#!/usr/bin/env python

# maix_cv.find_ball(pic,hsv)函数说明
# 功能:在图片pic中寻找符合hsv颜色区域的小球
# 输入：pic，240*240尺寸的图片bytes数据
#     hsv,hsv阈值数组，前三个是最小值，后三个是最大值
# 返回值：[[cr_x,cr_y,cr_w,cr_h]]，拟合小球的中心值，高和宽
# 时间：2021年9月16日
# 作者：dianjixz
from maix import camera
from maix import maix_cv
from PIL import Image, ImageDraw
from maix import display


class funation:
    red_hsv   = (176,76,0,255,255,255)
    green_hsv = (72,92,62,93,255,255) 
    blue_hsv  = (95,219,0,255,255,255)
    yello_hsv = (18,122,176,33,255,255)
    def __init__(self,device=None):
      self.event = self.run
    def __del__(self):
      pass
    def run(self):
      tmp = camera.read(video_num = 0)
      if tmp:
        ma = maix_cv.find_ball(tmp, self.blue_hsv)
        print(ma)
        if ma:
          draw = display.get_draw()
          for i in ma:
            draw.ellipse((i[0]-i[3]/2, i[1]-i[2]/2, i[0]+i[3]/2, i[1]+i[2]/2),
                          outline ='white',
                          width =2)
          display.show()
        else:
          display.clear()


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

#!/usr/bin/env python

# cv.get_blob_hsv(pic,roi,critical)函数说明
# 功能:在图片pic中寻找符合hsv颜色区域的色块
# 输入：pic，240*240尺寸的图片bytes数据
#     roi,感兴趣区域,他是一个数组，[x,y,w,h]
#critical 范围值 ,检测到区域内最多的颜色，然后加减该值
# 返回值：[140, 6, 134, 150, 16, 144]，HSV阈值列表
#[min_h,min_s,min_v,max_h,max_s,max_v] 该值可被直接用于寻找色块


from maix import camera
from _maix_opencv import _v83x_opencv
from PIL import Image, ImageDraw,ImageFont
from maix import display
cv = _v83x_opencv()



class funation:
    font = None
    def __init__(self):
      #跳过一些帧
        image = camera.capture()
        image = camera.capture()
        image = camera.capture()
        image = camera.capture()
        del image
        self.font = ImageFont.truetype("./res/baars.ttf", 20, encoding="unic")
    def run(self):
        tmp = camera.read()
        ma = cv.get_blob_hsv(tmp,[110,110,20,20],0)
        draw = display.get_draw()
        draw.rectangle((110,110, 130, 130), outline='red', width=2)
        draw.text((10, 10), str(ma[:-3]), (255, 0, 0), self.font)  # bgr
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
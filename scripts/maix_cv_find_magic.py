#!/usr/bin/env python
# # MaixPy3魔方面颜色图案获取示例
# # 功能说明：获取魔方面颜色图案信息
# # 时间：2021年9月16日
# # 作者：dianjixz
from maix import camera
from PIL import Image, ImageDraw
from maix import display
import time
# from maix import vision as maix_cv
from _maix_opencv import _v83x_opencv
maix_cv = _v83x_opencv() 


import numpy as np

M = np.array([[0.412453, 0.357580, 0.180423],
              [0.212671, 0.715160, 0.072169],
              [0.019334, 0.119193, 0.950227]])


# im_channel取值范围：[0,1]
def f(im_channel):
    return np.power(im_channel, 1 / 3) if im_channel > 0.008856 else 7.787 * im_channel + 0.137931


def anti_f(im_channel):
    return np.power(im_channel, 3) if im_channel > 0.206893 else (im_channel - 0.137931) / 7.787


# region Lab 转 RGB
def __lab2xyz__(Lab):
    fY = (Lab[0] + 16.0) / 116.0
    fX = Lab[1] / 500.0 + fY
    fZ = fY - Lab[2] / 200.0

    x = anti_f(fX)
    y = anti_f(fY)
    z = anti_f(fZ)

    x = x * 0.95047
    y = y * 1.0
    z = z * 1.0883

    return (x, y, z)


def __xyz2rgb(xyz):
    xyz = np.array(xyz)
    xyz = xyz * 255
    rgb = np.dot(np.linalg.inv(M), xyz.T)
    # rgb = rgb * 255
    rgb = np.uint8(np.clip(rgb, 0, 255))
    return rgb


def Lab2RGB(Lab):
    xyz = __lab2xyz__(Lab)
    rgb = __xyz2rgb(xyz)
    return rgb


class funation:
    mk = [(46, 46, 194, 194),(64,64,77,77),(113,64,126,77),(163,64,176,77),(64,113,77,127),(113,113,127,127),(163,113,176,127),(64,163,77,176),(113,163,127,176),(163,163,176,176)]
    md = [(0, 0, 15, 15),(15, 0, 30, 15),(30, 0, 45, 15), (0, 15, 15, 30), (15, 15, 30, 30),(30, 15, 45, 30),(0, 30, 15, 45),  (15, 30, 30, 45),   (30, 30, 45, 45)]

    def __init__(self,device=None):  
        self.event = self.run
    def __del__(self):
      print("maix_cv_find_blob_lab will exit!")
    def run(self):
        tmp = camera.read(video_num = 0)
        draw = display.get_draw()

        for i,idx in enumerate(self.mk):
            if i == 0:
                draw.rectangle(idx, outline='red', width=1)
            else:
                draw.rectangle(idx, outline='red', width=1)
                mda = idx[0:2] + (13,13)
                lab_c = maix_cv.get_blob_lab(tmp, mda, 0,color = 0)
                rgb_c = (int(lab_c[0]),int(lab_c[1]),int(lab_c[2]))
                print(rgb_c)
                draw.rectangle(self.md[i-1], outline='white', width=1,fill = tuple(rgb_c))

        display.show()


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

# #!/usr/bin/env python
# # MaixPy3魔方面颜色图案获取示例
# # 功能说明：获取魔方面颜色图案信息
# # 时间：2021年9月16日
# # 作者：dianjixz
# from maix import camera
# from PIL import Image, ImageDraw
# from maix import display
# import time
# try:
#   from maix import maix_cv
# except:
#   from _maix_opencv import _v83x_opencv
#   maix_cv = _v83x_opencv()


# class funation:
#     m_gree = [(46,-64,16,79,-34,49)]
#     m_yellow = [(56,-32,37,99,-7,96)]
#     m_blue = [(13,6,-77,40,42,-35)]
#     m_cheng = [(23,26,43,82,78,71)]
#     m_sred = [(17,27,-10,40,61,41)]
#     m_white = [(49,-13,-46,100,19,3)]
#     thr = [m_gree,m_yellow,m_blue,m_cheng,m_sred,m_white]
#     color_list = ["green", "yellow", "blue", "blue", "black", "white"]
#     def __init__(self,device=None):
#       self.event = self.run
#     def __del__(self):
#       pass
#     def run(self):
#         ma = []
#         for i in range(3):
#             tmp = camera.read(video_num = 0)
#             ma.append(maix_cv.find_blob_lab(tmp, self.thr[2 * i]))
#             ma.append(maix_cv.find_blob_lab(tmp, self.thr[2 * i + 1]))
#         draw = display.get_draw()
#         for idx, blob in enumerate(ma):
#             if blob:
#                 for b in blob:
#                     if b["pixels"] > 100 and b["pixels"] < 4000:
#                         draw.rectangle((b["x"], b["y"], b["x"] + b["w"], b["y"] + b["h"]), outline=self.color_list[idx], width=1)
#         display.show()


# if __name__ == "__main__":
#     import signal
#     def handle_signal_z(signum,frame):
#         print("APP OVER")
#         exit(0)
#     signal.signal(signal.SIGINT,handle_signal_z)
#     camera.config(size=(240,240))
#     start = funation()
#     while True:
#         start.event()

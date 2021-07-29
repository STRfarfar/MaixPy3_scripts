#!/usr/bin/env python
#v831上的寻找色块
from maix import camera
from maix import display
from maix import image
from PIL import Image, ImageFont, ImageDraw
import time
import os


camera.config(size=(224, 224))
threshold = [(2, 39, 11, 63, 7, 36)]    #颜色阈值

while True:
    img = camera.read()  # 224 * 224
    img = camera.camera.cam.get_vi()  # 240 * 240
    if len(img):
        image.send_to_image(img, 240, 240)
        ma = image.find_blobs(threshold, roi=[], x_stride=1, y_stride=1,
                                invert=False, area_threshold=1, pixels_threshold=20, merge=True, margin=0)
        for i in ma:
            image.draw_rectangle(i["x"], i["y"], i["w"], i["h"])
        # img_a = image.img_back_rgb888()
        img = Image.frombytes(mode="RGB", size=(240, 240), data=image.img_back_rgb888(), decoder_name="raw")
        image.close()
        display.show(img)


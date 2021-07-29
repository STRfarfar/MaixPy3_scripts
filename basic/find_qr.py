#!/usr/bin/env python
#v831二维码检测功能
from maix import camera
from PIL import Image, ImageFont, ImageDraw
from maix import display
from maix import image
import zbarlight

font = ImageFont.truetype("./res/baars.ttf", 40, encoding="unic")
camera.config(size=(224, 224))

while True:
    img = camera.capture()
    codes = zbarlight.scan_codes(['qrcode'], img)
    if codes:
        print(codes)
        images = Image.new("RGBA", (240, 240), "#00000000")
        draw = ImageDraw.Draw(images)
        draw.text((10, 10), codes[0].decode('ascii'), (255, 0, 0), font)  # bgr
        display.show(images)
    else:
        images = Image.new("RGBA", (240, 240), "#00000000")
        draw = ImageDraw.Draw(images)
        draw.text((10, 10), "not qr", (255, 0, 0), font)  # bgr
        display.show(images)


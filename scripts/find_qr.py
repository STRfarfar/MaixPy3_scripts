#!/usr/bin/env python


from maix import camera
from PIL import Image, ImageFont, ImageDraw
from maix import display
import zbarlight
import time
#qrcode     二维码
#EAN13      European Article Number (欧洲物品编码),超级市场和其它零售业
#UPCA       UPC-A条码是美国较常用也被广泛认可的条码类型,它主要用于零售行业
#UPCE       UPC-E码又称UPC缩短码，是UPC-A码的简化模式
#EAN8       码: 由8个数字组成，属EAN的简易编码型式(EAN缩短码)。
#CODE128    码是广泛应用在企业内部管理、生产流程、物流控制系统方面的条码码制
#Code39


class funation:
    font = None
    def __init__(self):
        image = camera.capture()
        image = camera.capture()
        image = camera.capture()
        image = camera.capture()
        del image
        self.font = ImageFont.truetype("./res/baars.ttf", 20, encoding="unic")
    def run(self):
        img = camera.capture()
        t = time.time()
        codes = zbarlight.scan_codes(['qrcode','EAN13'], img)     #二维码和条形码
        t = time.time() - t
        print("-- forward time: {}s".format(t))
        # codes = zbarlight.scan_codes(['EAN13'], img)        #普通条形码
        if codes:
            print(codes)
            draw = display.get_draw()
            draw.text((10, 10), codes[0].decode('ascii'), (255, 0, 0), self.font)  # bgr
            display.show()
        else:
            draw = display.get_draw()
            draw.text((10, 10), "not qr", (255, 0, 0), self.font)  # bgr
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
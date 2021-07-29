#!/usr/bin/env python

from maix import camera
from PIL import Image, ImageFont, ImageDraw
from maix import display
from maix import nn
from res.classes_label import labels
from evdev import InputDevice
import asyncio
import time
import os
import socket
from maix import image
import zbarlight
from maix.nn import decoder

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = "IP: " + s.getsockname()[0]
    except Exception as e:
        ip = "IP does not exist"
    finally:
        s.close()
    return ip

def draw_rectangle_with_title(img, box, disp_str, bg_color=(255, 0, 0), font_color=(255, 255, 255)):
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    font_w, font_h = font.getsize(disp_str)
    draw.rectangle((box[0], box[1], box[0] + box[2], box[1] +
                   box[3]), fill=None, outline=bg_color, width=2)
    draw.rectangle((box[0], box[1] - font_h, box[0] +
                   font_w, box[1]), fill=bg_color)
    draw.text((box[0], box[1] - font_h), disp_str, fill=font_color, font=font)

font = ImageFont.truetype("./res/baars.ttf", 40, encoding="unic")

canvas = Image.new("RGBA", (240, 240), "#2c3e50")
with Image.open('./res/logo.png') as logo:
    canvas.paste(logo, (50, 40, 50 + logo.size[0], 40 + logo.size[1]), logo)

draw = ImageDraw.Draw(canvas)
draw.text((10, 195), u'MaixPy.Sipeed.COM', "#bdc3c7", font)
draw.text((0, 0), u'<exit', "#7f8c8d", font)
draw.text((160, 0), u'demo> ', "#16a085", font)

exits = Image.new("RGBA", (240, 240), "#2c3e50")
draw = ImageDraw.Draw(exits)
draw.text((20, 40), u"Quit?\nLater can execute", "#1abc9c", font)
draw.text((30, 120), u"/home/app.py", "#16a085", font)

draw.text((20, 180), get_host_ip(), "#bdc3c7", font)
draw.text((0, 0), u'<No', "#2ecc71", font)
draw.text((180, 0), u'Yes> ', "#e74c3c", font)
# display.show(exits)

ini = 1
init_nn_s = 0

packet = {
    'selected': "main",
    'status': 0
}

asyncio.set_event_loop(asyncio.new_event_loop())
keys = InputDevice('/dev/input/event0')

async def keys_events(packet, device):
    global ini
    global init_nn_s
    async for event in device.async_read_loop():
        if event.value == 1 and event.code == 0x02:  # 右键
            if packet["status"] == 0:
                if packet["selected"] == "main":
                    img = Image.open("./res/face.png")
                    img = img.convert('RGBA')
                    display.show(img)
                    packet["status"] = 1
                elif packet["selected"] == "exit":
                    display.clear((0, 0, 0))
                    exit(233)
            elif packet["status"] == 1:
                packet["selected"] = "demo1"
                init_nn_s = 2
            elif packet["status"] == 2:
                packet["selected"] = "demo2"
            elif packet["status"] == 3:
                packet["selected"] = "demo3"
                init_nn_s = 1
            elif packet["status"] == 4:
                packet["selected"] = "demo4"
            elif packet["status"] == 5:
                display.show(canvas)
                packet["selected"] = "main"
                packet["status"] = 0
        elif event.value == 1 and event.code == 0x03:  # 左键
            if packet["status"] == 0:
                packet["selected"] = "exit"
            else:
                if packet["selected"] != "main":
                    packet["selected"] = "main"
                    packet["status"] = 0
                else:
                    packet["status"] += 1
                    if packet["status"] == 5:
                        packet["status"] = 1
                    if packet["status"] == 1:
                        img = Image.open("./res/face.png")
                        img = img.convert('RGBA')
                        display.show(img)
                        del img
                    elif packet["status"] == 2:
                        img = Image.open("./res/blob.png")
                        img = img.convert('RGBA')
                        display.show(img)
                        del img
                    elif packet["status"] == 3:
                        img = Image.open("./res/fenlei.png")
                        img = img.convert('RGBA')
                        display.show(img)
                        del img
                    elif packet["status"] == 4:
                        img = Image.open("./res/qr.png")
                        img = img.convert('RGBA')
                        display.show(img)
                        del img
                    elif packet["status"] == 5:
                        img = Image.open("./res/exit.png")
                        img = img.convert('RGBA')
                        display.show(img)
                        del img
for device in [keys]:
    asyncio.ensure_future(keys_events(packet, device))

camerax = None
npu = None
yolo2_decoder = None
camerax = camera
camera.config(size=(224, 224))

async def main(packet):
    global ini
    global camerax
    global font
    global fen
    global init_nn_s
    global npu
    global yolo2_decoder
    # camera.config(size=(240,240))
    labelss = ["person"]
    anchors = [1.19, 1.98, 2.79, 4.59, 4.53, 8.92, 8.06, 5.29, 10.32, 10.65]
    if init_nn_s == 1:  # 分类
        if npu != None:
            del npu
            time.sleep(1)
        npu = nn.load({
            "param": "./res/resnet.param",
            "bin": "./res/resnet.bin"
        }, opt={
            "model_type":  "awnn",
            "inputs": {
                "input0": (224, 224, 3)
            },
            "outputs": {
                "output0": (1, 1, 1000)
            },
            "first_layer_conv_no_pad": False,
            "mean": [127.5, 127.5, 127.5],
            "norm": [0.00784313725490196, 0.00784313725490196, 0.00784313725490196],
        })
        init_nn_s = 0
    if init_nn_s == 2:  # 人脸
        if npu != None:
            del npu
            time.sleep(1)
        model = {
            "param": "./res/yolo2_face_int8.param",
            "bin": "./res/yolo2_face_int8.bin"
        }
        options = {
            "model_type":  "awnn",
            "inputs": {
                "input0": (224, 224, 3)
            },
            "outputs": {
                "output0": (7, 7, (1+4+1)*5)
            },
            "mean": [127.5, 127.5, 127.5],
            "norm": [0.0078125, 0.0078125, 0.0078125],
        }
        npu = nn.load(model, opt=options)
        yolo2_decoder = decoder.Yolo2(
            len(labelss), anchors, net_in_size=(224, 224), net_out_size=(7, 7))
        init_nn_s = 0
    if packet["selected"] == "demo3":  # 分类
        img = camerax.capture()
        if img:
            out = npu.forward(img, quantize=True)
            out = nn.F.softmax(out)
            if out.max() > 0.1:
                images = Image.new("RGBA", (240, 240), "#00000000")
                draw = ImageDraw.Draw(images)
                draw.text((0, 0), "{:.2f}: {}".format(
                    out.max(), labels[out.argmax()]), (255, 0, 0), font)
                display.show(images)
        # else:
            # await asyncio.sleep(0.02)
    elif packet["selected"] == "main":
        if packet["status"] == 0:
            display.show(canvas)
    elif packet["selected"] == "exit":
        if packet["status"] == 0:
            display.show(exits)
    elif packet["selected"] == "demo1":
        img = camera.capture()
        out = npu.forward(img, quantize=True, layout="hwc")
        boxes, probs = yolo2_decoder.run(
            out, nms=0.3, threshold=0.5, img_size=(224, 224))
        if len(boxes):
            t = time.time()
            img = Image.new("RGBA", (240, 240), "#00000000")
            for i, box in enumerate(boxes):
                class_id = probs[i][0]
                prob = probs[i][1][class_id]
                disp_str = "{}:{:.2f}%".format(labelss[class_id], prob*100)
                draw_rectangle_with_title(img, box, disp_str)
            display.show(img)
            print("-- draw: ", time.time() - t)
            t = time.time()
            # display.show(img)
            print("-- show: ", time.time() - t)
        else:
            display.show(Image.new("RGBA", (240, 240), "#00000000"))

    elif packet["selected"] == "demo2":
        img = camerax.read()  # 224 * 224
        img = camerax.camera.cam.get_vi()  # 240 * 240
        if len(img):
            image.send_to_image(img, 240, 240)
            ma = image.find_blobs([(2, 39, 11, 63, 7, 36)], roi=[], x_stride=1, y_stride=1,
                                  invert=False, area_threshold=1, pixels_threshold=20, merge=True, margin=0)
            for i in ma:
                image.draw_rectangle(i["x"], i["y"], i["w"], i["h"])
            # img_a = image.img_back_rgb888()
            img = Image.frombytes(mode="RGB", size=(
                240, 240), data=image.img_back_rgb888(), decoder_name="raw")
            image.close()
            display.show(img)
    elif packet["selected"] == "demo4":  # 二维码
        img = camerax.capture()
        codes = zbarlight.scan_codes(['qrcode'], img)
        if codes:
            print(codes)
            images = Image.new("RGBA", (240, 240), "#00000000")
            draw = ImageDraw.Draw(images)
            draw.text((10, 10), codes[0].decode(
                'ascii'), (255, 0, 0), font)  # bgr
            display.show(images)
        else:
            images = Image.new("RGBA", (240, 240), "#00000000")
            draw = ImageDraw.Draw(images)
            draw.text((10, 10), "not qr", (255, 0, 0), font)  # bgr
            display.show(images)
    # else:
    #     # await asyncio.sleep(0.02)
    asyncio.ensure_future(main(packet))

asyncio.ensure_future(main(packet))
loop = asyncio.get_event_loop()
loop.run_forever()

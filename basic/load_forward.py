from maix import nn
from PIL import Image, ImageFont, ImageDraw
from maix import display
from classes_label import labels
import time
from maix import camera
camera.config(size=(224, 224))
# test_jpg = "/root/test_input/input.jpg"
model = {
    "param": "./res/resnet.param",
    "bin": "./res/resnet.bin"
}

options = {
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
}
print("-- load model:", model)
m = nn.load(model, opt=options)
print("-- load ok")
font = ImageFont.truetype("./res/baars.ttf",40, encoding="unic")
# print("-- read image")
# img = Image.open(test_jpg)
# print("-- read image ok")
# print("-- forward model with image as input")
# out = m.forward(img, quantize=True)
# print("-- read image ok")
# print("-- out:", out.shape)
# out = nn.F.softmax(out)
# print(out.max(), out.argmax())

while 1:
    img = camera.capture()
    t = time.time()
    out = m.forward(img, quantize=True)
    t = time.time() - t
    print("-- forward time: {}s".format(t))
    t = time.time()
    out2 = nn.F.softmax(out)
    t = time.time() - t
    print("-- softmax time: {}s".format(t))
    msg = "{:.2f}: {}".format(out.max(), labels[out.argmax()])
    print(msg)
    img = Image.new("RGBA", (240, 240), "#00000000")
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), msg, (255, 0, 0), font)
    display.show(img)
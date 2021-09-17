#!/usr/bin/env python

from time import sleep
from PIL import Image, ImageFont, ImageDraw
from maix import display, camera
from _maix_opencv import _v83x_opencv
from evdev import InputDevice
from select import select
import pickle
import time
import sys
import os

cv = _v83x_opencv()

def find_multi_color(thr_list, label_list):
    obj_num = 0
    tmp = camera.read()
    for idx, thr in enumerate(thr_list):
        ma = cv.find_blob(tmp, thr, tilt=1)
        if ma:
            pixels_max = 0
            for i in ma:
                if i["pixels"] > pixels_max:
                    pixels_max = i["pixels"]
                    info = i
            obj_num = obj_num + 1         
            draw = display.get_draw()     
            draw.rectangle((info["x"], info["y"], info["x"] + info["w"], info["y"] + info["h"]), outline="white", width=1)
            print(label_list[idx], end=" ")
    print()
    if obj_num != 0:
        display.show()
    else:
        display.clear()

keys = InputDevice('/dev/input/event0') 

def key_scan():
    key_val = 0
    r,w,x = select([keys], [], [], 0)
    if r:
        for event in keys.read():
            if event.value == 1 and event.code == 0x02:     # 右键
                key_val = 2
            elif event.value == 1 and event.code == 0x03:   # 左键
                key_val = 1
    return key_val

if __name__ == "__main__":
    import signal
    def handle_signal_z(signum,frame):
        print("APP OVER")
        exit(0)
    signal.signal(signal.SIGINT,handle_signal_z)
    MAX_NUM = 4
    labels = ["label"] * MAX_NUM
    hsv_list = [[0, 0, 0, 0, 0, 0]] * MAX_NUM
    idx = 0
    hsv_tmp = [0, 0, 0, 0, 0, 0]
    mode = 0

    # 加载标签和数据 
    if os.path.isfile("./data.pkl") == True:
        with open("data.pkl", "rb") as f:
            labels = pickle.load(f)
            hsv_list = pickle.load(f)
    
    while True:
        key_val = key_scan()        # 按键扫描
        if key_val == 1:            # 左键按下
            if mode == 1:
                mode = 0            # 学习模式
            else:
                print("Please input the label:", end=" ")
                label = input()
                if label == "clear":                # 删除所有标签和数据
                    idx = 0
                    for i in range(MAX_NUM):
                        labels[i] = ""
                        hsv_list[i] = [0, 0, 0, 0, 0, 0]
                else:
                    labels[idx] = label             # 添加标签到标签列表
                    hsv_list[idx] = hsv_tmp         # 添加颜色阈值到阈值列表
                with open("data.pkl", "wb") as f:   # 保存标签和颜色阈值到文件 
                    pickle.dump(labels, f)
                    pickle.dump(hsv_list, f)
                print("Save data successfully")
                with open("data.pkl", "rb") as f:
                    labels = pickle.load(f)
                    hsv_list = pickle.load(f)
                print("data is:", labels, hsv_list)
                idx = idx + 1
                if idx == 4:
                    idx = 0
        elif key_val == 2:          # 右键按下
            mode = 1                # 识别模式

        if mode == 0:
            img = camera.read()
            hsv_tmp = cv.get_blob_hsv(img, [110,110,20,20], 20)   # 获取hsv阈值
            draw = display.get_draw()
            draw.rectangle((110,110, 130, 130), outline='red', width=1)
            display.show()
            # print(hsv_tmp)
        else:
            find_multi_color(hsv_list, labels)


            

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
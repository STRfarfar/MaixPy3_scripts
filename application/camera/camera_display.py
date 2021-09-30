#!/usr/bin/env python
# MaixPy3拍照显示脚本
# 功能说明：拍照显示
# 时间：2021年9月30日
# 作者：dianjixz


from maix import display,camera
while True:
    display.show(camera.capture())
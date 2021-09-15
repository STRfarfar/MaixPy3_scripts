#!/usr/bin/env python3
import configparser
import os
import sys
import importlib
from evdev import InputDevice
from select import select
from PIL import Image, ImageFont, ImageDraw
from maix import display
import gc
from maix import camera



class SMART:
    modules_name = []
    keys = None
    status_old = None
    status = "default"
    fun_status = 0
    def __init__(self):
        camera.config(size=(240,240 ))
        font = ImageFont.truetype("./res/baars.ttf", 20, encoding="unic")
        canvas = Image.new("RGBA", (240, 240), "#2c3e50")
        with Image.open('./res/logo.png') as logo:
            canvas.paste(logo, (50, 40, 50 + logo.size[0], 40 + logo.size[1]), logo)
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 195), u'MaixPy.Sipeed.COM', "#bdc3c7", font)
        draw.text((0, 0), u'<exit', "#7f8c8d", font)
        draw.text((160, 0), u'demo> ', "#16a085", font)
        display.show(canvas)
        del draw
        del canvas
        del font
        gc.collect()
        conf = configparser.ConfigParser()
        # conf.read(os.path.dirname(os.path.realpath(__file__) + '/examples_comprehensive.ini'))
        conf.read(os.path.dirname(os.path.realpath(__file__)) + '/examples_comprehensive.ini')
        #将模块路径添加到环境变量里面
        for sections in conf.sections():            
            paths = conf.get(sections, 'path')
            if paths not in sys.path:
                sys.path.append(paths)
                # print(paths)
        #添加模块的名字
        for sections in conf.sections():
            self.modules_name.append(sections)
        self.keys = InputDevice('/dev/input/event0')
    def default(self):
        r,w,x = select([self.keys], [], [])
        if r:
            for event in self.keys.read():
                if event.value == 1 and event.code == 0x02:     # 右键
                    self.status = "fun_choose"
                elif event.value == 1 and event.code == 0x03:   # 左键
                    canvas = Image.new("RGB", (240, 240), "#2c3e50")
                    display.show(canvas)
                    exit(0)
    def fun_choose(self):
        self.fun_status = 0
        font = ImageFont.truetype("./res/baars.ttf", 20, encoding="unic")
        canvas = Image.new("RGB", (240, 240), "#2c3e50")
        with Image.open('./res/logo.png') as logo:
                canvas.paste(logo, (50, 40, 50 + logo.size[0], 40 + logo.size[1]), logo)
        draw = ImageDraw.Draw(canvas)
        draw.text((0, 0),"next", "#bdc3c7", font)
        draw.text((190, 0),"enter", "#bdc3c7", font)
        draw.text((80, 5),self.modules_name[self.fun_status], "#bdc3c7", font)
        display.show(canvas)
        r,w,x = select([self.keys], [], [], 0)
        if r:
            for event in self.keys.read():
                pass
        while True:
            r,w,x = select([self.keys], [], [])
            if r:
                for event in self.keys.read():
                    if event.value == 1 and event.code == 0x02:     # 右键
                        if self.fun_status >= len(self.modules_name):
                            self.status = "default"
                        else:
                            self.status = "fun_run"
                        del draw
                        del canvas
                        del font
                        gc.collect()
                        return

                    elif event.value == 1 and event.code == 0x03:   # 左键
                        if self.fun_status >= len(self.modules_name):
                            self.fun_status = 0
                        else:
                            self.fun_status += 1
                        canvas = Image.new("RGB", (240, 240), "#2c3e50")
                        with Image.open('./res/logo.png') as logo:
                            canvas.paste(logo, (50, 40, 50 + logo.size[0], 40 + logo.size[1]), logo)
                        draw = ImageDraw.Draw(canvas)
                        draw.text((0, 0),"next", "#bdc3c7", font)
                        draw.text((190, 0),"enter", "#bdc3c7", font)
                        if self.fun_status >= len(self.modules_name):
                            draw.text((80, 5),'exit', "#bdc3c7", font)
                            display.show(canvas)
                        else:
                            draw.text((80, 5),self.modules_name[self.fun_status], "#bdc3c7", font)
                            display.show(canvas)
    def fun_run(self): 
        display.clear()
        pid=os.fork()
        if pid == 0:
            print("执行子进程，子进程pid={pid},父进程ppid={ppid}".format(pid=os.getpid(),ppid=os.getppid()))
            import signal
            def handle_signal_z(signum,frame):
                print("erzi over")
                exit(0)
            signal.signal(signal.SIGINT,handle_signal_z)
            try:
                fun_moudle = importlib.import_module(self.modules_name[self.fun_status])
            except:
                exit(1)
            start = fun_moudle.funation()
            while True:
                start.run()
        else:
            print("执行父进程，子进程pid={pid},父进程ppid={ppid}".format(pid=os.getpid(),ppid=os.getppid()))
            import signal
            def handle_signal(signum,frame):
                print("father over")
                exit(0)
            signal.signal(signal.SIGINT,handle_signal)
            while True:
                r,w,x = select([self.keys], [], [])
                if r:
                    for event in self.keys.read():
                        if event.value == 1 and event.code == 0x03:   # 左键
                            os.kill(pid,signal.SIGINT)
                            while True:
                                print("wait zi exit!")
                                if os.wait()[0] == pid:
                                    break
                            exit(os.system('sleep 0.5 && cd /home && python examples_comprehensive.py &'))
                            # gc.collect()
                            # self.status = "default"
                            # return
    def switch(self):
        if self.status == "default":
            font = ImageFont.truetype("./res/baars.ttf", 20, encoding="unic")
            canvas = Image.new("RGB", (240, 240), "#2c3e50")
            with Image.open('./res/logo.png') as logo:
                canvas.paste(logo, (50, 40, 50 + logo.size[0], 40 + logo.size[1]), logo)
            draw = ImageDraw.Draw(canvas)
            draw.text((10, 195), u'MaixPy.Sipeed.COM', "#bdc3c7", font)
            draw.text((0, 0), u'<exit', "#7f8c8d", font)
            draw.text((160, 0), u'demo> ', "#16a085", font)
            display.show(canvas)
            del draw
            del canvas
            del font
            gc.collect()
        self.status_old = self.status

smart = SMART()
funation = {
    "default":smart.default,
    "fun_choose":smart.fun_choose,
    "fun_run":smart.fun_run
}

if __name__ == "__main__":
    while True:
        if(smart.status_old != smart.status):
            smart.switch() 
        funation[smart.status]()






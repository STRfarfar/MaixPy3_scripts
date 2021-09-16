#!/usr/bin/env python
# MaixPy3读取GPIO脚本
# 功能说明：读取GPIO上的电平信号,并保存
# 时间：2021年9月16日
# 作者：dianjixz
from gpiod import chip, line, line_request


class funation:         # for V831
    PF_BASE = 160 # "PF"
    PG_BASE = 192 # "PG"
    PH_BASE = 224 # "PH"   
    def __init__(self,device=None,gpiochip="gpiochip1",IO_BASE=224,GPIO_PIN=14):
      self.event = self.get_gpio
      self.gpiochip1 = chip(gpiochip)
      self.IO = self.gpio(IO_BASE + GPIO_PIN) # "PH14"
    def __del__(self):
      pass
    def gpio(self,line_offset=238):     #默认"PH14"
        try:
            tmp = None
            tmp = self.gpiochip1.get_line(line_offset)
            config = line_request() # led.active_state == line.ACTIVE_LOW
            config.request_type = line_request.DIRECTION_INPUT # line.DIRECTION_INPUT
            tmp.request(config)
        except Exception as e:
            print(e)
        finally:
            return tmp
    def get_gpio(self):
        pin = self.IO.get_value()
        print("GPIO:",pin)
        return pin


if __name__ == "__main__":
    import signal
    def handle_signal_z(signum,frame):
        print("erzi over")
        exit(0)
    signal.signal(signal.SIGINT,handle_signal_z)
    start = funation()
    while True:
        start.event()
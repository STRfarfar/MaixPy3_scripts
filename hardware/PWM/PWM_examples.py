#!/usr/bin/env python
# MaixPy3使用PWM脚本
# 功能说明：设置PWM输出
# 时间：2021年9月22日
# 作者：dianjixz
import time
from maix import pwm


class funation:         # for V831
    def __init__(self,device=None):
      self.event = self.main                                                                #定义统一调用接口,相当于函数指针  
    def __del__(self):
      pass
    def main(self):
        with pwm.PWM(6) as pwm6:
            pwm6.period = 1000000
            pwm6.duty_cycle = 10000
            pwm6.enable = True
            duty_cycle = 10000
            while True:
                for i in range(1,10):
                    pwm6.duty_cycle = 10000 * i
                    time.sleep(1)


if __name__ == "__main__":
    import signal
    def handle_signal_z(signum,frame):
        print("APP OVER")
        exit(0)
    signal.signal(signal.SIGINT,handle_signal_z)
    start = funation()
    while True:
        start.event()
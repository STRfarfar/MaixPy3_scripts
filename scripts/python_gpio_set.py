#!/usr/bin/env python
from gpiod import chip, line, line_request
import time
# for V831
class funation:
    PF_BASE = 160 # "PF"
    PG_BASE = 192 # "PG"
    PH_BASE = 224 # "PH"
    def __init__(self):
        self.gpiochip1 = chip("gpiochip1")
        self.led = self.gpio(self.PH_BASE + 14) # "PH14"
    def gpio(self,line_offset=(self.PH_BASE + 14)):
        try:
            tmp = None
            tmp = self.gpiochip1.get_line(line_offset)
            config = line_request() # led.active_state == line.ACTIVE_LOW
            config.request_type = line_request.DIRECTION_OUTPUT # line.DIRECTION_INPUT
            tmp.request(config)
        except Exception as e:
            print(e)
        finally:
            return tmp
    def run(self):
        self.led.set_value(0)
        time.sleep(0.1)
        self.led.set_value(1)
        time.sleep(0.1)


if __name__ == "__main__":
    import signal
    def handle_signalm(signum,frame):
        print("father over")
        exit(0)
    signal.signal(signal.SIGINT,handle_signalm)
    start = funation()
    while True:
        start.run()
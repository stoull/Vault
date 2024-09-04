import threading
import time
from datetime import datetime
from subprocess import run

# External module imports
# import RPi.GPIO as GPIO

class ScreenControl:
    def __init__(self, timeout=300):  # 默认超时时间为300秒（5分钟）
        self.detectedX = 0
        self.last_detection_time = time.time()
        self.timeout = self.get_timeout()
        self.screen_on = ScreenControl.current_screen_state()
        self.running = False
        self.timer_thread = None
        self.check_counter = 0

    def get_timeout(self):
        current_time = datetime.now().time()
        night_start = time(22, 0)  # 22:00
        night_end = time(6, 0)  # 06:00

        if night_start <= current_time or current_time < night_end:
            return 60  # 1分钟 (60秒)
        else:
            return 180  # 3分钟 (180秒)

    def start(self):
        self.running = True
        self.timer_thread = threading.Thread(target=self.check_timeout)
        self.timer_thread.start()

    def stop(self):
        self.running = False
        self.timer_thread.join()

    def update_detection(self, detected):
        self.detectedX = detected
        if detected == 1:
            self.last_detection_time = time.time()
            if not self.screen_on:
                self.change_screen_on()

    def check_timeout(self):
        while self.running:
            time_since_last_detection = time.time() - self.last_detection_time
            if time_since_last_detection >= self.timeout and self.screen_on:
                self.change_screen_off()
            # 每60秒检查一次屏幕状态,可能会被其它的程序改变
            self.check_counter += 1
            if self.check_counter >= 60:
                self.screen_on = ScreenControl.current_screen_state()
                self.check_counter = 0  # 重置计数器
            time.sleep(1)  # 每秒检查一次

    def change_screen_off(self):
        if self.screen_on == True:
            if ScreenControl.turn_screen_off():
                self.screen_on = False

    def change_screen_on(self):
        if not self.screen_on:
            if ScreenControl.turn_screen_on():
                self.screen_on = True

    @classmethod
    def turn_screen_off(cls):
        print("turn_screen_off xxx ")
        result = run('vcgencmd display_power 0', shell=True, capture_output=True, text=True)
        if result.stdout == 'display_power=0\n':
            return True
        else:
            return False

    @classmethod
    def turn_screen_on(cls):
        print("turn_screen_on xxx ")
        result = run('vcgencmd display_power 1', shell=True, capture_output=True, text=True)
        if result.stdout == 'display_power=1\n':
            return True
        else:
            return False

    @classmethod
    def current_screen_state(cls):
        result = run('vcgencmd display_power', shell=True, capture_output=True, text=True)
        if result.stdout == 'display_power=1\n':
            return True
        else:
            return False

# class PIRDetector:
#     def __init__(self, mode=GPIO.BCM, pin=4):  # 默认超时时间为300秒（5分钟）
#         GPIO.setmode(mode)
#         GPIO.setup(pin, GPIO.IN)
#         self.mode = mode
#         self.pin = pin
#         self.screen_controller = None
#
#     def start_detect(self):
#         self.screen_controller = ScreenControl()
#         self.screen_controller.start()
#         try:
#             while True:
#                 current_datetime = datetime.now()
#                 cDateStr = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
#                 value = GPIO.input(self.pin)
# #                 print(f"{cDateStr} value: ", value)
#                 self.screen_controller.update_detection(value)
#                 time.sleep(1)
#         except KeyboardInterrupt:
#             self.screen_controller.stop()
#             print("程序被用户中断")
#         finally:
#             # 清理 GPIO 设置
#             GPIO.cleanup()

if __name__ == "__main__":
    print('检测中.......按Ctrl+C退出')
    # detector = PIRDetector()
    # detector.start_detect()
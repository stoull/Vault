import threading
import time
from datetime import datetime
from subprocess import run

# External module imports
# import RPi.GPIO as GPIO

class ScreenControl:
    def __init__(self, timeout=60):  # 默认超时时间为300秒（5分钟）
        self.detectedX = 0
        self.last_detection_time = time.time()
        self.timeout = timeout
        screen_state_int = self.current_screen_state()
        self.screen_on = screen_state_int == 1
        self.running = False
        self.timer_thread = None

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
                self.turn_screen_on()
            else:
                print("screen is oning ")

    def check_timeout(self):
        while self.running:
            time_since_last_detection = time.time() - self.last_detection_time
            if time_since_last_detection >= self.timeout:
                if self.screen_on == False:
                    print("该关屏幕了, 但屏幕本来就是关着的")
            if time_since_last_detection >= self.timeout and self.screen_on:
                self.turn_screen_off()
            time.sleep(1)  # 每秒检查一次

    def change_screen_off(self):
        result = ScreenControl.turn_screen_off()
        if result == 0:
            self.screen_on = False

    def change_screen_on(self):
        if self.current_screen_state() != 1:
            result = ScreenControl.turn_screen_on()
            if result == 1:
                self.screen_on = True
            else:
                print("该开屏幕了, 但屏幕没有开起来")

    @classmethod
    def turn_screen_off(cls):
        result = run('vcgencmd display_power 0', shell=True, capture_output=True, text=True)
        return result.returncode

    @classmethod
    def turn_screen_on(cls):
        result = run('vcgencmd display_power 1', shell=True, capture_output=True, text=True)
        return result.returncode

    @classmethod
    def current_screen_state(cls):
        result = run('vcgencmd display_power', shell=True, capture_output=True, text=True)
        return result.returncode

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
#                 self.screen_controller.update_detection(value)
#                 time.sleep(1)
#         except KeyboardInterrupt:
#             self.screen_controller.stop()
#             print("程序被用户中断")
#         finally:
#             # 清理 GPIO 设置
#             GPIO.cleanup()

# if __name__ == "__main__":
#     print('检测中....')
#     detector = PIRDetector()
#     detector.start_detect()
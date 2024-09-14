import sqlite3, os, time, platform
import Adafruit_DHT
import psutil
from datetime import datetime
import requests

DB_FILE = "/home/pi/Documents/PythonProjects/Vault/api/surroundings.db"
# DB_FILE = "/Users/hut/Documents/PythonProjects/Vault/api/surroundings.db"
# 心知天气 https://www.seniverse.com
# WEATHER_URL = 'https://api.seniverse.com/v3/weather/now.json?key=S4zs06GXMojuzjjUH&location=Shenzhen&language=zh-Hans&unit=c'
# open weather
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather?lat=22.560780204311204&lon=113.87890358356606&appid=20c7b818bbb2f911cda86ce2798a91b0&lang=zh'
LOCATION = 'HOME'   # 记录的位置信息，如卧室，办公室，厨房等
# LOCATION = 'OFFICE'   # 记录的位置信息，如卧室，办公室，厨房等

def readTemAndHumidity():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 9)

    if humidity is not None and temperature is not None:
        humi = round(humidity, 2)
        temp = round(temperature, 2)
        result = (temp, humi)
        return result
    else:
        return (0, 0)

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_system_uptime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(psutil.boot_time()))


def get_system_run_duration():
    # 获取系统启动时间（时间戳）
    boot_time = psutil.boot_time()
    # 获取当前时间（时间戳）
    current_time = time.time()

    # 计算开机时长（秒）
    uptime_seconds = current_time - boot_time
    return int(uptime_seconds)

def get_cpu_temperature():
    # 注意：此方法在Windows上可能不适用
    if platform.system() == "Linux":
        try:
            # 读取lm-sensors提供的温度信息
            temp_info = psutil.sensors_temperatures()
            #             print(f"temp_info: {temp_info}")
            if 'cpu_thermal' in temp_info:
                temp_cpu = temp_info['cpu_thermal'][0].current
                return round(temp_cpu, 2)
            else:
                print("无法获取温度信息")
                return 0
        except Exception as e:
            print(str(e))
            return 0
    else:
        print("此功能在非Linux系统上不可用")
        return 0

def kelvin_to_celsius(kelvin):
    if kelvin < 0:
        raise 0
    celsius = kelvin - 273.15
    return celsius

# 获取室外温度
def get_outside_weather_now():
    place_weather = {
        'weather': '--',
        'weather_des': '--',
        'weather_code': '0',
        'weather_icon': '--',
        'outdoors_temp': '0',
        'outdoors_feels_like': '0',
        'outdoors_temp_min': '0',
        'outdoors_temp_max': '0',
        'outdoors_pressure': '0',
        'outdoors_humidity': '0'
    }
    try:
        response = requests.get(WEATHER_URL, timeout=30)
        response.raise_for_status()  # 检查请求是否成功（状态码为200-299）

        # 如果请求成功，处理响应数据
        res = response.json()
        weather = res['weather'][0]
        main_info = res['main']
        place_weather['weather'] = weather['main']
        place_weather['weather_des'] = weather['description']
        place_weather['weather_code'] = weather['id']
        place_weather['weather_icon'] = weather['icon']
        place_weather['outdoors_temp'] = round(kelvin_to_celsius(main_info['temp']), 2)
        place_weather['outdoors_feels_like'] = round(kelvin_to_celsius(main_info['feels_like']), 2)
        place_weather['outdoors_temp_min'] = round(kelvin_to_celsius(main_info['temp_min']), 2)
        place_weather['outdoors_temp_max'] = round(kelvin_to_celsius(main_info['temp_max']), 2)
        place_weather['outdoors_pressure'] = main_info['pressure']
        place_weather['outdoors_humidity'] = main_info['humidity']
        return place_weather
    except requests.exceptions.Timeout:
        # print('请求超时，请稍后重试。')
        return place_weather
    except requests.exceptions.RequestException as e:
        # 处理其他请求异常（如连接错误、HTTP错误等）
        # print('请求失败:', e)
        return place_weather
    except ValueError:
        # 处理JSON解析错误
        # print('响应不是有效的JSON格式。')
        return place_weather

def insertARecord(params):
    db_file = os.path.join(os.path.dirname(__file__), 'surroundings.db')
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO surroundings(location, temperature, humidity, cup_temp,"
        " cpu_used_rate, sys_uptime, sys_runtime, weather, weather_code,"
        " weather_des, weather_icon, outdoors_temp, outdoors_feels_like, outdoors_temp_min,"
        " outdoors_temp_max, outdoors_pressure, outdoors_humidity)"
        " values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        params)
    con.commit()
    cur.close()

if __name__ == "__main__":
    tem, humi = readTemAndHumidity()
    cpu_usage = get_cpu_usage()
    cpu_temperature = get_cpu_temperature()
    system_uptime = get_system_uptime()
    syste_runtime = get_system_run_duration()

    # 获取室外温度
    now_weather = get_outside_weather_now()
    weather = now_weather['weather']
    weather_des = now_weather['weather_des']
    weather_code = now_weather['weather_code']
    weather_icon = now_weather['weather_icon']
    outdoors_temp = now_weather['outdoors_temp']
    outdoors_feels_like = now_weather['outdoors_feels_like']
    outdoors_temp_min = now_weather['outdoors_temp_min']
    outdoors_temp_max = now_weather['outdoors_temp_max']
    outdoors_pressure = now_weather['outdoors_pressure']
    outdoors_humidity = now_weather['outdoors_humidity']

    # print(f"室外天气: {now_weather}")
    #
    # print(f"记录的地点: {LOCATION}")
    # print(f"温湿度: {tem} {humi}")
    # print(f"CPU使用率: {cpu_usage}%")
    # print(f"系统开机时间: {system_uptime}")
    # print(f"CPU温度: {cpu_temperature}°C")
    # print(f"系统运行时间: {syste_runtime}")

    current_time = datetime.now()

    insertARecord([LOCATION,
                   tem,
                   humi,
                   cpu_temperature,
                   cpu_usage,
                   system_uptime,
                   syste_runtime,
                   weather,
                   weather_code,
                   weather_des,
                   weather_icon,
                   outdoors_temp,
                   outdoors_feels_like,
                   outdoors_temp_min,
                   outdoors_temp_max,
                   outdoors_pressure,
                   outdoors_humidity
                   ])

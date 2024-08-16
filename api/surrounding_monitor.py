import sqlite3, os, time, platform, json
import Adafruit_DHT
import psutil

import requests

DB_FILE = "/home/pi/Documents/PythonProjects/Vault/api/surroundings.db"
# DB_FILE = "/Users/hut/Documents/PythonProjects/Vault/api/surroundings.db"
WEATHER_URL = 'https://api.seniverse.com/v3/weather/now.json?key=S4zs06GXMojuzjjUH&location=Shenzhen&language=zh-Hans&unit=c'
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

# 获取室外温度
def get_outside_weather_now():
    place_weather = {
        'text': '--',
        'code': '0',
        'temperature': '0'
    }
    try:
        response = requests.get(WEATHER_URL, timeout=5)
        response.raise_for_status()  # 检查请求是否成功（状态码为200-299）

        # 如果请求成功，处理响应数据
        res = response.json()
        # print('成功获取数据:', res)
        now = res['results'][0]['now']
        return now
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
        " cpu_used_rate, sys_uptime, sys_runtime, weather, weather_code, outdoors_temp)"
        " values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        params)
    con.commit()
    cur.close()

def initialDataBaseHomePod():
    db_file2 = os.path.join(os.path.dirname(__file__), 'homepod.db')
    con = sqlite3.connect(db_file2)
    cur = con.cursor()
    cur.execute('''CREATE TABLE sensor(
                    id INTEGER PRIMARY KEY,
                    temperature NUMERIC,
                    humidity NUMERIC,
                    createDate DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    con.commit()
    cur.close()

def insertAHomePodRecord(params):
    db_file2 = os.path.join(os.path.dirname(__file__), 'homepod.db')
    con = sqlite3.connect(db_file2)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO sensor(temperature, humidity) values(?, ?)", params)
    con.commit()
    cur.close()

# 创建一个存储的db
def initialDataBase():
    db_file = os.path.join(os.path.dirname(__file__), 'surroundings.db')
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    # create user table
    cur.execute('''CREATE TABLE surroundings(
                    id INTEGER PRIMARY KEY,
                    location VARCHAR(50),
                    temperature NUMERIC,
                    humidity NUMERIC,
                    cup_temp NUMERIC,
                    cpu_used_rate NUMERIC,
                    sys_uptime VARCHAR(50),
                    sys_runtime INTEGER,
                    weather VARCHAR(50),
                    weather_code INTEGER,
                    outdoors_temp NUMERIC,
                    createDate DATETIME DEFAULT CURRENT_TIMESTAMP)''')
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
    weather_text = now_weather['text']
    weather_code = now_weather['code']
    weather_temp = now_weather['temperature']
    # print(f"室外天气: {now_weather}")
    #
    # print(f"记录的地点: {LOCATION}")
    # print(f"温湿度: {tem} {humi}")
    # print(f"CPU使用率: {cpu_usage}%")
    # print(f"系统开机时间: {system_uptime}")
    # print(f"CPU温度: {cpu_temperature}°C")
    # print(f"系统运行时间: {syste_runtime}")

    # 创建数据库
    # initialDataBase()

    insertARecord([LOCATION,
                   tem,
                   humi,
                   cpu_temperature,
                   cpu_usage,
                   system_uptime,
                   syste_runtime,
                   weather_text,
                   weather_code,
                   weather_temp
                   ])
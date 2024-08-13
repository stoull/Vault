import sqlite3, os, time, platform
import Adafruit_DHT
import psutil

DB_FILE = "/home/pi/Documents/PythonProjects/Vault/api/surroundings.db"

# DB_FILE = "/Users/hut/Documents/PythonProjects/Vault/api/surroundings.db"

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

    # 将秒数转换为天、小时、分钟和秒
    days = uptime_seconds // (24 * 3600)
    uptime_seconds %= (24 * 3600)
    hours = uptime_seconds // 3600
    uptime_seconds %= 3600
    minutes = uptime_seconds // 60
    seconds = uptime_seconds % 60

    # return days, hours, minutes, seconds
    resultStr = f"{int(minutes)}min {int(seconds)}sec"
    if int(hours) > 0:
        resultStr = f"{int(hours)}hours " + resultStr
    if int(days) > 0:
        resultStr = f"{int(days)}day " + resultStr
    return resultStr


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
                return "无法获取温度信息"
        except Exception as e:
            return str(e)
    else:
        return "此功能在非Linux系统上不可用"


def insertARecord(params):
    db_file = os.path.join(os.path.dirname(__file__), 'surroundings.db')
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    # cur.execute("INSERT INTO surroundings values(NULL, 'Hut', 'Stoull', 'chang@12.com', 1, '1214555', 'Buttflay', ?)", params)
    cur.execute(
        "INSERT INTO surroundings(temperature, humidity, cup_temp, cpu_used_rate, sys_uptime, sys_runtime) values(?, ?, ?, ?, ?, ?)",
        params)
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
                temperature NUMERIC,
                humidity NUMERIC,
                cup_temp NUMERIC,
                cpu_used_rate NUMERIC,
                sys_uptime VARCHAR(60),
                sys_runtime VARCHAR(60),
                createDate DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    con.commit()
    cur.close()


if __name__ == "__main__":
    # initialDataBase()
    # insertARecord([2.0, 4.0, '60%', 30, "2020:2220", "12days 32hours"])

    tem, humi = readTemAndHumidity()
    cpu_usage = get_cpu_usage()
    cpu_temperature = get_cpu_temperature()
    system_uptime = get_system_uptime()
    syste_runtime = get_system_run_duration()

    #     print(f"温湿度: {tem} {humi}")
    #     print(f"CPU使用率: {cpu_usage}%")
    #     print(f"系统开机时间: {system_uptime}")
    #     print(f"CPU温度: {cpu_temperature}°C")
    #     print(f"系统运行时间: {syste_runtime}")

    insertARecord([tem, humi, cpu_temperature, cpu_usage, system_uptime, syste_runtime])
import sqlite3, os, time, platform, json
import Adafruit_DHT
import psutil
from datetime import datetime, timezone, timedelta
import requests

import paho.mqtt.client as mqtt
import time
import json

DB_FILE = "/home/pi/Documents/PythonProjects/Vault/api/surroundings.db"
# DB_FILE = "/Users/hut/Documents/python-projects/Vault/api/surroundings.db"
# 心知天气 https://www.seniverse.com
# WEATHER_URL = 'https://api.seniverse.com/v3/weather/now.json?key=S4zs06GXMojuzjjUH&location=Shenzhen&language=zh-Hans&unit=c'
# open weather
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather?lat=22.63404&lon=113.81842&appid=20c7b818bbb2f911cda86ce2798a91b0&lang=zh'
LOCATION = 'HOME'   # 记录的位置信息，如卧室，办公室，厨房等
# LOCATION = 'OFFICE'   # 记录的位置信息，如卧室，办公室，厨房等

MQTT_BROKER = "43.138.214.161"
MQTT_PORT = 1883
MQTT_USERNAME = "hut"
MQTT_PASSWORD = "mqtt_hut_mos_8"
MQTT_TOPIC = "sensor/dht22/1/data"
MQTT_TOPIC_DEVICE_INFO = "device/system/1/device_info"

# 时区设置（根据实际情况调整）
TIMEZONE_OFFSET = timedelta(hours=8)  # 例如：东八区（UTC+8）
def get_iso8601_time_with_timezone():
    """
    获取ISO 8601格式的时间戳，包含时区信息
    格式: 2024-01-15T14:30:45+08:00
    """
    # 获取当前UTC时间
    utc_now = datetime.now(timezone.utc)

    # 转换为本地时间（带时区信息）
    local_now = utc_now.astimezone(timezone(TIMEZONE_OFFSET))

    # 格式化为ISO 8601格式
    return local_now.isoformat()

def readTemAndHumidity():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 9)

    return abnormalVaulueCheck(humidity, temperature)

def abnormalVaulueCheck(humidity, temperature):
    theLastTemp, theLastHumi, unusual_temp_count, unusual_hum_count = readTheLastInfo()
    if humidity and temperature:
        
        if humidity == 0 and temperature == 0:
            if theLastTemp and theLastHumi:
                return (theLastTemp, theLastHumi)
            else:
                return (0, 0)
        
        humi = round(humidity, 2)
        temp = round(temperature, 2)
        if theLastTemp is None: theLastTemp = temp
        if theLastHumi is None: theLastHumi = humi
        if unusual_temp_count is None: unusual_temp_count = 0
        if unusual_hum_count is None: unusual_hum_count = 0
        dTemp = 0
        dHumi = 0
        if theLastTemp is not None: dTemp = temp - theLastTemp
        if theLastHumi is not None: dHumi = humi - theLastHumi
        if abs(dTemp) > 3:
            unusual_temp_count+=1
            if unusual_temp_count > 5:
                unusual_temp_count=0
            else:
                temp = theLastTemp
        else:
            unusual_temp_count = 0
        if abs(dHumi) > 10:
            unusual_hum_count+=1
            if unusual_hum_count > 5:
                unusual_hum_count=0
            else:
                humi = theLastHumi
        else:
            unusual_hum_count = 0
        result = (temp, humi)
        writeTheLastInfo((temp, humi, unusual_temp_count, unusual_hum_count))
        return result
    else:
        if theLastTemp and theLastHumi:
            return (theLastTemp, theLastHumi)
        else:
            return (0, 0)

TheLastInfoFilePath = "/home/pi/Documents/PythonProjects/Vault/api/TheLastInfo.json"
def readTheLastInfo():
    try:
        with open(TheLastInfoFilePath, 'r') as json_file:
            data_read = json.load(json_file)
            return data_read['temp'], data_read['humi'], data_read['unusual_temp_count'], data_read['unusual_hum_count'],
    except FileNotFoundError as e:
         return None,None,None,None

def writeTheLastInfo(info):
    temp, humi, unusual_temp_count, unusual_hum_count = info
    data_to_write = {
        "temp": temp,
        "humi": humi,
        "unusual_temp_count": unusual_temp_count,
        "unusual_hum_count": unusual_hum_count,
    }
    with open(TheLastInfoFilePath, 'w') as json_file:
        json.dump(data_to_write, json_file, indent=4)

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

def postArecord(params):
    url = "https://ahut.site:8000/smart-clock/home_climate/record"
    payload = {"record": params}
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"插入一条记录成功: {response.json()}")
        return response.json()
    except requests.RequestException as e:
        print(f"插入一条记录失败: str(e)")
        return {"result": 0, "message": str(e)}

def create_mqtt_client():
    """创建并配置MQTT客户端（使用Callback API V2）"""
    # 方法1：使用回调API版本2
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # 方法2：或者直接指定版本号为2
    # client = mqtt.Client(callback_api_version=2)

    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    return client

# 获取设备信息 下面 - 上面引入过了
# import time
# import psutil
# import platform
# import os

import sys
import uuid
import socket
import struct
import fcntl
import netifaces
import subprocess
import re

def get_unique_id():
    """
    获取 Raspberry Pi 的 CPU 序列号作为唯一ID
    """
    try:
        # 方法1：从 /proc/cpuinfo 读取
        with open('/proc/cpuinfo', 'r') as f:
            for line in f: 
                if line.startswith('Serial'):
                    serial = line.split(':')[1].strip()
                    # 移除开头的0或其他填充字符
                    return serial.lstrip('0') if serial != '0' * len(serial) else serial
    except Exception: 
        pass
    
    try: 
        # 方法2：从 devicetree 读取（某些系统）
        with open('/sys/firmware/devicetree/base/serial-number', 'r') as f:
            serial = f.read().strip().rstrip('\x00')
            return serial
    except Exception:
        pass
    
    # 备用方案：使用 MAC 地址
    try:
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return mac
    except Exception:  
        pass
    
    return ''

def get_os_version():
    """
    获取 Linux 系统名称和版本
    """
    try:
        # 优先从 /etc/os-release 读取（最标准的方式）
        with open('/etc/os-release', 'r') as f:
            os_info = {}
            for line in f: 
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os_info[key] = value.strip('"')
            
            # 优先使用 PRETTY_NAME，否则组合 NAME 和 VERSION
            if 'PRETTY_NAME' in os_info:
                return os_info['PRETTY_NAME']
            elif 'NAME' in os_info and 'VERSION' in os_info:
                return f"{os_info['NAME']} {os_info['VERSION']}"
            elif 'NAME' in os_info:
                return os_info['NAME']
    except Exception:
        pass
    
    try:
        # 备用方案：使用 platform 模块
        return platform.platform()
    except Exception:
        pass
    
    return ''

def get_rssi(iface='wlan0'):
    """
    获取指定接口的Wi-Fi信号强度（RSSI，单位dBm），失败时返回空字符串
    """
    try:
        result = subprocess.check_output(['iwconfig', iface], stderr=subprocess.DEVNULL).decode()
        m = re.search(r'Signal level=(-?\d+) dBm', result)
        if m:
            return int(m.group(1))
    except Exception:
        pass
    return ''

def get_network_info():
    """
    获取网络信息（以 eth0 或 wlan0 为主）
    Returns: 
        dict: {'ip', 'subnet', 'gateway', 'dns', 'rssi', 'mac'}
    """
    info = {'ip': '', 'subnet': '', 'gateway':  '', 'dns': '', 'rssi': '', 'mac':  ''}
    iface_priority = ['wlan0', 'eth0', 'en0']

    iface = ''
    for i in iface_priority: 
        if i in netifaces.interfaces():
            iface = i
            break
    if not iface:
        ifaces = netifaces.interfaces()
        if ifaces:
            iface = ifaces[0]

    if iface:
        addrs = netifaces.ifaddresses(iface)
        # IPv4
        ipinfo = addrs.get(netifaces.AF_INET, [{}])[0]
        info['ip'] = ipinfo.get('addr', '')
        info['subnet'] = ipinfo.get('netmask', '')
        # Gateway
        gateways = netifaces.gateways()
        gw = gateways.get('default', {}).get(netifaces.AF_INET, [''])
        info['gateway'] = gw[0] if gw else ''
        # DNS
        dns_list = []
        try: 
            with open('/etc/resolv.conf') as f:
                for line in f:
                    if line.startswith('nameserver'):
                        dns_list.append(line.strip().split()[1])
            info['dns'] = ','.join(dns_list)
        except Exception:
            info['dns'] = ''
        # MAC
        try:
            mac_bytes = netifaces.ifaddresses(iface)[netifaces.AF_LINK][0]['addr']
            info['mac'] = mac_bytes
        except:
            info['mac'] = ''
        # RSSI
        if iface.startswith('wlan'):
            info['rssi'] = get_rssi(iface)
        else:
            info['rssi'] = ''
    return info

def get_memory_info():
    vm = psutil.virtual_memory()
    info = {
        'total': vm.total,
        'used': vm.used,
        'free': vm.available,
        'usage_percent': vm.percent,
    }
    return info

def get_cpu_temperature():
    # 尝试读取树莓派温度
    try:
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            temp_str = f.read().strip()
        return float(temp_str) / 1000
    except Exception: 
        return 0.0

def get_cpu_frequency():
    """
    获取 CPU 当前频率（MHz）
    """
    try: 
        # 读取当前频率（单位：KHz）
        with open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq', 'r') as f:
            freq_khz = int(f.read().strip())
            return freq_khz // 1000  # 转换为 MHz
    except Exception:
        pass
    
    try:
        # 读取最大频率作为备用（单位：KHz）
        with open('/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq', 'r') as f:
            freq_khz = int(f.read().strip())
            return freq_khz // 1000  # 转换为 MHz
    except Exception:
        pass
    
    return ''

def get_device_info_all():
    all_info = {}
    
    # unique_id: 获取 Raspberry Pi CPU 序列号
    all_info['unique_id'] = get_unique_id()
    
    all_info['platform'] = sys.platform if hasattr(sys, "platform") else platform.system()
    
    # os_version:  获取 Linux 系统名称和版本
    all_info['os_version'] = get_os_version()
    
    # CPU frequency (MHz)
    all_info['cpu_frequency_mhz'] = get_cpu_frequency()
    
    # CPU temp
    all_info['cpu_temperature'] = round(get_cpu_temperature(), 2)
    
    # Storage info
    st = os.statvfs('/')
    total = st.f_frsize * st.f_blocks
    free = st.f_frsize * st.f_bavail
    used = total - free
    all_info['total_storage_bytes'] = total
    all_info['used_storage_bytes'] = used
    all_info['free_storage_bytes'] = free
    all_info['storage_usage_percent'] = round(used / total * 100, 1) if total > 0 else 0
    
    # Memory info
    memory_info = get_memory_info()
    all_info['total_memory_bytes'] = memory_info['total']
    all_info['used_memory_bytes'] = memory_info['used']
    all_info['free_memory_bytes'] = memory_info['free']
    all_info['memory_usage_percent'] = memory_info['usage_percent']
    
    # Uptime
    try:
        all_info['uptime_seconds'] = int(time.time() - psutil.boot_time())
    except Exception:
        all_info['uptime_seconds'] = ''
    
    # Reset cause (Linux下只能大致识别)
    # 0: 正常上电，1: 看门狗，9: 其他
    all_info['reset_reason'] = 9
    return all_info

def publish_device_info_data():
    """读取设备信息并发到 MQTT"""
    
    # 读取设备信息
    d_info = get_device_info_all()
    d_info['created_at'] = get_iso8601_time_with_timezone()
    
    # 读取网络信息
    net_info = get_network_info()
    if net_info:
        d_info.update(net_info)
    
    if d_info is None:
        # log_error("设备信息读取失败")
        return False
    
    return d_info
# 获取设备信息 上面

def publish_dht22_data(data):
    """连接、发布数据、断开连接"""
    client = None
    try:
        if not data:
            return False

        # 2. 创建MQTT客户端
        client = create_mqtt_client()

        # 3. 连接MQTT服务器（设置连接超时）
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 正在连接MQTT服务器...")
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)

        # 4. 发布数据（使用阻塞方式，确保发布完成）
        client.loop_start()  # 启动后台线程
        time.sleep(0.1)  # 等待连接建立

        json_data = json.dumps(data)
        result = client.publish(MQTT_TOPIC, json_data, qos=1)

        # 等待发布完成
        result.wait_for_publish(timeout=20.0)

        device_info = publish_device_info_data()
        if device_info:
            json_device_info = json.dumps(device_info)
            result1 = client.publish(MQTT_TOPIC_DEVICE_INFO, json_device_info, qos=1)
            result1.wait_for_publish(timeout=20.0)

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 成功发布: {json_data}")
            return True
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 发布失败")
            return False

    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] MQTT操作错误: {e}")
        return False

    finally:
        # 5. 清理资源
        if client:
            try:
                client.loop_stop()
                client.disconnect()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] MQTT连接已断开")
            except:
                pass

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

    params = [LOCATION,
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
                   ]
    insertARecord(params)
    postArecord(params)

    mqtt_data = {
        "created_at": get_iso8601_time_with_timezone(),
        "temperature": tem,
        "humidity": humi,
    }
    publish_dht22_data(mqtt_data)

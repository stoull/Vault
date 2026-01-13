# 上面引入过了
import time
import psutil
import platform
import os

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

# 示例用法
if __name__ == '__main__':
    result = publish_device_info_data()
    print("设备信息：")
    for key, value in result.items():
        print(f"{key}: {value}")
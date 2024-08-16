
import sqlite3, os, time, platform
from datetime import datetime
import pytz

from .surrounding_monitor import readTemAndHumidity, DB_FILE

KEYLIST = ["id", "location", "temperature", "humidity", "cup_temp",
		   "cpu_used_rate", "sys_uptime", "sys_runtime", "weather",
		   "weather_code", "outdoors_temp", "createDate"]

def readTemAndHumidity():
    return readTemAndHumidity()

def readTheLastRecord():
	db_file = os.path.join(os.path.dirname(__file__), 'surroundings.db')
	con = sqlite3.connect(DB_FILE)
	cur = con.cursor()
	cur.execute("SELECT * FROM surroundings ORDER BY id DESC LIMIT 1 OFFSET 0;")
	datas = []

	for data in cur.fetchall():
		itemDic = {}
		for i in range(0, len(KEYLIST)):
			key = KEYLIST[i]
			itemDic[key] = data[i]
		datas.append(itemDic)
	con.commit()
	cur.close()
	return itemDic

def readTheLastEightHoursRecord():
	db_file = os.path.join(os.path.dirname(__file__), 'surroundings.db')
	con = sqlite3.connect(DB_FILE)
	cur = con.cursor()
	cur.execute("SELECT * FROM surroundings ORDER BY id DESC LIMIT 288 OFFSET 0;")
	datas = []

	for data in cur.fetchall():
		itemDic = {}
		for i in range(0, len(KEYLIST)):
			key = KEYLIST[i]
			itemDic[key] = data[i]
			if key is 'createDate':
				utc_time_str = data[i]
				naive_datetime = datetime.strptime(utc_time_str, '%Y-%m-%d %H:%M:%S')
				# 创建 UTC 时区对象
				utc_timezone = pytz.utc
				# 将 naive datetime 转换为 UTC datetime
				utc_datetime = utc_timezone.localize(naive_datetime)
				target_timezone = pytz.timezone('Asia/Shanghai')
				local_time = utc_datetime.astimezone(target_timezone)
				itemDic[key] = local_time
		datas.append(itemDic)
	con.commit()
	cur.close()

	temperatures = [item_d["temperature"] for item_d in datas]
	humidities = [item_d["humidity"] for item_d in datas]
	cup_temps = [item_d["cup_temp"] for item_d in datas]
	cpu_used_rates = [item_d["cpu_used_rate"] for item_d in datas]
	createDates = [item_d["createDate"].strftime("%H:%M") for item_d in datas]

	temperatures.reverse()
	humidities.reverse()
	cup_temps.reverse()
	cpu_used_rates.reverse()
	createDates.reverse()

	return {
		"labels": createDates,
		"temp": temperatures,
		"humi": humidities,
		"cuptemp": cup_temps,
		"cpu_used_rates": cpu_used_rates
	}

def insertAHomePodRecord(params):
	db_file2 = os.path.join(os.path.dirname(__file__), 'homepod.db')
	con = sqlite3.connect(db_file2)
	cur = con.cursor()
	cur.execute(
		"INSERT INTO sensor(temperature, humidity) values(?, ?)", params)
	con.commit()
	cur.close()

def readHomePodRecord():
	db_file2 = os.path.join(os.path.dirname(__file__), 'homepod.db')
	con = sqlite3.connect(db_file2)
	cur = con.cursor()
	cur.execute("SELECT * FROM sensor ORDER BY id DESC LIMIT 20 OFFSET 0;")
	datas = []

	home_pod_keys = ["id", "temperature", "humidity", "createDate"]
	for data in cur.fetchall():
		itemDic = {}
		for i in range(0, len(home_pod_keys)):
			key = home_pod_keys[i]
			itemDic[key] = data[i]
			if key is 'createDate':
				utc_time_str = data[i]
				naive_datetime = datetime.strptime(utc_time_str, '%Y-%m-%d %H:%M:%S')
				# 创建 UTC 时区对象
				utc_timezone = pytz.utc
				# 将 naive datetime 转换为 UTC datetime
				utc_datetime = utc_timezone.localize(naive_datetime)
				target_timezone = pytz.timezone('Asia/Shanghai')
				local_time = utc_datetime.astimezone(target_timezone)
				itemDic[key] = local_time
		datas.append(itemDic)
	con.commit()
	cur.close()
	return {
		"data": datas
	}

def readTheLastTemAndHumidity():
	result = readTheLastRecord()
	return (result['temperature'], result['humidity'])

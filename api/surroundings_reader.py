
import sqlite3, os, time, platform
from datetime import datetime
from .api_helper import is_date_format_valid
import pytz

from .surrounding_monitor import readTemAndHumidity, DB_FILE

KEYLIST = ["id", "location", "temperature", "humidity", "cup_temp",
		   "cpu_used_rate", "sys_uptime", "sys_runtime", "weather", "weather_code",
		   "weather_des", "weather_icon",  "outdoors_temp", "outdoors_feels_like",
		   "outdoors_temp_min", "outdoors_temp_max", "outdoors_pressure", "outdoors_humidity", "createDate"]

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

def readRecordsWithPeriod(startDate, endDate):
	if not is_date_format_valid(startDate)  or not is_date_format_valid(endDate):
		return {
		"labels": [],
		"temp": [],
		"humi": [],
		"cuptemp": [],
		"cpu_used_rates": []
		}

	selectSQL = f"""
	    SELECT *
	    FROM (
	        SELECT *, DATETIME(createDate, '+8 hours') AS localTime
	        FROM surroundings
	    )
	    WHERE localTime BETWEEN '{startDate}' AND '{endDate}';
	"""
	db_file = os.path.join(os.path.dirname(__file__), 'surroundings.db')
	con = sqlite3.connect(DB_FILE)
	cur = con.cursor()
	cur.execute(selectSQL)
	datas = []

	for data in cur.fetchall():
		itemDic = {}
		for i in range(0, len(KEYLIST)):
			key = KEYLIST[i]
			itemDic[key] = data[i]
			if key is 'createDate':
				time_str = data[i]
				if '.' in time_str:
					naive_datetime = datetime.fromisoformat(time_str)  # 包含微秒的情况
				else:
					naive_datetime = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")  # 不包含微秒的情况
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

	return {
		"labels": createDates,
		"temp": temperatures,
		"humi": humidities,
		"cuptemp": cup_temps,
		"cpu_used_rates": cpu_used_rates
	}

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
				time_str = data[i]
				if '.' in time_str:
					naive_datetime = datetime.fromisoformat(time_str)  # 包含微秒的情况
				else:
					naive_datetime = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")  # 不包含微秒的情况
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

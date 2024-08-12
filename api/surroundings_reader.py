
import sqlite3, os, time, platform

from .surrounding_monitor import readTemAndHumidity, DB_FILE

def readTemAndHumidity():
    return readTemAndHumidity()

def readTheLastRecord():
	db_file = os.path.join(os.path.dirname(__file__), 'surroundings.db')
	con = sqlite3.connect(DB_FILE)
	cur = con.cursor()
	cur.execute("SELECT * FROM surroundings ORDER BY id DESC LIMIT 1 OFFSET 0;")
	datas = []

	for data in cur.fetchall():
		keyList = ["id", "temperature", "humidity", "cup_temp", "cpu_used_rate", "sys_uptime", "sys_runtime", "createDate"]
		itemDic = {}
		for i in range(0, len(keyList)):
			key = keyList[i]
			itemDic[key] = data[i]
		datas.append(itemDic)
	con.commit()
	cur.close()
	return itemDic

def readTheLastTemAndHumidity():
	result = readTheLastRecord()
	return (result['temperature'], result['humidity'])

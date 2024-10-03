import sqlite3, os

DB_FILE = "/home/pi/Documents/PythonProjects/Vault/api/surroundings.db"
# DB_FILE = "/Users/hut/Documents/PythonProjects/Vault/api/surroundings.db"
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

# 创建一个存储的db
def initSurroundingsDataBase():
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
                    weather_des VARCHAR(50),
                    weather_icon VARCHAR(10),
                    outdoors_temp NUMERIC,
                    outdoors_feels_like NUMERIC,
                    outdoors_temp_min NUMERIC,
                    outdoors_temp_max NUMERIC,
                    outdoors_pressure NUMERIC,
                    outdoors_humidity NUMERIC,
                    createDate DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    con.commit()
    cur.close()

def initAirConditionerDataBase():
    db_file = os.path.join(os.path.dirname(__file__), 'surroundings.db')
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute('''CREATE TABLE airconditioner(
                    id INTEGER PRIMARY KEY,
                    location VARCHAR(50),
                    temperature NUMERIC,
                    model INTEGER,
                    description VARCHAR(50),
                    createDate DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    con.commit()
    cur.close()

def initHomePodDataBase():
    db_file = os.path.join(os.path.dirname(__file__), 'surroundings.db')
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute('''CREATE TABLE homepod(
                    id INTEGER PRIMARY KEY,
                    temperature NUMERIC,
                    humidity NUMERIC,
                    createDate DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    con.commit()
    cur.close()

def initScreenLogDataBase():
    db_file = os.path.join(os.path.dirname(__file__), 'surroundings.db')
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute('''CREATE TABLE screen_log(
                    id INTEGER PRIMARY KEY,
                    action BOOLEAN,
                    createDate DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    con.commit()
    cur.close()

def initNoteDataBase():
    db_file = os.path.join(os.path.dirname(__file__), 'surroundings.db')
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute('''CREATE TABLE note(
                    id INTEGER PRIMARY KEY,
                    note VARCHAR(200),
                    createDate DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    con.commit()
    cur.close()

def initFridgeDataBase():
    db_file = os.path.join(os.path.dirname(__file__), 'surroundings.db')
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute('''CREATE TABLE fridge(
                    id INTEGER PRIMARY KEY,
                    tag VARCHAR(50),
                    temperature NUMERIC,
                    humidity NUMERIC,
                    createDate DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    con.commit()
    cur.close()

if __name__ == "__main__":
    # initHomePodDataBase()
    # initScreenLogDataBase()
    # initNoteDataBase()
    initFridgeDataBase()

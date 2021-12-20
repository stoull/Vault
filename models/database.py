import sqlite3, os, hashlib, time, sys

# from flask_sqlalchemy import SQLAlchemy, Model

class DBManager(object):
	"""Sqlite databse manager"""
	def __init__(self):
		self.db_file = "vault.db"
		self.initialDataBase()
		self.connect = sqlite3.connect(self.db_file)

	# 判断一个文件是否是SQLite3文件
	def isSQLite3File(self, filePath):
		if os.path.isfile(filePath):
			if os.path.getsize(filePath) > 100:
				with open(filePath, 'r', encoding = "ISO-8859-1") as f:
					header = f.read(100)
					if header.startswith('SQLite format 3'):
						# SQlite3 database has been detected
						return True
		return False

	# 建表及其关系
	def initialDataBase(self):
		db_file = os.path.join(os.path.dirname(__file__), 'vault.db')
		if self.isSQLite3File(db_file) == False:
			con = sqlite3.connect(db_file)
			cur = con.cursor()
			# create user table
			cur.execute('''CREATE TABLE user(
				id INTEGER PRIMARY KEY,
 				name VARCHAR(20) NOT NULL,
 				alias VARCHAR(20), 
 				email VARCHAR(20),
 				gender INT DEFAULT 0,
 				phoneNumber VARCHAR(20),
 				introduction TEXT,
 				createDate DATETIME DEFAULT CURRENT_TIMESTAMP)''')
			
			# create movie table
			cur.execute('''CREATE TABLE movie(
				id INTEGER PRIMARY KEY,
 				name VARCHAR(40) NOT NULL,
 				releaseDate DATETIME,
 				language VARCHAR(20),
 				length REAL,
 				otherNames VARCHAR(100),
 				score INT,
 				synopsis TEXT,
 				filePath VARCHAR(100),
 				fileUrl VARCHAR(100),
 				posterUrl VARCHAR(100),
 				iconUrl VARCHAR(100),
 				createDate DATETIME DEFAULT CURRENT_TIMESTAMP,
 				lastWatchDate DATETIME,
 				lastWatchUser VARCHAR(40))''')

			cur.execute('''CREATE TABLE director(
				id INTEGER PRIMARY KEY,
				name_cn VARCHAR(40) NOT NULL,
				name_en VARCHAR(40),
				gender BOOLEAN,
				birthday DATETIME,
				birthplace VARCHAR(20)
				)''')

			cur.execute('''CREATE TABLE actor(
				id INTEGER PRIMARY KEY,
				name_cn VARCHAR(40) NOT NULL,
				name_en VARCHAR(40),
				gender BOOLEAN,
				birthday DATETIME,
				birthplace VARCHAR(20)
				)''')

			cur.execute('''CREATE TABLE scenarist(
				id INTEGER PRIMARY KEY,
				name_cn VARCHAR(40) NOT NULL,
				name_en VARCHAR(40),
				gender BOOLEAN,
				birthday DATETIME,
				birthplace VARCHAR(20)
				)''')

			cur.execute('''CREATE TABLE area(
				id INTEGER PRIMARY KEY,
				name VARCHAR(20)
				)''')

			cur.execute('''CREATE TABLE type(
				id INTEGER PRIMARY KEY,
				name VARCHAR(40)
				)''')

			cur.execute('''CREATE TABLE tag(
				id INTEGER PRIMARY KEY,
				name VARCHAR(40)
				)''')

			cur.execute('''CREATE TABLE movie_director(
				movie_id INTEGER ,
				director_id INTEGER,
				CONSTRAINT FK_movie_id FOREIGN KEY (movie_id) REFERENCES movie(id),
				CONSTRAINT FK_director_id FOREIGN KEY (director_id) REFERENCES director(id)
				)''')

			cur.execute('''CREATE TABLE movie_actor(
				movie_id INTEGER,
				actor_id INTEGER,
				CONSTRAINT FK_movie_id FOREIGN KEY (movie_id) REFERENCES movie(id),
				CONSTRAINT FK_actor_id FOREIGN KEY (actor_id) REFERENCES actor(id)
				)''')

			cur.execute('''CREATE TABLE movie_scenarist(
				movie_id INTEGER,
				sscenarist_id INTEGER,
				CONSTRAINT FK_movie_id FOREIGN KEY (movie_id) REFERENCES movie(id),
				CONSTRAINT FK_scenarist_id FOREIGN KEY (sscenarist_id) REFERENCES scenarist(id)
				)''')

			cur.execute('''CREATE TABLE movie_area(
				movie_id INTEGER,
				area_id INTEGER,
				CONSTRAINT FK_movie_id FOREIGN KEY (movie_id) REFERENCES movie(id),
				CONSTRAINT FK_area_id FOREIGN KEY (area_id) REFERENCES area(id)
				)''')

			cur.execute('''CREATE TABLE movie_tag(
				movie_id INTEGER,
				tag_id INTEGER,
				CONSTRAINT FK_movie_id FOREIGN KEY (movie_id) REFERENCES movie(id),
				CONSTRAINT FK_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id)
				)''')

			cur.execute('''CREATE TABLE movie_type(
				movie_id INTEGER,
				tppe_id INTEGER,
				CONSTRAINT FK_movie_id FOREIGN KEY (movie_id) REFERENCES movie(id),
				CONSTRAINT FK_type_id FOREIGN KEY (tppe_id) REFERENCES type(id)
				)''')

			con.commit()
			cur.close()
			self.db_file = db_file
			self.connect = con

	# 增加一些测试的用户数据
	def insertUser(self):
		cur = self.connect.cursor()
		params = [int(time.time())]
		cur.execute("insert into user values(NULL, 'Hut', 'Stoull', 'chang@12.com', 1, '1214555', 'Buttflay', ?)", params)
		cur.execute("insert into user(name, alias, email, gender, phoneNumber, introduction) values('Kevin', 'Stoull', 'chang@12.com', 1, '1214555', 'Buttflay')")


	def closeDataBase(self):
		self.connect.commit()
		self.connect.close()

	def getAllTableNames(self):
		newConnect = sqlite3.connect(self.db_file)
		cur = newConnect.cursor()
		cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
		tables = []
		for tableName in cur.fetchall():
			tables.append(tableName[0])
		newConnect.close()
		return tables



if __name__=='__main__':
	db = DBManager()
	tables = db.getAllTableNames()
	print(f"is reandTAlbes: {tables}")
	# db.insertUser()
	# db.closeDataBase()
	



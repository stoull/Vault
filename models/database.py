import sqlite3, os, hashlib, time, sys

# from flask_sqlalchemy import SQLAlchemy, Model

class DBManager(object):
	"""Sqlite databse manager"""
	def __init__(self):
		self.db_file = "vault.db"
		self.initialDataBase()

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
            name VARCHAR(200) NOT NULL,
            directors VARCHAR(200),
            scenarists VARCHAR(200),
            actors VARCHAR(400),
            style VARCHAR(60),
            year INTEGER,
            releaseDate VARCHAR(200),
            area VARCHAR(120),
            language VARCHAR(60),
            length INTEGER,
            otherNames VARCHAR(100),
            score NUMERIC,
            synopsis TEXT,
            imdb VARCHAR(20),
            doubanUrl VARCHAR(250),
            posterUrl VARCHAR(250),
            iconUrl VARCHAR(250),
            filePath VARCHAR(250),
            fileUrl VARCHAR(250),
            createDate DATETIME DEFAULT CURRENT_TIMESTAMP,
            lastWatchDate DATETIME,
            lastWatchUser VARCHAR(40))''')

            cur.execute('''CREATE TABLE director(
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            gender BOOLEAN,
            zodiac VARCHAR(10),
            livingTime VARCHAR(100),
            birthday INTEGER,
            leaveday INTEGER,
            birthplace VARCHAR(100),
            occupation VARCHAR(100),
            names_cn VARCHAR(300),
            names_en VARCHAR(300),
            family VARCHAR(200),
            imdb VARCHAR(20),
            intro TEXT,
            photoUrl VARCHAR(250)
            )''')

            cur.execute('''CREATE TABLE actor(
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            gender BOOLEAN,
            zodiac VARCHAR(10),
            livingTime VARCHAR(100),
            birthday INTEGER,
            leaveday INTEGER,
            birthplace VARCHAR(100),
            occupation VARCHAR(100),
            names_cn VARCHAR(300),
            names_en VARCHAR(300),
            family VARCHAR(200),
            imdb VARCHAR(20),
            intro TEXT,
            photoUrl VARCHAR(250)
            )''')

            cur.execute('''CREATE TABLE scenarist(
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            gender BOOLEAN,
            zodiac VARCHAR(10),
            livingTime VARCHAR(100),
            birthday INTEGER,
            leaveday INTEGER,
            birthplace VARCHAR(100),
            occupation VARCHAR(100),
            names_cn VARCHAR(300),
            names_en VARCHAR(300),
            family VARCHAR(200),
            imdb VARCHAR(20),
            intro TEXT,
            photoUrl VARCHAR(250)
            )''')

            cur.execute('''CREATE TABLE area(
            id INTEGER PRIMARY KEY,
            name VARCHAR(20) NOT NULL,
            unique (name)
            )''')

            cur.execute('''CREATE TABLE type(
            id INTEGER PRIMARY KEY,
            name VARCHAR(40) NOT NULL,
            unique (name)
            )''')

            cur.execute('''CREATE TABLE tag(
            id INTEGER PRIMARY KEY,
            name VARCHAR(40) NOT NULL,
            unique (name)
            )''')

			cur.execute('''CREATE TABLE language(
	            id INTEGER PRIMARY KEY,
	            name VARCHAR(30) NOT NULL,
	            unique (name)
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
            scenarist_id INTEGER,
            CONSTRAINT FK_movie_id FOREIGN KEY (movie_id) REFERENCES movie(id),
            CONSTRAINT FK_scenarist_id FOREIGN KEY (scenarist_id) REFERENCES scenarist(id)
            )''')

            cur.execute('''CREATE TABLE movie_area(
            movie_id INTEGER,
            area_id INTEGER,
            CONSTRAINT FK_movie_id FOREIGN KEY (movie_id) REFERENCES movie(id),
            CONSTRAINT FK_area_id FOREIGN KEY (area_id) REFERENCES area(id)
            )''')

            cur.execute('''CREATE TABLE movie_type(
            movie_id INTEGER,
            type_id INTEGER,
            CONSTRAINT FK_movie_id FOREIGN KEY (movie_id) REFERENCES movie(id),
            CONSTRAINT FK_type_id FOREIGN KEY (type_id) REFERENCES type(id)
            )''')

            cur.execute('''CREATE TABLE movie_tag(
            movie_id INTEGER,
            tag_id INTEGER,
            CONSTRAINT FK_movie_id FOREIGN KEY (movie_id) REFERENCES movie(id),
            CONSTRAINT FK_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id)
            )''')

            cur.execute('''CREATE TABLE movie_language(
            movie_id INTEGER,
            language_id INTEGER,
            CONSTRAINT FK_movie_id FOREIGN KEY (movie_id) REFERENCES movie(id),
            CONSTRAINT FK_language_id FOREIGN KEY (language_id) REFERENCES language(id)
            )''')

            cur.execute('''CREATE TABLE diector_area(
            diector_id INTEGER,
            area_id INTEGER,
            CONSTRAINT FK_diector_id FOREIGN KEY (diector_id) REFERENCES diector(id),
            CONSTRAINT FK_type_id FOREIGN KEY (area_id) REFERENCES area(id)
            )''')

            cur.execute('''CREATE TABLE scenarist_area(
            scenarist_id INTEGER,
            area_id INTEGER,
            CONSTRAINT FK_diector_id FOREIGN KEY (scenarist_id) REFERENCES scenarist(id),
            CONSTRAINT FK_type_id FOREIGN KEY (area_id) REFERENCES area(id)
            )''')

            cur.execute('''CREATE TABLE actor_area(
            actor_id INTEGER,
            area_id INTEGER,
            CONSTRAINT FK_diector_id FOREIGN KEY (actor_id) REFERENCES actor(id),
            CONSTRAINT FK_type_id FOREIGN KEY (area_id) REFERENCES area(id)
            )''')
            
			con.commit()
			cur.close()

	# 增加一些测试的用户数据
	def insertUser(self):
		con = sqlite3.connect(self.db_file)
		cur = con.cursor()
		params = [int(time.time())]
		cur.execute("insert into user values(NULL, 'Hut', 'Stoull', 'chang@12.com', 1, '1214555', 'Buttflay', ?)", params)
		cur.execute("insert into user(name, alias, email, gender, phoneNumber, introduction) values('Kevin', 'Stoull', 'chang@12.com', 1, '1214555', 'Buttflay')")
		con.commit()
		cur.close()

	def closeDataBase(self):
		self.connect.commit()
		self.connect.close()

	def getAllTableNames(self):
		con = sqlite3.connect(self.db_file)
		cur = con.cursor()
		cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
		tables = []
		for tableName in cur.fetchall():
			tables.append(tableName[0])
			return ["in here"]
		return [tables]
		con.commit()
		cur.close()



if __name__=='__main__':
	db = DBManager()
	tables = db.getAllTableNames()
	# db.insertUser()
	# db.closeDataBase()
	



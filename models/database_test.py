import sqlite3, os, hashlib, time, sys

# from flask_sqlalchemy import SQLAlchemy, Model

class DBManager(object):
	"""Sqlite databse manager"""
	def __init__(self):
		self.db_file = "vault.db"
		self.connect = sqlite3.connect(self.db_file)
		self.initialDataBase()

	def isSQLite3File(self, filePath):
		if os.path.isfile(filePath):
			if os.path.getsize(filePath) > 100:
				with open(filePath, 'r', encoding = "ISO-8859-1") as f:
					header = f.read(100)
					if header.startswith('SQLite format 3'):
						# SQlite3 database has been detected
						return True
		return False

	def initialDataBase(self):
		db_file = os.path.join(os.path.dirname(__file__), 'vault.db')
		if self.isSQLite3File(db_file) == False:
			con = sqlite3.connect(db_file)
			cur = con.cursor()
			# create user table
			cur.execute('''CREATE TABLE user(
							id INTEGER PRIMARY KEY,
			 				name VARCHAR(20),
			 				alias VARCHAR(20), 
			 				email VARCHAR(20),
			 				gender INT DEFAULT 0,
			 				phoneNumber VARCHAR(20),
			 				introduction TEXT,
			 				createDate DATETIME DEFAULT CURRENT_TIMESTAMP)''')
			
			#cureate director table
			cur.execute('''CREATE TABLE director(
						id INTEGER PRIMARY KEY,
						name VARCHAR(40),
						country VARCHAR(20)
						)''')

			# create movie table
			cur.execute('''CREATE TABLE movie(
							id INTEGER PRIMARY KEY,
			 				name VARCHAR(40),
			 				directorId INTEGER,
			 				FOREIGN KEY (directorId) REFERENCES director (id)
			 				)''')
			con.commit()
			cur.close()
			self.db_file = db_file
			self.connect = con

	def insertUser(self):
		cur = self.connect.cursor()
		params = [int(time.time())]
		# insert a user
		cur.execute("insert into user(name, alias, email, gender, phoneNumber, introduction) values('Kevin', 'Stoull', 'chang@12.com', 1, '1214555', 'Buttflay')")
		# insert directors


	def closeDataBase(self):
		self.connect.commit()
		self.connect.close()


if __name__=='__main__':
	db = DBManager()
	db.insertUser()
	db.closeDataBase()
	



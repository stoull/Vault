import os, sqlite3

db_file = os.path.join(os.path.dirname(__file__), 'test.db')
if os.path.isfile(db_file):
	os.remove(db_file)

#初始数据
con = sqlite3.connect(db_file)
cursor = con.cursor()
cursor.execute('''create table user(id VARCHAR(20) primary key, name VARCHAR(20), score INT)''')
cursor.execute("insert into user values('A-001', 'Adam', 95)")
cursor.execute("insert into user values('A-002', 'Bart', 62)")
cursor.execute("insert into user values('A-023', 'Kevin', 78)")

cursor.close()
con.commit()
con.close()

def get_score_in(low, high):
	con = sqlite3.connect(db_file)
	cur = con.cursor()
	cur.execute("SELECT name, score FROM user WHERE score>? AND score<? ORDER BY score DESC", (low, high))
	result = cur.fetchall()
	cur.close()
	con.close()
	return result

for name in get_score_in(60, 90):
	print(name)

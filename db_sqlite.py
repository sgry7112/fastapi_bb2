import sqlite3

conn = sqlite3.connect('./db.sqlite3')
c = conn.cursor()

sql = 'CREATE TABLE SATORU (id integer primary key, 時刻 datetime, 内容 text) ;'
c.execute(sql)

# sql = 'DROP TABLE SATORU'
# c.execute(sql)
# conn.commit()

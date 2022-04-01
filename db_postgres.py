# import os
# import psycopg2
# import pandas as pd

# DATABASE_URL = 'postgres://qwosamqjhsmjse:bdc36cd41f29cad53b026230c202df7ff08f34b0a1ede8a6334f134cc146f45f@ec2-44-194-92-192.compute-1.amazonaws.com:5432/d79ilntrh62i11'
# conn = psycopg2.connect(DATABASE_URL)
# cur = conn.cursor()

# # sql = '''
# # CREATE TABLE HISTORY (
# #     ID SERIAL NOT NULL,
# #     学習者 TEXT NOT NULL,
# #     学習日 TIMESTAMP NOT NULL,
# #     再生回数 INTEGER NOT NULL,
# #     PRIMARY KEY (ID)
# # );
# # '''


# # sql = '''
# # CREATE TABLE ITERATION (
# #     ID SERIAL NOT NULL,
# #     学習者 TEXT NOT NULL,
# # '''
# # for i in ["spade_", "club_", "dia_", "heart_"]:
# #     for j in range(1, 17):
# #         sql += f"    {i}{str(j).zfill(2)} INTEGER ,\n"

# # sql = sql[:-2] + ' );'


# # # sql = '''
# # # insert into articles (id, title, url) values(1, 'test', 'test-url')
# # # '''

# sql = 'select * from history'
# df = pd.read_sql(sql, conn)
# print(df)


# # cur.execute(sql)
# # conn.commit()

# # cur.close()
# # conn.close()

# from sqlalchemy import Column, String, DateTime, ForeignKey
# from sqlalchemy.sql.functions import current_timestamp
# from sqlalchemy.dialects.mysql import INTEGER, BOOLEAN

# import hashlib


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
RDB_PATH = "postgres://qwosamqjhsmjse:bdc36cd41f29cad53b026230c202df7ff08f34b0a1ede8a6334f134cc146f45f@ec2-44-194-92-192.compute-1.amazonaws.com:5432/d79ilntrh62i11"
ECHO_LOG = True

engine = create_engine(
    RDB_PATH
)

Session = sessionmaker(bind=engine)
session = Session()

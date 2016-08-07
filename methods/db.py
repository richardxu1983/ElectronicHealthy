#coding:utf-8

import psycopg2

conn = psycopg2.connect(database="health", user="dbuser", password="ranran", host="127.0.0.1", port="5432")#链接数据库

cur = conn.cursor()
#conn.set_session(autocommit=True)#设置自动提交,如果不设置,则需要手动提交
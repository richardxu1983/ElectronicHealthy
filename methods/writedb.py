#coding:utf-8

from db import *

#添加用户到数据库
def addUser(table, u_id, u_account, u_password_hash, u_salt, u_permission, u_status, u_email):
    sql = "INSERT INTO " + table + " (u_id, u_account, u_password_hash, u_salt, u_permission, u_status, u_email) VALUES (" + u_id + ", " + u_account + ", " + u_password_hash + ", " + u_salt + ", " + u_permission + ", " + u_status + ", " + u_email + ")"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()#出现异常则回滚
        return False
    else:
        conn.commit()  # 无异常,则提交
        return True

#修改密码
def changePassword(table, u_account, u_password_hash, u_salt):
    sql = "UPDATE " + table + " SET u_password_hash = '" + u_password_hash + "', u_salt = '" + u_salt + "' WHERE u_account = '" + u_account + "'"
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return False
    else:
        conn.commit()
        return True
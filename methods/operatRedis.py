#coding:utf-8

import binascii
import os
from connRedis import *

#在用户登录的时候,给用户设置一个随机字符串,每次登录时会改变。
def set_login_code(username):
    login_code = binascii.b2a_hex(os.urandom(16))
    r.set(username, login_code)

#根据用户名获取随机字符串
def get_login_code(username):
    if r.get(username) == None:#若获取随机字符串时为空,则先设置一个,再获取
        set_login_code(username)
        get_login_code(username)
    else:
        return r.get(username)



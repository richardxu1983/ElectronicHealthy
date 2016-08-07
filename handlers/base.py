# coding=utf-8
# encoding=utf-8
import tornado.web
import random
import binascii
import os
import hashlib
from tornado import gen
import logging
import methods.redisOperate as operateRedis
from random import choice
import string
import time

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    # 生成递增自然数
    def num_increase(self, max):
        a, b = 1, 1
        while a < max:
            yield a
            a = a + b

    # 自然数格式化
    def num_format(self, num):
        if num < 10:
            return '0' + '0' + str(num)

        elif num < 100:
            return '0' + str(num)
        else:
            return num

    # 生成随机密码
    def password_random(self):
        length = 8
        chars = string.ascii_letters + string.digits
        return ''.join([choice(chars) for i in range(length)])

    # 生成当前操作的系统时间
    def time_operate(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    # 判断密码格式是否正确
    def password_format(self, password):
        key = 0
        for value in password:
            if value.isspace() == True:#判断密码中是否有空格,如果有,则key+1
                key += 1
        if key == 0:#密码中没有空格
            if len(password)<8 or len(password)>16:
                return "105"#密码长度不正确
        else:
            return "104"#密码中出现空格

    # 判断允许值是否可枚举
    def de_acceptable_value_if_iterable_verify(self, de_acceptable_value):
        temp = "S1"
        if cmp(temp, de_acceptable_value) == 0:
            return False
        else:
            return True
#########################################################################3
    # 数据元标识符主题分类截取
    def de_theme_classification(self, de_di):
        return de_di[0:1]
    # 数据元标识符大类截取
    def de_classification_1(self, de_di):
        return de_di[2:3]
    # 数据元标识符小类截取
    def de_classification_2(self, de_di):
         return de_di[5:6]


    # 判断是否为CV值域代码
    def value_field_if_cv(self, vf_code):
        return vf_code[0:1] == 'CV'
    # 值域代码大类
    def cvvf_classification_1(self, vf_code):
        return vf_code[2:3]
    # 值域代码小类
    def cvvf_classification_2(self, vf_code):
        return vf_code[5:6]


    # 业务数据集即数据集标识符一级类目截取
    def dsmd_field_classification_1(self, dsmd_id):
        return dsmd_id[3]
    # 业务数据集即数据集标识符一级类目截取
    def dsmd_field_classification_2(self, dsmd_id):
        return dsmd_id[4:5]


    # 基本数据集即数据子集一级类目截取
    def dssmd_field_classification_1(self, dssmd_id):
        return dssmd_id[3]
    # 基本数据集即数据子集二级类目截取
    def dssmd_field_classification_2(self, dssmd_id):
        return dssmd_id[4:5]
    # 基本数据集即数据子集三级类目截取
    def dssmd_field_classification_3(self, dssmd_id):
        return dssmd_id[6:7]


    #数据元内部标识符一级类目截取
    def deridc_classification_1(self, de_rid):
        return de_rid[3]
    # 数据元内部标识符二级类目截取
    def deridc_classification_2(self, de_rid):
        return de_rid[4:5]
    # 数据元内部标识符三级类目截取
    def deridc_classification_3(self, de_rid):
        return de_rid[6:7]

##################################################################################
    # 生成18位随机数
    def random_number(self):
        return random.randint(100000000000000000, 999999999999999999)

    # 产生32位的salt值
    def random_salt(self):
        return binascii.b2a_hex(os.urandom(16))

    # 产生存入数据库的密码hash值
    def result_hash(self, username, password, salt):
        hash_value = hashlib.md5(username + password).hexdigest().decode()
        return hashlib.md5(salt + hash_value).hexdigest()


    # 设置当前登录用户
    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")


    # 设置登录码login_code
    def set_current_login_code(self, login_code):
        if login_code:
            self.set_secure_cookie("login_code", tornado.escape.json_encode(login_code))
        else:
            self.clear_cookie("login_code")

    # 比较login_code是否一致
    def login_code_verify(self, username, login_code):
        if operateRedis.get_login_code(username) == login_code:
            return True
        else:
            self.clear_cookie("user")
            self.clear_cookie("login_code")
            return False

    # 获取用户名cookie
    def get_current_user(self):
        return self.get_secure_cookie("user")


    # 获取登录码login_code
    def get_current_login_code(self):
        return self.get_secure_cookie("login_code")


    # 用户权限验证
    @gen.coroutine
    def permission_verify(self, permission):
        username = tornado.escape.json_decode(self.current_user)
        login_code = tornado.escape.json_decode(self.get_current_login_code())  # 获取登录码
        try:
            f2 = self.db.execute('select * from user_infos where u_account = %s', (username))  # 根据用户名查询数据库
            yield f2
            cursor = f2.result()
            data = cursor.fetchone()

            if self.login_code_verify(username, login_code):  # 判断登录码是否正确
                u_status = data[6]
                if u_status:  # 判断是否处于激活状态
                    u_permission = data[5]  # 获取用户权限
                    if u_permission == permission:  # 判断是否为用户管理员 2： 用户管理员 1 ： 数据管理员 0 ： 普通用户
                        raise gen.Return(data)
                        #self.render("userManage.html", user_infos=data)
                    else:
                        # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
                        raise gen.Return(False)
                        #self.write("您没有进行此操作的权限!")
                else:
                    self.clear_all_cookies()
                    # self.write({"status_code": "-5"})  # 账号被冻结，请联系管理员
                    self.write("<html><body><p>账号已经被冻结,请联系管理员!</p></body></html>")
            else:
                # self.write({"status_code": "-7"})  # 你的账号已在别处登录
                self.write("你的账号已在别处登录")
        except Exception:
            # self.write({"status_code": "-4"})  # 表示没有此用户，请注册申请
            logging.exception("Username: " + str(username))
        finally:
            self.finish()

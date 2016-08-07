# coding=utf-8
# encoding=utf-8

from tornado import gen
import momoko
import hashlib
import tornado.escape
import logging
import tornado.web
from base import BaseHandler
import methods.redisOperate as operateRedis
import methods.emailSend as emailSend

class LoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.clear_cookie("user")
        self.clear_cookie("login_code")
        self.render("login.html")

    @gen.coroutine
    def post(self, *args, **kwargs):
        username = self.get_arguments("username")  # 获取登录表单信息中的用户名
        hash_value = self.get_arguments("hash_value")  # 获取登录表单的hash_value
        if not username or not hash_value:
            self.write({"status_code": "-3"})   # 表示账号或密码为空
            self.finish()
            return
        operateRedis.set_login_code(username)  # 用户登录时设置login_code
        login_code = operateRedis.get_login_code(username)  # 获取用户登录随即设置的login_code
        try:
            f1 = self.db.execute('select * from user_infos where u_account = %s', (username))
            yield f1
            cursor = f1.result()
            data = cursor.fetchone()
            u_password_hash1 = hashlib.md5(data[4] + hash_value[0]).hexdigest()
            if data[3] == u_password_hash1:  # 判断是够密码正确
                if data[6]:
                    self.set_current_user(username)
                    self.set_current_login_code(login_code)
                else:
                    self.write({"status_code": "-2"})  # 表示用户被冻结
            else:
                self.write({"status_code": "-1"})  # 表示账号或密码错误
        except Exception:
            # self.write({"status_code": "-4"})  # 表示没有此用户，请注册申请
            logging.exception("Username:" + str(username))
        finally:
            self.finish()

class LogOutHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.clear_all_cookies()
        self.redirect("login.html")

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        username = tornado.escape.json_decode(self.current_user)   # 获取登录名
        login_code = tornado.escape.json_decode(self.get_current_login_code())   # 获取登录码
        try:
            f2 = self.db.execute('select * from user_infos where u_account = %s', (username))   # 根据用户名查询数据库
            yield f2
            cursor = f2.result()
            if self.login_code_verify(username, login_code):  # 判断密码是否正确
                u_status = cursor.fetchone()[6]
                if u_status:    # 判断是否处于激活状态
                    self.render("index.html")
                else:
                    self.clear_cookie("user")
                    self.clear_cookie("login_code")
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

class PasswordModifyHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        username = tornado.escape.json_decode(self.current_user)  # 获取登录名
        login_code = tornado.escape.json_decode(self.get_current_login_code())  # 获取登录码
        try:
            f2 = self.db.execute('select * from user_infos where u_account = %s', (username))  # 根据用户名查询数据库
            yield f2
            cursor = f2.result()
            data = cursor.fetchone()
            if self.login_code_verify(username, login_code):  # 判断密码是否正确
                u_status = data[6]
                if u_status:  # 判断是否处于激活状态
                    passwordOld = self.get_argument("passwordOld")
                    passwordNew = self.get_argument("passwordNew")
                    passwordVerify = self.get_argument("passwordVerify")
                    if not passwordOld or not passwordNew or not passwordVerify:
                        #self.write({"status": '-13'})  # 密码为空，请重新输入
                        self.write("密码为空，请重新输入")
                        return
                    elif passwordOld == passwordNew:
                        # self.write({"status": '-14'})  # 密码与新密码相同，请重新输入
                        self.write(" 密码与新密码相同，请重新输入")
                    elif passwordVerify != passwordNew:
                        # self.write({"status": '-15'})  # 验证密码与新密码不相同，请重新输入
                        self.write("验证密码与新密码不相同，请重新输入")
                    else:
                        u_salt = data[4]
                        u_account = username
                        u_password_hash = self.result_hash(username=u_account, password=passwordNew, salt=u_salt)
                        try:
                            future = self.db.execute(
                                'update user_infos set U_PASSWORD_HASH = u_password_hash where U_ACCOUNT = u_account')  # 根据用户名更新数据库
                            yield future
                        except Exception:
                            # self.write({"status_code": "-9"})  # 表示更新用户失败
                            self.write("更新用户失败")
                        else:
                            # self.write({"status_code": "10"})  # 表示更新用户成功
                            self.write("更新用户成功")
                else:
                    self.clear_cookie("user")
                    self.clear_cookie("login_code")
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


class PasswordForgetHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        username = self.get_argument("username")   # 获取账号
        email = self.get_argument("email")    # 获取邮箱以修改密码
        try:
            future = self.db.execute('select * from user_infos where u_account = %s', (username))  # 根据用户名查询数据库
            yield future
            cursor = future.result()
            data = cursor.fetchone()
            passwordNew = self.password_random()
            u_salt = data[4]
            u_account = username
            u_password_hash = self.result_hash(username=u_account, password=passwordNew, salt=u_salt)
            try:
                future = self.db.execute(
                    'update user_infos set U_PASSWORD_HASH = u_password_hash where U_ACCOUNT = u_account')  # 根据用户名更新数据库
                yield future
                content = username + ", 你的密码是: " + passwordNew + ",请重新登录"   # 邮件内容
                emailSend.send_mail(email, "电子健康档案账号密码修改",content=content)   # 邮箱发送
            except Exception:
                # self.write({"status_code": "-9"})  # 表示更新用户失败
                self.write("更新用户失败")
            else:
                # self.write({"status_code": "10"})  # 表示更新用户成功
                self.write("更新用户成功")
        except Exception:
            # self.write({"status_code": "-4"})  # 表示没有此用户，请注册申请
            self.write("表示没有此用户，请注册申请")
            logging.exception("Username: " + str(username))
        finally:
            self.finish()


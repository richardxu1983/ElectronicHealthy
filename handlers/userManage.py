# coding=utf-8

import tornado.web
import tornado.escape
from tornado import gen
import logging

from base import BaseHandler

class UserManageHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        data = yield self.permission_verify(permission=2)
        if data:
            self.render("userManage.html", user_infos=data)
        else:
            # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
            self.write("您没有进行此操作的权限!")

class UserAddHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        data = yield self.permission_verify(permission=2)
        if data:
            userAdd = self.get_argument("userAdd")
            passwordAdd = self.get_argument("passwordAdd")
            emailAdd = self.get_argument("emailAdd")
            permissionAdd = self.get_argument("permissionAdd")
            statusAdd = self.get_argument("statusAdd")
            if not userAdd or not passwordAdd or not emailAdd or not permissionAdd or not statusAdd:
                #self.write({"status_code": "-8"})  # 表示账号或密码或邮箱或权限或状态为空
                self.write("账号或密码或邮箱或权限或状态为空, 请重新验证")
                return
            u_id = self.random_number()
            u_account = userAdd
            u_salt = self.random_salt()
            u_permission = permissionAdd
            u_password_hash = self.result_hash(username=userAdd, password=passwordAdd, salt=u_salt)
            u_status = statusAdd
            u_email = emailAdd
            try:
                future = self.db.execute('select * from user_infos where u_account = %s', (userAdd))  # 根据用户名查询用户信息
                yield future
            except Exception:
                try:
                    future = self.db.execute(
                        'insert into user_infos(U_ID,U_ACCOUNT,U_PASSWORD_HASH,U_SALT,U_PERMISSION,U_STATUS,U_EMAIL) VALUES (u_id, u_account, u_password_hash, u_salt, u_permission, u_status, u_email)')  # 将数据插入数据库
                    yield future
                except Exception:
                    # self.write({"status_code": "-9"})  # 表示创建用户失败
                    self.write("创建用户失败")
                else:
                    # self.write({"status_code": "10"})  # 表示创建用户成功
                    self.write("创建用户成功")
            else:
                # self.write({"status_code": "-10"}) # 该用户已存在，不能重新创建
                self.write("该用户已存在，不能重新创建")
        else:
            # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
            self.write("您没有进行此操作的权限!")

class UserModifyHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        data = yield self.permission_verify(permission=2)
        if data:
            userModify = self.get_argument("userModify")
            passwordModify = self.get_argument("passwordModify")
            emailModify = self.get_argument("emailModify")
            permissionModify = self.get_argument("permissionModify")
            statusModify = self.get_argument("statusModify")
            if not userModify or not passwordModify or not emailModify or not permissionModify or not statusModify:
                # self.write({"status_code": "-8"})  # 表示账号或密码或邮箱或权限或状态为空
                self.write("账号或密码或邮箱或权限或状态为空, 请重新验证")
                return
            u_salt = data[4]
            u_password_hash = self.result_hash(username=userModify, password=passwordModify, salt=u_salt)
            u_account = userModify
            u_permission = permissionModify
            u_status = statusModify
            try:
                future = self.db.execute('select * from user_infos where u_account = %s', (userModify))  # 根据用户名查询用户信息
                yield future
                try:
                    future = self.db.execute(
                        'update user_infos set U_PASSWORD_HASH = u_password_hash,U_PERMISSION = u_permission,U_STATUS = u_status,U_EMAIL = u_email where U_ACCOUNT = u_account')  # 根据用户名更新数据库
                    yield future
                except Exception:
                    # self.write({"status_code": "-9"})  # 表示更新用户失败
                    self.write("更新用户失败")
                else:
                    # self.write({"status_code": "10"})  # 表示更新用户成功
                    self.write("更新用户成功")
            except Exception:
                # self.write({"status_code": "-12"}) # 找不到该用户
                self.write("找不到该用户，请重新创建该用户")
                # self.redirect("/userManage/add")
        else:
            # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
            self.write("您没有进行此操作的权限!")


class UserSearchHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        data = yield self.permission_verify(permission=2)
        if data:
            userSearch = self.get_argument("userSearch")
            if not userSearch:   # 输入为空
                try:
                    future = self.db.execute('select * from user_infos')
                    yield future
                    cursor = future.result()
                    self.write({"data": cursor.fetchall(), "status_code":"11"})   # 查询用户成功
                    self.write("查询用户成功")
                except Exception:
                    # self.write({"status_code": "-11"})  # 表示查询用户失败
                    self.write("查询用户失败,没有改用户，请重新创建")
                    # self.redirect("/userManage/add")
                finally:
                    self.finish()
            else:
                try:
                    future = self.db.execute('select * from user_infos where u_account = %s', (userSearch))   # 根据用户名查询用户信息
                    yield future
                    cursor = future.result()
                    self.write({"data": cursor.fetchone(), "status_code": "11"})  # 查询用户成功
                    self.write("查询用户成功")
                except Exception:
                    # self.write({"status_code": "-11"})  # 表示查询用户失败
                    self.write("查询用户失败,没有改用户，请重新创建")
                    # self.redirect("/userManage/add")
                finally:
                    self.finish()
        else:
            # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
            self.write("您没有进行此操作的权限!")

class UserDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        data = yield self.permission_verify(permission=2)
        if data:
            userDelete = self.get_argument("userDelete")
            if not userDelete:  # 输入为空
                self.write("账号为空, 请重新输入")
                return
            try:
                future = self.db.execute('delete from user_infos where u_account = %s', (userDelete))   # 根据用户名删除用户信息
                yield future
                self.write({"status": "12"})    # 删除用户成功
                self.write("删除用户成功")
            except Exception:
                # self.write({"status_code": "-13"})  # 表示删除用户失败
                self.write("删除用户失败，没有该用户，请仔细检查")
                # self.redirect("/userManage/search")
            finally:
                self.finish()
        else:
            # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
            self.write("您没有进行此操作的权限!")
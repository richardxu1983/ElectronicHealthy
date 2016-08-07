# coding=utf-8

from tornado import gen
from base import BaseHandler
import tornado.web
import logging

# 数据元管理
class DataElementManageHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        data = yield self.permission_verify(permission=1)
        if data:
            self.render("dataelementManage.html", user_infos=data)
        else:
            # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
            self.write("您没有进行此操作的权限!")

class DataElementAddHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        data = yield self.permission_verify(permission=1)
        if data:
            de_di = self.get_argument("de_di")    # 数据元标识符
            de_definition = self.get_argument("de_definition")  # 数据元定义
            de_name = self.get_argument("de_name")   # 数据元名称
            de_data_type = self.get_argument("de_data_type")   # 数据元数据类型
            de_present_format = self.get_argument("de_present_format")    # 数据元表示格式
            de_acceptable_values = self.get_argument("de_acceptable_values")  # 数据元允许值
            # de_acceptable_value_if_iterable = self.get_argument("de_acceptable_value_if_iterable")  # 数据元允许值是否可枚举
            de_value_field_code = self.get_argument("de_di")  # 数据元值域代码编号
            de_status = self.get_argument("de_di")  # 数据元状态
            de_value_field_if_cv = self.get_argument("de_value_field_if_cv")  # 数据元值域代码是否为cv值域

            if not de_di or not de_definition or not de_name or not de_data_type or not de_present_format or not de_status or not de_value_field_if_cv:
                # self.write({"status_code": "-8"})  # 表示数据元标识符或定义或名称或数据类型或表示格式或状态或值域代码是否为cv值域为空
                self.write("数据元标识符或定义或名称或数据类型或表示格式或状态或值域代码是否为cv值域为空，请重新输入")
                return
            de_created_datetime = self.time_operate()   # 创建时间
            de_theme_classification = self.de_theme_classification(de_di)   # 主题分类
            de_classification_1 = self.de_classification_1(de_di)    # 大类
            de_classification_2 = self.de_classification_2(de_di)  # 小类
            try:
                future = self.db.execute('select * from DATAELEMENT where DE_DI = %s', (de_di))
                yield future
            except Exception:
                try:
                    future = self.db.execute(
                        'INSERT INTO DATAELEMENT(DE_DI, DE_THEME_CLASSIFICATION, DE_CLASSIFICATION_1, DE_CLASSIFICATION_2, DE_NAME,DE_DEFINATION, DE_DATA_TYPE, DE_PRESENT_FORMAT, DE_ACCEPTABLE_VALUES,DE_ACCEPTABLE_VALUE_IF_ITERABLE, DE_VALUE_FIELD_CODE, DE_STATUS, DE_CREATED_DATETIME,DE_VALUE_FIELD_IF_CV)VALUES(de_di, de_theme_classification, de_classification_1, de_classification_2, de_name,de_defination, de_data_type, de_present_format, de_acceptable_values,de_acceptable_value_if_iterable, de_value_field_code, de_status, de_created_datetime,de_value_field_if_cv)')  # 将数据元插入数据元列表
                    yield future
                except Exception:
                    # self.write({"status_code": "-15"})  # 表示新增数据元失败
                    self.write("新增数据元失败")
                else:
                    # self.write({"status_code": "20"})  # 表示新增数据元成功
                    self.write("新增数据元成功")
            else:
                # self.write({"status_code": "-18"})  # 表示新增数据元失败,已有改数据元
                self.write("新增数据元失败,已有改数据元")
        else:
            # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
            self.write("您没有进行此操作的权限!")

class DataElementModifyHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        data = yield self.permission_verify(permission=1)
        if data:
            de_di = self.get_argument("de_di")  # 数据元标识符
            de_definition = self.get_argument("de_definition")  # 数据元定义
            de_name = self.get_argument("de_name")  # 数据元名称
            de_data_type = self.get_argument("de_data_type")  # 数据元数据类型
            de_present_format = self.get_argument("de_present_format")  # 数据元表示格式
            de_acceptable_values = self.get_argument("de_acceptable_values")  # 数据元允许值
            # de_acceptable_value_if_iterable = self.get_argument("de_acceptable_value_if_iterable")  # 数据元允许值是否可枚举
            de_value_field_code = self.get_argument("de_di")  # 数据元值域代码编号
            de_status = self.get_argument("de_di")  # 数据元状态
            de_value_field_if_cv = self.get_argument("de_value_field_if_cv")  # 数据元值域代码是否为cv值域

            if not de_di or not de_definition or not de_name or not de_data_type or not de_present_format or not de_status or not de_value_field_if_cv:
                # self.write({"status_code": "-8"})  # 表示数据元标识符或定义或名称或数据类型或表示格式或状态或值域代码是否为cv值域为空
                self.write("数据元标识符或定义或名称或数据类型或表示格式或状态或值域代码是否为cv值域为空，请重新输入")
                return
            # 修改前数据元判断是否存在，由于获取时数据元标识符不变，故判断省去

            de_created_datetime = self.time_operate()  # 创建时间
            # 数据元标识符 和值域代码不变，故主题分类、大类小类不变
            de_theme_classification = self.de_theme_classification(de_di)  # 主题分类
            de_classification_1 = self.de_classification_1(de_di)  # 大类
            de_classification_1 = self.de_classification_2(de_di)  # 小类
            try:
                future = self.db.execute('select * from DATAELEMENT where DE_DI = %s', (de_di))
                yield future
                try:
                    future = self.db.execute(
                        'update DATAELEMENT set DE_NAME = de_name,DE_DEFINATION = de_defination,DE_DATA_TYPE = de_data_type,DE_PRESENT_FORMAT = de_present_format,DE_ACCEPTABLE_VALUES=de_acceptable_values,DE_ACCEPTABLE_VALUE_IF_ITERABLE=de_acceptable_value_if_iterable,DE_STATUS=de_status, DE_CREATED_DATETIME=de_created_datetime  where DE_DI = de_di')  # 根据数据元标识符更新数据库
                    yield future
                except Exception:
                    # self.write({"status_code": "-16"})  # 表示更新数据元失败
                    self.write("更新数据元失败")
                else:
                    # self.write({"status_code": "21"})  # 表示更新数据元成功
                    self.write("更新数据元成功，请重新导入数据集记录")
            except Exception:
                # self.write({"status_code": "-21"})  # 表示更新数据元失败，没有该数据元
                self.write("表示更新数据元失败，没有该数据元")
                # self.redirect("/dataelementManage/add")
        else:
            # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
            self.write("您没有进行此操作的权限!")

class DataElementSearchHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        # data = yield self.permission_verify(permission=1)
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
                    de_di = self.get_argument("de_di")  #
                    # de_stutus = 1
                    if not de_di:  # 输入为空
                        try:
                            future = self.db.execute('select * from DATAELEMENT')
                            yield future
                            cursor = future.result()
                            self.write({"data": cursor.fetchall(), "status_code": "11"})  # 查询数据元成功
                            self.write("查询数据元成功")
                        except Exception:
                            # self.write({"status_code": "-11"})  # 表示查询数据元失败
                            self.write("查询数据元失败")
                        finally:
                            self.finish()
                    else:
                        try:
                            future = self.db.execute('select * from DATAELEMENT where DE_DI = %s and DE_STATUS = 1',(de_di))  # 根据用户名查询用户信息
                            yield future
                            cursor = future.result()
                            self.write({"data": cursor.fetchone(), "status_code": "11"})  # 查询数据元成功
                            self.write("查询数据元成功")
                        except Exception:
                            # self.write({"status_code": "-11"})  # 表示查询数据元失败
                            self.write("查询数据元失败")
                        finally:
                            self.finish()
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

class DataElementDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        data = yield self.permission_verify(permission=2)
        if data:
            de_di = self.get_argument("de_di")
            if not de_di:  # 输入为空
                self.write("账号为空, 请重新输入")
                return
            de_status = 0    # 1 表示存在 0 表删除
            try:   # 删除前先判断
                future = self.db.execute('select * from DATAELEMENT where DE_DI = %s', (de_di))
                yield future
                try:
                    future = self.db.execute('update DATAELEMENT set DE_STATUS=de_status  where DE_DI =  %s',
                                             (de_di))  # 根据用户名删除用户信息
                    yield future
                    self.write({"status": "23"})  # 删除数据元成功
                    self.write("删除数据元成功")
                except Exception:
                    # self.write({"status_code": "-18"})  # 表示删除数据元失败
                    self.write("删除数据元失败")
            except Exception:
                # self.write({"status_code": "-19"})  # 表示删除数据元失败，没有该数据元
                self.write("删除数据元失败,没有该数据元")
                self.redirect("/dataelementManage/add")
            finally:
                self.finish()
        else:
            # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
            self.write("您没有进行此操作的权限!")
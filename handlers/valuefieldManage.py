# coding=utf-8

from tornado import gen
import tornado.web
from base import BaseHandler
import logging

# 数据元管理
class ValueFieldManageHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        data = yield self.permission_verify(permission=1)
        if data:
            self.render("valuefieldManage.html", user_infos=data)
        else:
            # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
            self.write("您没有进行此操作的权限!")

class ValueFieldAddHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        data = yield self.permission_verify(permission=1)
        if data:
            cvvf_oid = self.get_argument("cvvf_oid")    #  cv_oid
            cvvf_code = self.get_argument("cvvf_code")  #  值域代码编号

            cvvf_name = self.get_argument("cvvf_name")    #  值域代码名字
            cvvf_classification = self.get_argument("cvvf_classification")  # 值域代码类别
            cvvf_status = self.get_argument("cvvf_status")  # 状态

            cvvf_value = self.get_argument("cvvf_value")   # 值域代码值
            cvvf_definition = self.get_argument("cvvf_definition")  # 值定义
            cvvf_note = self.get_argument("cvvf_note")   # 备注

            if not cvvf_oid or not cvvf_code or not cvvf_name or not cvvf_status or not cvvf_classification :
                # self.write({"status_code": "-8"})  # 表示cv_oid或值域代码名字或值域代码编号或值域代码类别或状态为空
                self.write("cv_oid或值域代码名字或值域代码编号或值域代码类别或状态为空，请重新输入")
                return
            cv_created_datetime = self.time_operate()   # 创建时间
            cvvf_classification_1 = self.cvvf_classification_1(cvvf_code)   # 值域代码大类
            cvvf_classification_2 = self.cvvf_classification_2(cvvf_code)  # 值域代码小类

            if self.value_field_if_cv(cvvf_code):   # 判断是否为CV值域代码
                try:
                    future = self.db.execute('select * from CVVALUEFIELD where CVVF_CODE = %s', (cvvf_code))  # 搜索是否已有值域代码
                    yield future
                    try:
                        future1 = self.db.execute('INSERT INTO CVVALUEFIELD_VALUE(CVVF_VALUE, CVVF_DEFINATION, CVVF_NOTE) VALUES(cvvf_value,cvvf_definition, cvvf_note) WHERE CVVALUEFIELD.CVVF_INC_PK = CVVALUEFIELD_VALUE.CVVF_INC_PK')
                        yield future1
                    except Exception:
                        # self.write({"status_code": "-15"})  # 表示新增值域代码值失败
                        self.write("新增值域代码值失败")
                except Exception:
                    try:
                        future = self.db.execute(
                            'INSERT INTO CVVALUEFIELD(CVVF_OID, CVVF_CODE, CVVF_CLASSIFICATION_1 , CVVF_CLASSIFICATION_2, CVVF_NAME ,CVVF_CLASSIFICATION, CVVF_STATUS, CVVF_CREATED_DATETIME)VALUES(cvvf_oid, cvvf_code, cvvf_classification_1 , cvvf_classification_2, cvvf_name ,cvvf_classification, cvvf_status, cvvf_created_datetime)')  # 将值域代码插入值域代码列表
                        yield future
                    except Exception:
                        # self.write({"status_code": "-15"})  # 表示新增值域代码失败
                        self.write("新增值域代码失败")
                    else:
                        # self.write({"status_code": "20"})  # 表示新增值域代码成功
                        self.write("新增值域代码成功")
                else:
                    # self.write({"status_code": "-18"})  # 表示新增值域代码失败,已有值域代码
                    self.write("新增值域代码失败,已有该值域代码")
            else:
                try:
                    future = self.db.execute('select * from VALUEFIELD where CVVF_CODE = %s', (cvvf_code))
                    yield future
                    try:
                        future1 = self.db.execute(
                            'INSERT INTO VALUEFIELD_VALUE(VF_VALUE,VF_DEFINATION, VF_NOTE) VALUES(cvvf_value,cvvf_definition, cvvf_note) WHERE VALUEFIELD.VF_INC_PK = VALUEFIELD_VALUE.VF_INC_PK')
                        yield future1
                    except Exception:
                        # self.write({"status_code": "-15"})  # 表示新增值域代码值失败
                        self.write("新增值域代码值失败")
                except Exception:
                    try:
                        future = self.db.execute(
                            'INSERT INTO VALUEFIELD(VF_OID, VF_CODE, VF_CLASSIFICATION_1 , VF_CLASSIFICATION_2, VF_NAME ,VF_CLASSIFICATION, VF_STATUS, VF_CREATED_DATETIME)VALUES(cvvf_oid, cvvf_code, cvvf_classification_1 , cvvf_classification_2, cvvf_name ,cvvf_classification, cvvf_status, cvvf_created_datetime)')  # 将值域代码插入值域代码列表
                        yield future
                    except Exception:
                        # self.write({"status_code": "-15"})  # 表示新增值域代码失败
                        self.write("新增值域代码失败")
                    else:
                        # self.write({"status_code": "20"})  # 表示新增值域代码成功
                        self.write("新增值域代码成功")
                else:
                    # self.write({"status_code": "-18"})  # 表示新增值域代码失败,已有值域代码
                    self.write("新增值域代码失败,已有该值域代码")
        else:
            # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
            self.write("您没有进行此操作的权限!")

class ValueFieldModifyHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        data = yield self.permission_verify(permission=1)
        if data:
            cvvf_oid = self.get_argument("cvvf_oid")  # cv_oid
            cvvf_code = self.get_argument("cvvf_code")  # 值域代码编号

            cvvf_name = self.get_argument("cvvf_name")  # 值域代码名字
            cvvf_classification = self.get_argument("cvvf_classification")  # 值域代码类别
            cvvf_status = self.get_argument("cvvf_status")  # 状态

            cvvf_value = self.get_argument("cvvf_value")  # 值域代码值
            cvvf_definition = self.get_argument("cvvf_definition")  # 值定义
            cvvf_note = self.get_argument("cvvf_note")  # 备注

            if not cvvf_oid or not cvvf_code or not cvvf_name or not cvvf_status or not cvvf_classification:
                # self.write({"status_code": "-8"})  # 表示cv_oid或值域代码名字或值域代码编号或值域代码类别或状态为空
                self.write("cv_oid或值域代码名字或值域代码编号或值域代码类别或状态为空，请重新输入")
                return
            cv_created_datetime = self.time_operate()  # 创建时间
            cvvf_classification_1 = self.cvvf_classification_1(cvvf_code)  # 值域代码大类
            cvvf_classification_2 = self.cvvf_classification_2(cvvf_code)  # 值域代码小类
            if self.value_field_if_cv(cvvf_code):  # 判断是否为CV值域代码
                try:
                    future = self.db.execute('select * from CVVALUEFIELD where CVVF_CODE = %s',(cvvf_code))  # 搜索是否已有值域代码
                    yield future
                    try:
                        future = self.db.execute(
                            'update CVVALUEFIELD set CVVF_NAME = cvvf_name,CVVF_CLASSIFICATION = cvvf_classification,CVVF_STATUS = cvvf_status,CVVF_CREATED_DATETIME = cvvf_created_datetime  where CVVF_CODE = cvvf_code')  # 根据值域代码编号更新数据库
                        yield future
                        future1 = self.db.execute(
                            'update CVVALUEFIELD_VALUE set CVVF_VALUE= cvvf_value,CVVF_DEFINITION = cvvf_definition,CVVF_NOTE = cvvf_note  where CVVALUEFIELD.CVVF_INC_PK = CVVALUEFIELD_VALUE.CVVF_INC_PK')
                        yield future1
                    except Exception:
                        # self.write({"status_code": "-16"})  # 表示更新数据元失败
                        self.write("更新数据元失败")
                    else:
                        # self.write({"status_code": "21"})  # 表示更新数据元成功
                        self.write("更新数据元成功")
                except Exception:
                    # self.write({"status_code": "-21"})  # 表示更新数据元失败，没有该数据元
                    self.write("表示更新数据元失败，没有该数据元")
                    self.redirect("/valuefieldManage/add")
            else:
                try:
                    future = self.db.execute('select * from VALUEFIELD where VF_CODE = %s',
                                             (cvvf_code))  # 搜索是否已有值域代码
                    yield future
                    try:
                        future = self.db.execute(
                            'update VALUEFIELD set VF_NAME = cvvf_name,VF_CLASSIFICATION = cvvf_classification,VF_STATUS = cvvf_status,VF_CREATED_DATETIME = cvvf_created_datetime  where VF_CODE = cvvf_code')  # 根据值域代码编号更新数据库
                        yield future
                        future1 = self.db.execute(
                            'update VALUEFIELD_VALUE set VF_VALUE= cvvf_value,VF_DEFINITION = cvvf_definition,VF_NOTE = cvvf_note  where VALUEFIELD.VF_INC_PK = VALUEFIELD_VALUE.VF_INC_PK')
                        yield future1
                    except Exception:
                        # self.write({"status_code": "-16"})  # 表示更新数据元失败
                        self.write("更新数据元失败")
                    else:
                        # self.write({"status_code": "21"})  # 表示更新数据元成功
                        self.write("更新数据元成功")
                except Exception:
                    # self.write({"status_code": "-21"})  # 表示更新数据元失败，没有该数据元
                    self.write("表示更新数据元失败，没有该数据元")
        else:
            # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
            self.write("您没有进行此操作的权限!")

class ValueFieldSearchHandler(BaseHandler):
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
                    cvvf_code = self.get_argument("cvvf_code")  # 获取前台的数据
                    # de_stutus = 1
                    if not cvvf_code:  # 输入为空
                        try:
                            future = self.db.execute('select CVVALUEFIELD.CVVF_OID, CVVALUEFIELD.CVVF_CODE, CVVALUEFIELD.CVVF_NAME, CVVALUEFIELD.CVVF_CLASSIFICATION, CVVALUEFIELD.CVVF_STATUS, CVVALUEFIELD.CVVF_CREATED_DATETIME,CVVALUEFIELD_VALUE.CVVF_VALUE , CVVALUEFIELD_VALUE.CVVF_DEFINATION from CVVALUEFIELD JOIN CVVALUEFIELD_VALUE ON CVVALUEFIELD_VALUE.CVVF_INC_PK = CVVALUEFIELD.CVVF_INC_PK')
                            yield future
                            cursor = future.result()
                            future1 = self.db.execute('select VALUEFIELD.VF_OID, VALUEFIELD.VF_CODE, VALUEFIELD.VF_NAME, VALUEFIELD.VF_CLASSIFICATION, VALUEFIELD.VF_STATUS, VALUEFIELD.VF_CREATED_DATETIME,VALUEFIELD_VALUE.VF_VALUE , VALUEFIELD_VALUE.VF_DEFINATION from VALUEFIELD JOIN VALUEFIELD_VALUE ON VALUEFIELD_VALUE.VF_INC_PK = VALUEFIELD.CVVF_INC_PK')
                            yield future1
                            cursor1 = future1.result()
                            self.write({"data": cursor.fetchall()+ cursor1.fetchall() , "status_code": "11"})  # 查询值域代码成功
                            self.write("查询值域代码成功")
                        except Exception:
                            # self.write({"status_code": "-11"})  # 表示查询值域代码失败
                            self.write("查询值域代码失败")
                        finally:
                            self.finish()
                    else:
                        if self.value_field_if_cv(cvvf_code):
                            try:
                                future = self.db.execute( 'select CVVALUEFIELD.CVVF_OID, CVVALUEFIELD.CVVF_CODE, CVVALUEFIELD.CVVF_NAME, CVVALUEFIELD.CVVF_CLASSIFICATION, CVVALUEFIELD.CVVF_STATUS, CVVALUEFIELD.CVVF_CREATED_DATETIME,CVVALUEFIELD_VALUE.CVVF_VALUE , CVVALUEFIELD_VALUE.CVVF_DEFINATION from CVVALUEFIELD JOIN CVVALUEFIELD_VALUE ON CVVALUEFIELD_VALUE.CVVF_INC_PK = CVVALUEFIELD.CVVF_INC_PK WHERE CVVALUEFIELD.CVVF_CODE = %s or CVVALUEFIELDCVVF_NAME = %s',(cvvf_code,cvvf_code))
                                yield future
                                cursor = future.result()
                                self.write({"data": cursor.fetchone(), "status_code": "11"})  # 查询值域代码成功
                                self.write("查询值域代码成功")
                            except Exception:
                                # self.write({"status_code": "-11"})  # 表示查询值域代码失败
                                self.write("查询值域代码失败")
                            finally:
                                self.finish()
                        else:
                            try:
                                future = self.db.execute( 'select VALUEFIELD.VF_OID, VALUEFIELD.VF_CODE, VALUEFIELD.VF_NAME, VALUEFIELD.VF_CLASSIFICATION, VALUEFIELD.VF_STATUS, VALUEFIELD.VF_CREATED_DATETIME,VALUEFIELD_VALUE.VF_VALUE , VALUEFIELD_VALUE.VF_DEFINATION from VALUEFIELD JOIN VALUEFIELD_VALUE ON VALUEFIELD_VALUE.VF_INC_PK = VALUEFIELD.CVVF_INC_PK WHERE VALUEFIELD.VF_CODE = %s or VALUEFIELDCVVF_NAME = %s',(cvvf_code,cvvf_code))
                                yield future
                                cursor = future.result()
                                self.write({"data": cursor.fetchone(), "status_code": "11"})  # 查询值域代码成功
                                self.write("查询值域代码成功")
                            except Exception:
                                # self.write({"status_code": "-11"})  # 表示查询值域代码失败
                                self.write("查询值域代码失败")
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

class ValueFieldDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        data = yield self.permission_verify(permission=2)
        if data:
            cvvf_code = self.get_argument("cvvf_code")
            if not cvvf_code:  # 输入为空
                self.write("账号为空, 请重新输入")
                return
            cvvf_status = 0    # 1 表示存在 0 表删除
            if self.value_field_if_cv(cvvf_code):  # 判断是否为CV值域代码
                try:  # 删除前先判断
                    future = self.db.execute('select * from CVVALUEFIELD where CVVF_CODE = %s', (cvvf_code))
                    yield future
                    try:
                        future = self.db.execute('update CVVALUEFIELD set CVVF_STATUS=cvvf_status  CVVF_CODE = %s',
                                                 (cvvf_code))  # 根据用户名删除值域代码
                        yield future
                        self.write({"status": "23"})  # 删除值域代码成功
                        self.write("删除值域代码成功")
                    except Exception:
                        # self.write({"status_code": "-18"})  # 表示删除值域代码失败
                        self.write("删除值域代码失败")
                except Exception:
                    # self.write({"status_code": "-19"})  # 表示删除值域代码失败，没有该值域代码
                    self.write("删除值域代码失败,没有该值域代码")
                    # self.redirect("/valuefieldManage/add")
                finally:
                    self.finish()
            else:
                try:  # 删除前先判断
                    future = self.db.execute('select * from VALUEFIELD where VF_CODE = %s', (cvvf_code))
                    yield future
                    try:
                        future = self.db.execute('update VALUEFIELD set VF_STATUS=cvvf_status  VF_CODE = %s',
                                                 (cvvf_code))  # 根据用户名删除值域代码
                        yield future
                        self.write({"status": "23"})  # 删除值域代码成功
                        self.write("删除值域代码成功")
                    except Exception:
                        # self.write({"status_code": "-18"})  # 表示删除值域代码失败
                        self.write("删除值域代码失败")
                except Exception:
                    # self.write({"status_code": "-19"})  # 表示删除值域代码失败，没有该值域代码
                    self.write("删除值域代码失败,没有该值域代码")
                    # self.redirect("/valuefieldManage/add")
                finally:
                    self.finish()
        else:
            # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
            self.write("您没有进行此操作的权限!")
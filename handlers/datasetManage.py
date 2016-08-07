# coding=utf-8

from base import BaseHandler
from tornado import gen
import tornado.web
import logging

# 业务数据集管理
class DataSetManager(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        data = yield self.permission_verify(permission=1)
        if data:
            self.render("datasetManage.html", user_infos=data)
        else:
            # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
            self.write("您没有进行此操作的权限!")

class DataSetAddHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        data = yield self.permission_verify(permission=1)
        if data:
            dsmd_id = self.get_argument("dsmd_di")    # 业务数据集标识符
            dsmd_name = self.get_argument("dsmd_name")   # 业务数据集名称

            dssmd_id_c = self.get_argument('dssmd_id_c')  # 基本数据集自定义标识符
            dssmd_id_g = self.get_argument('dssmd_id_g')  # 基本数据集国标标识符
            dssmd_id_p = self.get_argument('dssmd_id_p')  # 基本数据集省标标识符
            dssmd_name = self.get_argument('dssmd_name')  # 基本数据集名称

            if not dsmd_id or not dsmd_name:
                # self.write({"status_code": "-8"})  # 表示业务数据集标识符或业务数据集名称为空
                self.write("业务数据集标识符或业务数据集名称为空，请重新输入")
                return

            if not dssmd_id_c and not dssmd_id_p and not dssmd_id_g:
                # self.write({"status_code": "-8"})  # 表示基本数据集标识符为空
                self.write("基本数据集标识符为空，请重新输入")
                return
            if not dssmd_id_c:
                dssmd_id = dssmd_id_c
            elif not dssmd_id_g:
                dssmd_id = dssmd_id_g
            else:
                dssmd_id = dssmd_id_p

            dsmd_created_datetime = self.time_operate()   # 创建时间
            dsmd_status = 1  # 业务数据集状态 1 表插入 0 表删除
            dsmd_field_classification_1 = self.dsmd_field_classification_1(dsmd_id=dsmd_id)    # 业务数据集一级类目
            dsmd_field_classification_2 = self.dsmd_field_classification_2(dsmd_id=dsmd_id)  # 业务数据集二级类目

            dssmd__created_datetime = self.time_operate()   # 创建时间
            dssmd_status = 1  # 基本数据集状态 1 表插入 0 表删除
            dssmd_field_classfication_1 = self.dssmd_field_classification_1(dssmd_id)  # 基本数据集一级类目
            dssmd_field_classfication_2 = self.dssmd_field_classification_2(dssmd_id)  # 基本数据集二级类目
            dssmd_field_classfication_3 = self.dssmd_field_classification_3(dssmd_id)  # 基本数据集三级类目

            try:
                future = self.db.execute('select * from DATASET_META_DATA where DSMD_ID = %s', (dsmd_id))  # 根据业务数据集标识符查询数据集
                yield future
                cursor = future.result()
                try:
                    future1 = self.db.execute('select DATASUBSET_META_DATA.DSMD_INC_PK  from DATASUBSET_META_DATA JOIN DATASET_META_DATA ON DATASET_META_DATA.DSMD_INC_PK =  DATASUBSET_META_DATA.DSMD_INC_PK ')
                    yield future1
                except Exception:
                    try:
                        future = self.db.execute(
                            'INSERT INTO DATASUBSET_META_DATA(DSMD_INC_PK, DSSMD_ID_C, DSSMD_ID_G, DSSMD_ID_P, DSSMD_FIELD_CLASSIFICATION_1, DSSMD_FIELD_CLASSIFICATION_2, DSSMD_FIELD_CLASSIFICATION_3, DSSMD_NAME,DSSMD_CREATED_DATETIME, DSSMD_STATUS)VALUES(dsmd_inc_pk, dssmd_id_c, dssmd_id_g, dssmd_id_p, dssmd_field_classification_1, dssmd_field_classification_2, dssmd_field_classification_3, dssmd_name,dssmd_created_datetime, dssmd_status)')  # 创建数据子集
                        yield future
                    except Exception:
                        # self.write({"status_code": "-15"})  # 表示基本数据集失败
                        self.write("新增基本数据集失败")
                    else:
                        # self.write({"status_code": "20"})  # 表示新增基本数据集成功
                        self.write("新增基本数据集成功")
                else:
                    # self.write({"status_code": "-18"})  # 表示新增基本数据集及数据子集失败,已有该数据子集
                    self.write("新增基本数据集及数据子集失败,已有该数据子集")
            except Exception:
                try:
                    future = self.db.execute(
                        'INSERT INTO DATASET_META_DATA(DSMD_ID , DSMD_FIELD_CLASSIFICATION_1, DSMD_FIELD_CLASSIFICATION_2, DSMD_NAME, DSMD_STATUS,DSMD_CREATED_DATETIME)VALUES(dsmd_id , dsmd_field_classification_1, dsmd_field_classification_2, dsmd_name, dsmd_status,dsmd_created_datetime)')  # 创建业务数据集
                    yield future
                except Exception:
                    # self.write({"status_code": "-15"})  # 表示新增业务数据集失败
                    self.write("新增业务数据集失败")
                else:
                    # self.write({"status_code": "20"})  # 表示新增业务数据集成功
                    self.write("新增业务数据集成功")
            else:
                # self.write({"status_code": "-18"})  # 表示新增业务数据集失败,已有该业务数据集
                self.write("新增业务数据集失败,已有该业务数据集")
        else:
            # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
            self.write("您没有进行此操作的权限!")

class DataSetModifyHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        data = yield self.permission_verify(permission=1)
        if data:
            dsmd_id = self.get_argument("dsmd_di")  # 业务数据集标识符
            dsmd_name = self.get_argument("dsmd_name")  # 业务数据集名称

            dssmd_id_c = self.get_argument('dssmd_id_c')  # 基本数据集自定义标识符
            dssmd_id_g = self.get_argument('dssmd_id_g')  # 基本数据集国标标识符
            dssmd_id_p = self.get_argument('dssmd_id_p')  # 基本数据集省标标识符
            dssmd_name = self.get_argument('dssmd_name')  # 基本数据集名称

            if not dsmd_id or not dsmd_name:
                # self.write({"status_code": "-8"})  # 表示业务数据集标识符或业务数据集名称为空
                self.write("业务数据集标识符或业务数据集名称为空，请重新输入")
                return

            if not dssmd_id_c and not dssmd_id_p and not dssmd_id_g:
                # self.write({"status_code": "-8"})  # 表示基本数据集标识符为空
                self.write("基本数据集标识符为空，请重新输入")
                return
            if not dssmd_id_c:
                dssmd_id = dssmd_id_c
            elif not dssmd_id_g:
                dssmd_id = dssmd_id_g
            else:
                dssmd_id = dssmd_id_p

            dsmd_created_datetime = self.time_operate()  # 创建时间
            dsmd_status = 1  # 业务数据集状态 1 表插入 0 表删除
            dsmd_field_classification_1 = self.dsmd_field_classification_1(dsmd_id=dsmd_id)  # 业务数据集一级类目
            dsmd_field_classification_2 = self.dsmd_field_classification_2(dsmd_id=dsmd_id)  # 业务数据集二级类目

            dssmd__created_datetime = self.time_operate()  # 创建时间
            dssmd_status = 1  # 基本数据集状态 1 表插入 0 表删除
            dssmd_field_classfication_1 = self.dssmd_field_classification_1(dssmd_id)  # 基本数据集一级类目
            dssmd_field_classfication_2 = self.dssmd_field_classification_2(dssmd_id)  # 基本数据集二级类目
            dssmd_field_classfication_3 = self.dssmd_field_classification_3(dssmd_id)  # 基本数据集三级类目

            try:
                future = self.db.execute('select * from DATASET_META_DATA where DSMD_ID = %s',
                                         (dsmd_id))  # 根据业务数据集标识符查询数据集
                yield future
                # cursor = future.result()
                try:
                    future = self.db.execute( 'update DATASET_META_DATA set DSMD_NAME = dsmd_name, DSMD_CREATED_DATETIME=dsmd_created_datetime  where DSMD_ID = dsmd_id')  # 根据业务数据集标识符更新数据库
                    yield future
                except Exception:
                    # self.write({"status_code": "-18"})  # 表示更新业务数据集及数据集失败,
                    self.write("更新业务数据集及数据集失败")
                else:
                    # self.write({"status_code": "18"})  # 表示更新业务数据集及数据集成功
                    self.write("更新业务数据集及数据集成功")
            except Exception:
                # self.write({"status_code": "-21"})  # 表示更新业务数据集失败，没有该业务数据集
                self.write("表示更新业务数据集失败，没有该业务数据集")
                # self.redirect("/datasetManage/add")
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

                    dsmd_name = self.get_argument("dsmd_name")  #

                    if not dsmd_name:  # 输入为空
                        try:
                            future = self.db.execute('select * from DATASET_META_DATA')
                            yield future
                            cursor = future.result()
                            self.write({"data": cursor.fetchall(), "status_code": "11"})  # 查询业务数据集成功
                            self.write("查询业务数据集成功")
                        except Exception:
                            # self.write({"status_code": "-11"})  # 表示查询业务数据集失败
                            self.write("查询业务数据集失败")
                        finally:
                            self.finish()
                    else:
                        try:
                            future = self.db.execute('select * from DATAELEMENT where DE_DI = %s and DE_STATUS = 1',(dsmd_name))  # 根据业务数据名称查询
                            yield future
                            cursor = future.result()
                            self.write({"data": cursor.fetchone(), "status_code": "11"})  # 查询业务数据集成功
                            self.write("查询业务数据集成功")
                        except Exception:
                            # self.write({"status_code": "-11"})  # 表示查询业务数据集失败
                            self.write("查询业务数据集失败")
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
        data = yield self.permission_verify(permission=1)
        if data:
            dsmd_id = self.get_argument("dsmd_di")  # 业务数据集标识符
            dsmd_name = self.get_argument("dsmd_name")  # 业务数据集名称

            dssmd_id_c = self.get_argument('dssmd_id_c')  # 基本数据集自定义标识符
            dssmd_id_g = self.get_argument('dssmd_id_g')  # 基本数据集国标标识符
            dssmd_id_p = self.get_argument('dssmd_id_p')  # 基本数据集省标标识符
            dssmd_name = self.get_argument('dssmd_name')  # 基本数据集名称

            if not dsmd_id or not dsmd_name:
                # self.write({"status_code": "-8"})  # 表示业务数据集标识符或业务数据集名称为空
                self.write("业务数据集标识符或业务数据集名称为空，请重新输入")
                return

            if not dssmd_id_c and not dssmd_id_p and not dssmd_id_g:
                # self.write({"status_code": "-8"})  # 表示基本数据集标识符为空
                self.write("基本数据集标识符为空，请重新输入")
                return
            if not dssmd_id_c:
                dssmd_id = dssmd_id_c
            elif not dssmd_id_g:
                dssmd_id = dssmd_id_g
            else:
                dssmd_id = dssmd_id_p

            dsmd_created_datetime = self.time_operate()  # 创建时间
            dsmd_status = 0  # 业务数据集状态 1 表插入 0 表删除
            dsmd_field_classification_1 = self.dsmd_field_classification_1(dsmd_id=dsmd_id)  # 业务数据集一级类目
            dsmd_field_classification_2 = self.dsmd_field_classification_2(dsmd_id=dsmd_id)  # 业务数据集二级类目

            dssmd__created_datetime = self.time_operate()  # 创建时间
            dssmd_status = 0  # 基本数据集状态 1 表插入 0 表删除
            dssmd_field_classfication_1 = self.dssmd_field_classification_1(dssmd_id)  # 基本数据集一级类目
            dssmd_field_classfication_2 = self.dssmd_field_classification_2(dssmd_id)  # 基本数据集二级类目
            dssmd_field_classfication_3 = self.dssmd_field_classification_3(dssmd_id)  # 基本数据集三级类目
            try:   # 删除前先判断
                future = self.db.execute('select * from DATASET_META_DATA where DSMD_ID = %s', (dsmd_id))  # 根据业务数据集标识符查询数据集
                yield future
                try:
                    future = self.db.execute('update DATASET_META_DATA set DSMD_STATUS=dsmd_status  where DSMD_ID = %s', (dsmd_id))  # 根据业务数据集标识符删除数据集
                    yield future
                    try:
                        future = self.db.execute(
                            'update DATASUBSET_META_DATA set DSSMD_STATUS=dssmd_status  where DATASUBSET_META_DATA.DSMD_INC_PK = DATASET_META_DATA.DSMD_INC_PK')  # 根据业务数据集标识符删除数据集
                        yield future
                    except Exception:
                        # self.write({"status_code": "-18"})  # 表示删除数据子集失败
                        self.write("删除数据子集失败")
                    else:
                        self.write({"status": "23"})  # 删除业务数据集成功
                        self.write("删除业务数据集成功")
                except Exception:
                    # self.write({"status_code": "-18"})  # 表示删除业务数据集失败
                    self.write("删除业务数据集失败")
            except Exception:
                # self.write({"status_code": "-19"})  # 表示删除业务数据集失败，没有该业务数据集
                self.write("删除业务数据集失败,没有该业务数据集")
                self.redirect("/datasetManage/add")
            finally:
                self.finish()
        else:
            # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
            self.write("您没有进行此操作的权限!")


# 基本数据集即数据子集 #########################################################

class datasubsetManageHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        data = yield self.permission_verify(permission=1)
        if data:
            self.render("datasubsetManage.html", user_infos=data)
        else:
            # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
            self.write("您没有进行此操作的权限!")

class datasubsetAddHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        data = yield self.permission_verify(permission=1)

        if data:
            dssmd_name = self.get_argument('dssmd_name')  # 基本数据集名称
            de_name = self.get_argument('de_name')   # 数据元名称
            # de_rid_c, de_rid_g, de_rid_p, dss_de_status
            try:
                future = self.db.execute(
                    'select *  from DATASUBSET_META_DATA WHERE DSSMD_NAME = %s ', (dssmd_name))  # 根据基本数据集名称查询基本数据集
                yield future
                cursor = future.result()
                data_result = cursor.fetchone()

                dssmd_inc_pk = data_result[0]

                dssmd_id_c = data_result[2]
                dssmd_id_g = data_result[3]
                dssmd_id_p = data_result[4]

                f = self.num_increase(1000) # 生成顺序号
                # 生成数据元内部标识符
                if dssmd_id_c:
                    de_rid_c = dssmd_id_c + self.num_format(f.next())
                else:
                    de_rid_c = dssmd_id_c
                if dssmd_id_g:
                    de_rid_g = dssmd_id_g + self.num_format(f.next())
                else:
                    de_rid_g = dssmd_id_g
                if dssmd_id_p:
                    de_rid_p = dssmd_id_p + self.num_format(f.next())
                else:
                    de_rid_p = dssmd_id_p

                dss_de_status = 1

                try:
                    future2 = self.db.execute(
                        'select *  from DATASUBSET JOIN DATAELEMENT ON DATAELEMENT.DE_INC_PK = DATASUBSET.DE_INC_PK WHERE DE_NAME = %s ', (de_name))  # 根据数据元名称查询基本数据集
                    yield future2
                    # self.write({"status_code": "-15"})  # 表示新增数据元失败，已有该数据元
                    self.write("新增数据元失败，已有该数据元")
                except Exception:
                    try:
                        future1 = self.db.execute(
                        'INSERT INTO DATASUBSET(DSSMD_INC_PK, DE_RID_C, DE_RID_G,DE_RID_P, DSS_DE_STATUS ) VALUES(dssmd_inc_pk, de_rid_c, de_rid_g,de_rid_p, dss_de_status) ')   # 插入数据元到数据子集中
                        yield future1
                    except Exception:
                        # self.write({"status_code": "-15"})  # 表示新增数据元失败
                        self.write("新增数据元失败")
            except Exception:
                # self.write({"status_code": "-21"})  # 表示添加数据子集数据元失败，没有该数据子集
                self.write("添加数据子集数据元失败，没有该数据子集")
                # self.redirect("/datasetManage/add")
        else:
            # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
            self.write("您没有进行此操作的权限!")


class datasubsetModifyHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        data = yield self.permission_verify(permission=1)
        if data:
            dssmd_id = self.get_argument('dssmd_id')  # 基本数据集标识符
            try:
                future = self.db.execute(
                    'update DATASUBSET_META_DATA set DSSMD_NAME = dssmd_name, DSSMD_CREATED_DATETIME=dssmd_created_datetime  where DSSMD_ID = dssmd_id')  # 根据业务数据集标识符更新数据库
                yield future
            except Exception:
                # self.write({"status_code": "-18"})  # 表示更新基本数据集及数据集失败,
                self.write("更新基本数据集及数据集失败")
            else:
                # self.write({"status_code": "18"})  # 表示更新基本数据集及数据集成功
                self.write("更新基本数据集及数据集成功")
        else:
            # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
            self.write("您没有进行此操作的权限!")

class datasubsetSearchHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
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

                    dssmd_name = self.get_argument("dssmd_name")  #

                    if not dssmd_name:  # 输入为空
                        try:
                            future = self.db.execute('select * from DATASUBSET_META_DATA')
                            yield future
                            cursor = future.result()
                            self.write({"data": cursor.fetchall(), "status_code": "11"})  # 查询基本数据集成功
                            self.write("查询基本数据集成功")
                        except Exception:
                            # self.write({"status_code": "-11"})  # 表示查询业务数据集失败
                            self.write("查询基本数据集失败")
                        finally:
                            self.finish()
                    else:
                        try:
                            future = self.db.execute('select * from DATASUBSET_META_DATA where DSSMD_NAME = %s and DE_STATUS = 1',
                                                     (dssmd_name))  # 根据基本数据名称查询
                            yield future
                            cursor = future.result()
                            self.write({"data": cursor.fetchone(), "status_code": "11"})  # 查询基本数据集成功
                            self.write("查询基本数据集成功")
                        except Exception:
                            # self.write({"status_code": "-11"})  # 表示基本业务数据集失败
                            self.write("查询基本数据集失败")
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


class datasubsetDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        data = yield self.permission_verify(permission=1)
        dssmd_id = self.get_argument("dssmd_id")
        dssmd_status = 0   #  0 表删除
        dss_de_status = 0
        if data:

            try:  # 删除前先判断
                future = self.db.execute('select * from DATASUBSET_META_DATA where DSSMD_ID = %s',
                                         (dssmd_id))  # 根据基本数据集标识符查询数据集
                yield future
                try:
                    future = self.db.execute('update DATASUBSET_META_DATA set DSSMD_STATUS=dssmd_status  where DSSMD_ID = %s',
                                             (dssmd_id))  # 根据业务数据集标识符删除数据集
                    yield future
                    try:
                        future = self.db.execute(
                            'update DATASUBSET set DSS_DE_STATUS=dss_de_status  where DATASUBSET_META_DATA.DSSMD_INC_PK = DATASUBSET.DSSMD_INC_PK')  # 根据业务数据集标识符删除数据集
                        yield future
                    except Exception:
                        # self.write({"status_code": "-18"})  # 表示删除数据子集中的数据元失败
                        self.write("删除数据子集中的数据元失败")
                    else:
                        self.write({"status": "23"})  # 删除删除数据子集中的数据元成功
                        self.write("删除数据子集中的数据元成功")
                except Exception:
                    # self.write({"status_code": "-18"})  # 表示基本业务数据集失败
                    self.write("删除基本数据集失败")
            except Exception:
                # self.write({"status_code": "-19"})  # 表示删基本数据集失败，没有该基本数据集
                self.write("删除基本数据集失败,没有该基本数据集")
                self.redirect("/datasetManage/add")
            finally:
                self.finish()
        else:
            # self.write({"status_code": "-6"})  # 您没有进行此操作的权限!
            self.write("您没有进行此操作的权限!")

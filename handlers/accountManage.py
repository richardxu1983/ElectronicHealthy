#coding:utf-8

import tornado.web
import tornado.escape
import methods.writedb as writedb

from base import BaseHandler

class ChangePassword(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        if self.judge_info() != False:
            self.render("changePassword.html")

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        if self.judge_info() != False:
            username = tornado.escape.json_decode(self.current_user)  # 获取cookie中的用户名
            old_password = self.get_argument("old_password")
            new_password1 = self.get_argument("new_password1")
            new_password2 = self.get_argument("new_password2")
            if self.compare_password(username, old_password) == True:
                if new_password1 == new_password2:
                    if old_password != new_password1:
                        if self.password_format(new_password1) == "104":
                            self.write({"status_code":"104"})#新密码中有空格
                        elif self.password_format(new_password1) == "105":
                            self.write("105")#新密码长度不正确
                        else:
                            new_salt = self.random_salt()
                            new_password_hash = self.result_hash(username=username, password=new_password1)
                            dbresult = writedb.changePassword(table="user_infos", u_account=username, u_password_hash=new_password_hash, u_salt=new_salt)
                            if dbresult == False:#数据库修改失败
                                self.write("500")
                            elif dbresult == True:#数据库修改成功
                                self.write("200")
                    else:
                        self.write("103")#输入的新密码与原密码相同
                else:
                    self.write("102")#输入的密码不相同
            else:
                self.write("101")#原密码错误
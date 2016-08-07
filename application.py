# coding=utf-8

import tornado.web
import os
import momoko

from url import url

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),#设置静态页面路径
    static_path=os.path.join(os.path.dirname(__file__), "statics"),#设置css,js文件路径
    cookie_secret="qwsBnAr/SYude9L/uPmYEovG8H9rx07CsL+Ep1/HA78=",#加密cookie   #base64.b64encode(uuid.uuid4().bytes)
    xsrf_cookies=True,#解决跨站请求伪造XSRF
    login_url='/'
)

application = tornado.web.Application(
    handlers=url,
    **settings
)

application.db = momoko.Pool(
    dsn='dbname=health user=postgres password=ywcdgqb168 '
    'host=localhost port=5432',
    size=1,
)

future = application.db.connect()
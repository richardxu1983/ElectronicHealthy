# coding=utf-8

import sys
reload(sys)

from handlers.index import LoginHandler, IndexHandler
from handlers.userManage import UserManageHandler, UserAddHandler, UserModifyHandler, UserDeleteHandler, UserSearchHandler
from handlers.dataelementManage import DataElementAddHandler,DataElementModifyHandler, DataElementSearchHandler, DataElementDeleteHandler,DataElementManageHandler
from handlers.valuefieldManage import ValueFieldManageHandler,ValueFieldAddHandler,ValueFieldDeleteHandler,ValueFieldModifyHandler,ValueFieldSearchHandler
url = [
    (r'/', LoginHandler),
    (r'/index', IndexHandler),
    (r'/userManage', UserManageHandler),
    (r'/userManage/add', UserAddHandler),
    (r'/userManage/modify', UserModifyHandler),
    (r'/userManage/delete', UserDeleteHandler),
    (r'/userManage/search', UserSearchHandler),
    (r'/dataelementManage', DataElementManageHandler),
    (r'/dataelementManageadd', DataElementAddHandler),
    (r'/dataelementManagemodify', DataElementModifyHandler),
    (r'/dataelementManagedelete', DataElementSearchHandler),
    (r'/dataelementManagesearch', DataElementDeleteHandler),
    (r'/valuefieldManage', ValueFieldManageHandler),
    (r'/valuefieldManage/add', ValueFieldAddHandler),
    (r'/valuefieldManage/modify', ValueFieldModifyHandler),
    (r'/valuefieldManage/delete', ValueFieldDeleteHandler),
    (r'/valuefieldManage/search', ValueFieldSearchHandler),
]


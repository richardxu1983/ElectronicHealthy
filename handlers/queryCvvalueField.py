#coding:utf-8

import tornado.web
import tornado.escape
import json
import  methods.readdb as readdb

from base import BaseHandler

class QueryCvvalueFieldHandler(BaseHandler):
    def get(self):
        if self.judge_info() !=False:
            self.render("queryCvvalueField.html")

    def post(self, *args, **kwargs):
        if self.judge_info() != False:
            cv_value_field = self.get_argument("cv_value_field")
            cv_value_field_infos = readdb.select_table(table="cvvaluefield", column="*", condition="cvvf_oid",
                                                   value=cv_value_field)

            if cv_value_field_infos:
                cvvf_status = cv_value_field_infos[0][7]
                if cvvf_status == 0:
                    cv_value_field_value_infos = readdb.select_table(table="cvvaluefield_value", column="*", condition="cvvf_inc_pk",
                                                                       value=bytes(cv_value_field_infos[0][0]))
                    use_cv_value_field_value_infos = []
                    use_cv_value_field_value_dict = dict()
                    for i in range(0, len(cv_value_field_infos)+1, 1):
                        use_cv_value_field_value_dict['cvvf_inc_pk'] = cv_value_field_infos[0][0]
                        use_cv_value_field_value_dict['cvvf_oid'] = cv_value_field_infos[0][1]
                        use_cv_value_field_value_dict['cvvf_code'] = cv_value_field_infos[0][2]
                        use_cv_value_field_value_dict['cvvf_classification_1'] = cv_value_field_infos[0][3]
                        use_cv_value_field_value_dict['cvvf_classification_2'] = cv_value_field_infos[0][4]
                        use_cv_value_field_value_dict['cvvf_name'] = cv_value_field_infos[0][5]
                        use_cv_value_field_value_dict['cvvf_classification'] = cv_value_field_infos[0][6]
                        use_cv_value_field_value_dict['cvvf_status'] = cv_value_field_infos[0][7]
                        use_cv_value_field_value_dict['cvvf_created_datetime'] = cv_value_field_infos[0][8]
                        use_cv_value_field_value_dict['v_inc_pk'] = cv_value_field_value_infos[i][0]
                        use_cv_value_field_value_dict['cvvf_value'] = cv_value_field_value_infos[i][2]
                        use_cv_value_field_value_dict['cvvf_defination'] = cv_value_field_value_infos[i][3]
                        use_cv_value_field_value_dict['cvvf_note'] = cv_value_field_value_infos[i][4]
                        use_cv_value_field_value_infos.append(use_cv_value_field_value_dict)
                    print "查询结果json数组为use_cv_value_field_value_infos%s" % use_cv_value_field_value_infos

                    def date_handler(obj):
                        if hasattr(obj, 'isoformat'):
                            return obj.isoformat()
                        else:
                            raise TypeError

                    self.write(json.dumps(use_cv_value_field_value_infos, default=date_handler))
                elif cvvf_status == 1:
                    self.write("0")
            else:
                self.write("-1")


    def ErrorHandler(BaseHadler):
        def get(self, *args, **kwargs):
            self.render("error.html")



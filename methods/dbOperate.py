# coding=utf-8

# 根据字段获取表指定内容
def select_table(table, column, condition, value):
    sql = "select " + column + " from " + table + " where " + condition + " =' " + value + "'"
    return sql
#coding:utf-8
from __future__ import unicode_literals
import smtplib
from email.mime.text import MIMEText
from email.header import Header

mailto_list = ["931094193@qq.com","1547073674@qq.com"] #发送名单
mail_host = "smtp.sina.com"
mail_user = "grateful_r@sina.com" #新浪试用邮箱帐号
mail_pass = "931094193@qq.com"    #密码


def send_mail(to_list, sub, content):
    me =  mail_user
    msg = MIMEText(content, _subtype='html', _charset="gb2312")
    msg['Subject'] = sub
    msg['From'] = mail_user
    msg['To'] = ",".join(to_list)
    # subject = 'Python SMTP 邮件测试'
    # msg['Subject'] = Header(subject, 'utf-8')
    try:
        s = smtplib.SMTP()
        s.connect(mail_host, 25)
        s.login(mail_user, mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False
if __name__ == '__main__':
    if send_mail(mailto_list,"主题hello","<a href='http://www.baidu.com'>点击跳转</a>密码是22222"):
        print "发送成功"
    else:
        print "发送失败"


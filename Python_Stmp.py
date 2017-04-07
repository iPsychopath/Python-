#   导入模块
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

# 输入Email地址和口令:
from_addr = input('From: ')
password = input('Password: ')
# 输入收件人地址:
to_addr = input('To: ')
# 输入SMTP服务器地址:
smtp_server = input('SMTP server: ')

# msg = MIMEText('hello, send by Python...\r\nI just want to say that Li Jingfeng is rubbish', 'plain', 'utf-8')
i=20
while i<21:
    msg = MIMEText('<html><body>' +
        '<p><a href="#">Hello World</a></p>' +
        '</body></html>', 'html', 'utf-8')
    msg['From'] = _format_addr('Python学习者'+str(i)+' <%s>' % from_addr)
    msg['To'] = _format_addr('管理员'+str(i)+' <%s>' % to_addr)
    msg['Subject'] = Header('来自Python'+str(i)+'发送的邮件', 'utf-8').encode()
    #   SMTP协议默认端口是25
    server = smtplib.SMTP(smtp_server, 25)
    #   关闭调试模式
    server.set_debuglevel(0)
    #   登陆到smtp服务器
    server.login(from_addr, password)
    #   发送邮件
    server.sendmail(from_addr, [to_addr], msg.as_string())
    #   断开与smtp服务器的连接
    server.quit()
    i=i+1

import smtplib
from email.message import EmailMessage
from email.utils import formataddr

from_email_addr = "3394601452@qq.com"
from_email_pass = "zcmsurwgnavjdacd"
to_email_addr = "3394601452@qq.com"

msg = EmailMessage()

body = "Hello from Raspberry Pi"
msg.set_content(body)

msg['From'] = from_email_addr
msg['To'] = to_email_addr

msg['Subject']= 'TEST EMAIL'

server = smtplib.SMTP_SSL('smtp.qq.com',465)
server.login(from_email_addr, from_email_pass)
server.send_message(msg)
print('Email sent')
server.quit()

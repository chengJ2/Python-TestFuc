#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

attach_file = "C:\\Users\\wh1510032\\Desktop\\001.xlsx"
attach_file2 = "C:\\Users\\wh1510032\\Desktop\\Test.txt"

def send_mail(mail_send_list,subject,content):
	"'发送普通邮件'"
	mail_send_user = ""
	mail_send_pwd = ""
	msg = MIMEText(content,_charset='utf-8')
	#msg = MIMEText('<html><body><h1>Hello</h1>' +
    #'<p>send by <a href="http://www.python.org">Python</a>...</p>' +
    #'</body></html>', 'html', 'utf-8')
	msg['Subject'] = subject
	msg['From'] = mail_send_user
	msg['To'] = mail_send_list
	try:
		s = smtplib.SMTP_SSL('smtp.163.com') #连接邮箱服务器，默认端口号25
		s.login(mail_send_user,mail_send_pwd) #登录邮箱
		s.sendmail(mail_send_user,mail_send_list,msg.as_string()) #发送邮件
		s.quit() #发送完毕，退出smtp
		return True
	except Exception as e:
		print (str(e))
		return False

def send_attach_mail(mail_send_list,subject,content,attach_file):
	"'发送带附件的邮件'"
	mail_send_user = ""
	mail_send_pwd = ""
	msg = MIMEMultipart() # 邮件内容
	# 读取文件，可以发送复杂附件，如Execl等
	attach = MIMEText(open(attach_file,'rb').read(),'base64','utf-8')
	# 指定当前文件格式类型
	attach['Content-type'] = 'application/octet-stream'
	# 设置附件信息
	attach['Content-Disposition'] = 'attachment;filename="%s"' %os.path.basename(attach_file)
	msg.attach(attach) # 添加附件
	msg.attach(MIMEText(content,_charset='utf-8'))
	msg['Subject'] = subject
	msg['From'] = mail_send_user
	msg['To'] = mail_send_list
	try:
		s = smtplib.SMTP_SSL('smtp.163.com') #连接邮箱服务器，默认端口号25
		s.login(mail_send_user,mail_send_pwd) #登录邮箱
		s.sendmail(mail_send_user,mail_send_list,msg.as_string()) #发送邮件
		s.quit() #发送完毕，退出smtp
		return True
	except Exception as e:
		print (str(e))
		return False

def send_attachs_mail(mail_send_list,subject,content,attach_file):
	"'发送多个附件的邮件'"
	mail_send_user = ""
	mail_send_pwd = ""

	msgRoot = MIMEMultipart() # 邮件内容
	msgRoot['Subject'] = subject
	msgRoot['From'] = mail_send_user
	msgRoot['To'] = mail_send_list

	part = MIMEText(content,_charset='utf-8') 
	msgRoot.attach(part)

	# 添加附件部分
	for path in attach_file:
		if ".xlsx" in path:
			#xlsx类型附件
			xlsx_name = path.split("\\")[-1]
			part = MIMEApplication(open(path,'rb').read()) 
			part.add_header('Content-Disposition', 'attachment', filename=xlsx_name)
			msgRoot.attach(part)
            
		if ".txt" in path:
			#txt类型附件
			txt_name = path.split("\\")[-1]
			part = MIMEApplication(open(path,'rb').read())
			part.add_header('Content-Disposition', 'attachment', filename=txt_name)
			msgRoot.attach(part)

		if ".pdf" in path:
			#txt类型附件
			pdf_name = path.split("\\")[-1]
			part = MIMEApplication(open(path,'rb').read())
			part.add_header('Content-Disposition', 'attachment', filename=pdf_name)
			msgRoot.attach(part)
	
	try:
		s = smtplib.SMTP_SSL('smtp.163.com') #连接邮箱服务器，默认端口号25
		s.login(mail_send_user,mail_send_pwd) #登录邮箱
		s.sendmail(mail_send_user,mail_send_list,msgRoot.as_string()) #发送邮件
		s.quit() #发送完毕，退出smtp
		return True
	except Exception as e:
		print (str(e))
		return False

import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

def receiveEmail():
	# 连接到POP3服务器:
	server = poplib.POP3('pop.163.com')
	# 可以打开或关闭调试信息:
	server.set_debuglevel(1)
	# 可选:打印POP3服务器的欢迎文字:
	print(server.getwelcome().decode('utf-8'))

	server.user('13667258212@163.com')
	server.pass_('')
	# stat()返回邮件数量和占用空间:
	print('Messages: %s. Size: %s' % server.stat())
	# list()返回所有邮件的编号:
	resp, mails, octets = server.list()
	# 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
	#print(mails)
	# 获取最新一封邮件, 注意索引号从1开始:
	index = len(mails)
	resp, lines, octets = server.retr(index)

	# lines存储了邮件的原始文本的每一行,
	# 可以获得整个邮件的原始文本:
	msg_content = b'\r\n'.join(lines).decode('utf-8')
	# 稍后解析出邮件:
	msg = Parser().parsestr(msg_content)

	printEmailInfo(msg,0)

	# 可以根据邮件索引号直接从服务器删除邮件:
	# server.dele(0)
	# 关闭连接:
	server.quit()


def printEmailInfo(msg,indent=0):
	if indent == 0:
		for header in ['From','To','Subject']:
			value = msg.get(header,'')
			if value:
				if header == 'Subject':
					value = decode_str(value)
				else:
					hdr,addr = parseaddr(value)
					name = decode_str(hdr)
					value = u'%s <%s>' % (name, addr)
	if (msg.is_multipart()):
		parts = msg.get_payload()
		for n,part in enumerate(parts):
			#print('%spart %s' % ('  ' * indent, n))
			#print('%s--------------------' % ('  ' * indent))
			printEmailInfo(part, indent + 1)
	else:
		content_type = msg.get_content_type()
		print (content_type)
		if content_type == 'text/plain' or content_type == 'text/html':
			content = msg.get_payload(decode=True)
			charset = guess_charset(msg)
			if charset:
				content = content.decode(charset)
			print('%sText: %s' % ('  ' * indent, content + '...'))
		else:
			print('%sAttachment: %s' % ('  ' * indent, content_type))
		
# 邮件的Subject或者Email中包含的名字都是经过编码后的str，要正常显示，就必须decode：
def decode_str(s):
	value,charset = decode_header(s)[0] #返回一个list，因为像Cc、Bcc这样的字段可能包含多个邮件地址，所以解析出来的会有多个元素。
	if charset:
		value = value.decode(charset)
	return value

def guess_charset(msg):
	charset = msg.get_charset()
	if charset is None:
		content_type = msg.get('Content-Type','').lower()
		pos = content_type.find('charset=')
		if pos > 0:
			charset = content_type[pos + 8:].strip()
	return charset

if __name__ == '__main__':
	# 收件人列表，多个人用;隔开
	#mail_send_list='1042838789@qq.com'
	#if send_mail(mail_send_list, "subject", "content"):
	#if send_attach_mail(mail_send_list, "attach file subject", "attach file content", attach_file):
	#if send_attachs_mail(mail_send_list, "attach file subject", "attach file content",[attach_file,attach_file2]):
	#	print ("Send success")
	#else:
	#	print ("Send fail")
	receiveEmail()

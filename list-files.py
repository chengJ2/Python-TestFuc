#!/usr/bin/env python3
# -*- coding：utf-8 -*-

import os

def saveFiles(path,key):	
	'列出某个目录下的所有文件并保存到list.txt文件里'
	os.chdir(path)
	for x in os.listdir(path):
		if os.path.isfile(x) and os.path.splitext(x)[0].__contains__(key):
			#print (os.path.join(path, x))
			with open(os.path.join(cur,"list.txt"),'a+') as f:
				f.writelines(os.path.join(path, x) + "\n")
			#try:
			#	f = open(os.path.join(cur,"list.txt\n"),'a+')
			#	f.write(os.path.join(path, x))
			#finally:
			#	if f:
			#		f.close()
		if os.path.isdir(x):
			dir = os.path.join(path,x)
			saveFiles(dir,key)
			os.chdir(os.pardir)

if __name__ == '__main__':
	cur = os.path.abspath('.')
	#cur = os.getcwd()
	curpath = os.path.join(cur,"testdir")
	print ('curpath: %s' % curpath)
	saveFiles(curpath,'')


file = 'E:/PyWork/BaseCore/note.txt'

#with open(file, 'w') as f:
#	f.write('I\'m learning')


#try:
#	f = open(file, 'r')
#	print (f.read())
#finally:
#	if f:
#		f.close()
#print ("=====引入了with语句来自动调用close()方法=========")
#with open(file, 'r') as f:
#    print(f.read())

#with open('E:/PyWork/BaseCore/note.txt', 'r', encoding='gbk') as f:
#	 print(f.read())


#print ("操作系统类型:%s"%os.name) 
# 结果如果是posix：为Linux、Unix或Mac OS X系统
# 结果如果是nt，就是Windows系统
#print ("环境变量:%s"%os.environ) # 列出在操作系统中定义的环境变量
#print("当前目录:%s"%os.getcwd()) 
# 结果为：E:\PyWork\BaseCore
#print("当前操作系统的路径分隔符:%s"%os.sep)
#print(os.rename('temp.txt','temp_new.txt'))#修改文件名称
#print(os.mkdir('newFolder'))#创建文件夹
#print(os.rmdir('newFolder'))#删除文件夹（只能删除空文件夹）
#print(os.makedirs('E:\\PyWork\\BaseCore\\testdir\\temp'))#依次创建目录
#print(os.removedirs('E:\\testdir\\temp'))#依次删除非空目录
#print("当前文件的绝对路径:%s"%os.path.abspath(__file__)) 
# 结果为：E:\PyWork\BaseCore\os.py
#print(os.path.isdir(os.path.abspath(__file__)))
#判断指定路径是不是一个文件夹，结果为False
#print(os.path.isfile(os.path.abspath(__file__)))
#判断指定路径是不是一个文件，结果为True
#print(os.path.split(os.path.abspath(__file__))) #拆分路径
# 结果类型为temple：('E:\\PyWork\\BaseCore', 'os.py')
#print(os.path.splitext(os.path.abspath(__file__))) #文件扩展名
# 结果类型为temple：('E:\\PyWork\\BaseCore\\os', '.py')


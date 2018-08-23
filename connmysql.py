#!/usr/bin/env python3
# -*- coding：utf-8 -*-

import MySQLdb
#import pymysql
#import mysql.connector
import json

db_config = {
	'host': '127.0.0.1',
	'user': 'root',
	'passwd': '******',
	'port': 3306,
	'db': 'test',
	'charset': 'utf8'
}

def connDB():
	try:
		#  MySQLdb.connect
		#  mysql.connector.connect
		conn = MySQLdb.connect(host=db_config['host'],
			user=db_config['user'],passwd=db_config['passwd'],
			port=db_config['port'],charset=db_config['charset'])
		conn.autocommit(True)
		curr = conn.cursor()
		curr.execute("SET NAMES %s" % db_config['charset'])
		curr.execute("USE %s" % db_config['db']);
		print ("== connect db success ==")
		return conn,curr
	except MySQLdb.Error as e:
		print ("Mysql Error %d: %s" % (e.args[0], e.args[1]))
		return None,None

def getCount(table=None,searchStr=None):
	try:
		cursor = connDB()[1]
		if table is None:
			return None
		if searchStr is None:
			sql = 'SELECT count(id) as cun FROM ' + table
		else:
			sql = "SELECT count(id) as cun FROM " + table 
			+ " WHERE name LIKE '%%%s%%'" %searchStr
		cursor.execute(sql)
		cun = cursor.fetchone()
		return cun[0]
	except MySQLdb.Error as e:
		print ("Mysql Error %d: %s" % (e.args[0], e.args[1]))
		return None
	finally:
		cursor.close()

def select(table=None,searchStr=None):
	data = {}
	try:
		cursor = connDB()[1]
		if table is None:
			return None
		if searchStr is None:
			sql = 'SELECT * FROM ' + table
		else:
			sql = "SELECT * FROM " + table +" WHERE name LIKE '%%%s%%'" %searchStr
		cursor.execute(sql)
		#results = cursor.fetchall()
		results = cursor.fetchmany(1)
		users = []
		for u in results:
			user = {}
			user['id'] = u[0]
			user['name'] = u[1]

			address =  {
				"street": "科技园路.",
				"city": "武汉光谷",
				"country": "中国"
			}
			user['address'] = address
			users.append(user)

		data['code'] = 200
		data['users'] = users
		jsonStr = json.dumps(data)

		return jsonStr
	except MySQLdb.Error as e:
		#print ("Mysql Error %d: %s" % (e.args[0], e.args[1]))
		data['code'] = str(e.args[0])
		data['msg'] = str(e.args[1])
		return json.dumps(data)
	except Exception as ex:
		#print ("Exception : %s" % ex)
		data['code'] = 404
		data['msg'] = str(ex)
		return json.dumps(data)
	finally:
		cursor.close()


def unionSelect(userId=None,searchStr=None):
	try:
		cursor = connDB()[1]
		if table is None:
			return None
		if searchStr is None:
			sql = "SELECT u.`id`,u.`name`,d.`address` FROM user u inner join user_detail d on u.id = d.user_Id and u.id = " + userId
		else:
			sql = "SELECT u.`id`,u.`name`,d.`address` FROM user u inner join user_detail d on u.id = d.user_Id and u.id = " + userId +" WHERE u.`name` LIKE '%%%s%%'" %searchStr

		cursor.execute(sql)
		results = cursor.fetchall()
		users = []
		data = {}
		for u in results:
			user = {}
			user['id'] = u[0]
			user['name'] = u[1]
			users.append(user)

		data['code'] = 200
		data['users'] = users
		jsonStr = json.dumps(data)

		return jsonStr
	except MySQLdb.Error as e:
		print ("Mysql Error %d: %s" % (e.args[0], e.args[1]))
		return None
	finally:
		cursor.close()		
	
def insertData(table=None,L=None):
	try:
		conn = connDB()[0]
		cursor = connDB()[1]
		if table is None:
			return None
		if L is None:
			return -1
		sql = "INSERT INTO " + table +" VALUES (%s,%s)"
		cursor.executemany(sql,L)
		conn.commit()
		return 1
	except MySQLdb.Error as e:
		print ("Mysql Error %d: %s" % (e.args[0], e.args[1]))
		return -1
	finally:
		cursor.close()
		conn.close()

def updateData(table=None,L=None):
	try:
		conn = connDB()[0]
		cursor = connDB()[1]
		if L is None:
			return -1
		sql = 'UPDATE user SET name = %s where id = %s'
		cursor.executemany(sql,L)
		conn.commit()
		return 1
	except MySQLdb.Error as e:
		print ("Mysql Error %d: %s" % (e.args[0], e.args[1]))
		conn.rollback()
		return -1
	finally:
		cursor.close()
		conn.close()

def deleteData(table=None,where=None):
	try:
		conn = connDB()[0]
		cursor = connDB()[1]
		if table is None:
			return None
		if where is None:
			sql = 'DELETE FROM ' + table
		else:
			sql = 'DELETE FROM '+ table + ' WHERE id in (%s)'
		cursor.execute(sql,where)
		conn.commit()
		return 1
	except MySQLdb.Error as e:
		print ("Mysql Error %d: %s" % (e.args[0], e.args[1]))
		return -1
	finally:
		cursor.close()	
		conn.close()	

def printAll(results=None):
	if results is not None:
		for row in results:
			id = row[0]
			name = row[1]
			print ("id=%s,name=%s," % (id, name))
	return None	

def batchInsert(table):
	items = []
	for x in range(1,20000):
		items.append([str(x),'Iter笔记'+str(x)])
	items = tuple(items)
	#print (items)	
	flag = insertData(table,items)
	if flag == 1:
		print ("批量添加数据成功，总共插入："
			+ str(getCount(table)))
	else:
		print ("批量添加数据失败")

def batchUpd(table):
	items = (['Iter笔记11','1'],['Iter笔记55','5',])
	flag = updateData(table,items)
	if flag == 1:
		print ("批量修改数据成功")
	else:
		print ("批量修改数据失败")

if __name__ == '__main__':
	#connDB()
	table = 'user'
	#print (getCount(table,'ff'))
	#print (select())
	print (select(table,'ff'))

	#printAll(select(table))

	#batchInsert(table)
	#batchUpd(table)
	
	#print (deleteData(table,['2']))
	
	#print (unionSelect('100'))
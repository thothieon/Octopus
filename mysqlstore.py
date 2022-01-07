# coding=utf-8

import os, datetime
import pprint

import pymysql

post = {
    "author": "Maxsu",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.utcnow()
}

#https://www.learncodewithmike.com/2020/02/python-mysql.html


# 資料庫參數設定
db_iDivingSettings = {
    "host": "192.168.12.57",
    "port": 3306,
    "user": "admin",
    "password": "admin220",
    "db": "iDiving",
    "charset": "utf8"
}

class MysqlStore():
    def __init__(self, diving_center):
        print("MysqlStore__init__")
        if diving_center == 'idiving':
            self.today = datetime.datetime.now()
            print("MysqlStore__init__self.today", self.today)
            # 建立Connection物件
            self.conn = pymysql.connect(**db_iDivingSettings)
            print("MysqlStore__init__self.conn", self.conn)

    def mysqltest(self, diving_center):
        print("mysqltestinit")
        # 建立Connection物件
        conn = pymysql.connect(**db_iDivingSettings)
        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料指令
            command = "SELECT 姓名, 身分證字號, 出生日期, 會員期限 FROM `人員名冊` WHERE (身分 = '學員' OR 身分 = '俱') and (會員期限 >= CURDATE() and 會員期限 != '' ) and (MONTH(出生日期)>4 and MONTH(出生日期)<6);"
            # 執行指令
            cursor.execute(command)
            # 取得所有資料
            result = cursor.fetchall()
            # 取得第一筆資料
            #result = cursor.fetchone()
            print(" ")
            print("Read",cursor.rowcount,"row(s) of data.")
            print(" ")
            print(result)
            print(" ")
    
        msg = '\n'
        msg += u'月份 當月會員生日名單\n'
        msg += u'姓名, 身分證字號, 出生日期, 會員期限\n'
        for row in result:
            print(row[0] + ', ' + row[1] + ', ' + str(row[2]) + ', ' + str(row[3]))
            msg += row[0] + ', ' + row[1] + ', ' + str(row[2]) + ', ' + str(row[3]) + '\n'
    
        print(msg)
        return msg

# coding=utf-8

import os
import datetime
import pprint

import pymysql
import pandas as pd

post = {
    "author": "Maxsu",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.utcnow()
}

# https://www.learncodewithmike.com/2020/02/python-mysql.html


# 資料庫參數設定
db_iDivingSettings57 = {
    "host": "192.168.12.57",
    "port": 3306,
    "user": "admin",
    "password": "admin220",
    "db": "iDiving",
    "charset": "utf8"
}

db_iDivingSettings249 = {
    "host": "192.168.12.249",
    "port": 3306,
    "user": "admin",
    "password": "admin220",
    "db": "iDiving",
    "charset": "utf8"
}

# home資料庫參數設定
db_homeSettings157 = {
    "host": "192.168.5.157",
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
            self.conn = pymysql.connect(**db_iDivingSettings57)
            print("MysqlStore__init__self.conn", self.conn)

    def mysqltest():
        print("mysqltestinit")
        # 建立Connection物件
        conn = pymysql.connect(**db_iDivingSettings57)
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
            print("Read", cursor.rowcount, "row(s) of data.")
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

    def CourseStatisticsQuery(command):
        print("mysqltestinit")
        # 建立Connection物件
        conn = pymysql.connect(**db_iDivingSettings57)
        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料指令
            #command = "SELECT * FROM `TransactionRecord` WHERE (課程選擇 LIKE '%自由潛水%' OR 課程選擇 LIKE '%FD%' OR 課程選擇 LIKE '%LV1%');"
            # 執行指令
            cursor.execute(command)
            # 取得所有資料
            result = cursor.fetchall()
            # 取得第一筆資料
            #result = cursor.fetchone()
            print(" ")
            print("Read", cursor.rowcount, "row(s) of data.")
            print(" ")
            print(result)
            print(" ")

        return cursor.rowcount

    def TransactionRecordQuery(name, tradingdata):
        print("TransactionRecordQuery")
        # 建立Connection物件
        conn = pymysql.connect(**db_iDivingSettings57)
        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料指令
            command = "SELECT * FROM TransactionRecord WHERE 中文姓名 = '" + \
                str(name) + "' AND 繳費紀錄 = '" + str(tradingdata) + "';"
            # 執行指令
            cursor.execute(command)
            # 取得所有資料
            result = cursor.fetchall()
            # 取得第一筆資料
            #result = cursor.fetchone()
            if cursor.rowcount != 0:
                print(" ")
                print("Read", cursor.rowcount, "row(s) of data.")
                print(" ")
                print(result)
                print(" ")
                return str(cursor.rowcount)
            elif cursor.rowcount == 0:
                print("Read", cursor.rowcount, "row(s) of data.")
                return 'norepeat'
        print("Finished")

    def TransactionRecordUpdata():
        print("TransactionRecordUpdata")

        print("Finished")

    def TransactionRecorAdd(dfmembers, intno, state):
        print("TransactionRecordAdd")
        # 建立Connection物件
        conn = pymysql.connect(**db_iDivingSettings57)
        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料指令
            command = "INSERT INTO TransactionRecord(時間戳記, 課程選擇, 中文姓名, 身分證字號, 手機號碼, EMail, 繳費紀錄, 狀態)VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (dfmembers.iat[intno, 0], dfmembers.iat[intno, 1], dfmembers.iat[intno, 2], dfmembers.iat[intno,
                    3], dfmembers.iat[intno, 20], dfmembers.iat[intno, 25], dfmembers.iat[intno, 4], str(state))
            # 執行指令
            cursor.execute(command, val)
            conn.commit()

        print("Finished")

    def BasicPersonalDataQuery(name, idnumber):
        print("BasicPersonalDataQuery")
        # 建立Connection物件
        conn = pymysql.connect(**db_iDivingSettings57)
        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料指令
            command = "SELECT * FROM BasicPersonalData WHERE 姓名 = '" + \
                str(name) + "' AND 身分證字號 = '" + str(idnumber) + "';"
            # 執行指令
            cursor.execute(command)
            # 取得所有資料
            result = cursor.fetchall()
            # 取得第一筆資料
            #result = cursor.fetchone()
            if cursor.rowcount != 0:
                print(" ")
                print("Read", cursor.rowcount, "row(s) of data.")
                print(" ")
                print(result)
                print(" ")
                return str(cursor.rowcount)
            elif cursor.rowcount == 0:
                print("Read", cursor.rowcount, "row(s) of data.")
                return 'nodata'
        print("Finished")

    def BasicPersonalDataAdd(dfmembers, intno, state):
        print("BasicPersonalDataAdd_init")

        datetime_dt = datetime.datetime.now()
        toyear = datetime_dt.strftime("%Y")
        print("BasicPersonalDataAdd_datetime ", datetime_dt.strftime("%Y%m%d%H%M%S"))
        # 建立Connection物件
        conn = pymysql.connect(**db_iDivingSettings57)
        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料指令
            command = "INSERT INTO BasicPersonalData(年份, 姓名, 行動電話, 身分證字號, 備註, 公司, 職稱, 公司電話, 來源, 住家電話, 暱稱, 郵遞區號, 地址, 緊急連絡人, 連絡人電話, 出生日期, 英文姓名, 國籍, EMail, MID, 繳費日期, 會員期限, 血型, 左眼, 右眼, 身高, 體重)VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (toyear,  # 年份
                    dfmembers.iat[intno, 2],  # 姓名
                    dfmembers.iat[intno, 20].replace('-', ''),  # 行動電話
                    dfmembers.iat[intno, 3],  # 身分證字號
                    dfmembers.iat[intno, 76],  # 備註
                    '',  # 公司
                    '',  # 職稱
                    dfmembers.iat[intno, 24],  # 公司電話
                    dfmembers.iat[intno, 48],  # 來源
                    '',  # 住家電話
                    '',  # 暱稱
                    '',  # 郵遞區號
                    dfmembers.iat[intno, 27],  # 地址
                    dfmembers.iat[intno, 35],  # 緊急連絡人
                    dfmembers.iat[intno, 36],  # 連絡人電話
                    dfmembers.iat[intno, 21],  # 出生日期
                    dfmembers.iat[intno, 22],  # 英文姓名
                    dfmembers.iat[intno, 23],  # 國籍
                    dfmembers.iat[intno, 24],  # EMail
                    '',  # MID
                    '',  # 繳費日期
                    '',  # 會員期限
                    dfmembers.iat[intno, 37],  # 血型
                    dfmembers.iat[intno, 32],  # 左眼
                    dfmembers.iat[intno, 31],  # 右眼
                    dfmembers.iat[intno, 28],  # 身高
                    dfmembers.iat[intno, 29]  # 體重
                    )

            # 執行指令
            cursor.execute(command, val)
            conn.commit()

        print("Finished")

# 年份,
# 姓名,
# 行動電話,
#身分證字號, dfmembers.iat[intno, 3]
#備註, dfmembers.iat[intno, 76]
#公司, ''
#職稱, ''
#公司電話, dfmembers.iat[intno, 24]
#來源, dfmembers.iat[intno, 48]
#住家電話, ''
# 暱稱,
#郵遞區號, ''
#地址, dfmembers.iat[intno, 27]
#緊急聯絡人, dfmembers.iat[intno, 35]
#聯絡人電話, dfmembers.iat[intno, 36]
#出生日期, dfmembers.iat[intno, 21]
#英文姓名, dfmembers.iat[intno, 22]
#國籍, dfmembers.iat[intno, 23]
#EMail, dfmembers.iat[intno, 24]
#MID, ''
#繳費日期, ''
# 會員期限,''
#血型, dfmembers.iat[intno, 37]
#左眼, dfmembers.iat[intno, 32]
#右眼, dfmembers.iat[intno, 31]
#身高, dfmembers.iat[intno, 28]
#體重 dfmembers.iat[intno, 29]


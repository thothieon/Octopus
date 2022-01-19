# coding=utf-8

import os
import sys
import codecs
import pickle

from pyasn1.type.univ import Null

from googleSheet import GoogleSheet
from mongodbstore import MongodbStore
from mysqlstore import MysqlStore
from linenotifyapi import LineNotifyAPI

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# py3importor_co.py -> py3octopus.py

diving_center = 'idiving'
#google_sheet_doc_key = '199CaQ4LvE0iPr-XtkhtsLCLob1cSQhTNvNo1E4iyDdM'
# test
google_sheet_doc_key_test = '18oBoHh4YjPcPHLn5m59r4v6_QI3CpgYqgD4rzLdS8Ds'
# 01 個人資料 Member
google_sheet_doc_key = '1ZdqwqFj9gUKzCbA4NQ2SATYCaxV4OL017tMhFUJBMoA'
# 04 課程報名表
google_sheet_doc_key_04 = '1sS9nUtXOg7JLSTVJVIQwXNYbNlbaxAu9b0Z_aDdVN-4'
# 自由潛水活動/補結訓/團練 報名表單
google_sheet_doc_key_04FD = '1-k6SJjhLGfda9xPp_bnsYMmLheQn-JpK4hlZs_Wj3T8'
# 06 出團報名表
google_sheet_doc_key_06 = '1XLkvfo8UR_JDv7ZZYgbUHoUTdnnhEUsY8x6WEZ79mvA'
# 21_年度價格表 Price List
# 21_google_sheet_doc_key = '1ZdqwqFj9gUKzCbA4NQ2SATYCaxV4OL017tMhFUJBMoA'
members_file = 'members.pickle'


def addMemberToFirestore():
    print("addMemberToFirestore_Init")


def addCourseToFirestore():
    print("addCourseToFirestore_Init")


def GoogleSheetparse04():
    print("GoogleSheetparse04_Init")
    # parse member from google sheet
    googleSheet = GoogleSheet(diving_center)
    name = "04A"
    members = googleSheet.parse04course(doc_key=google_sheet_doc_key_04, name=name, sheet=0)
    #print("GoogleSheetparse04_members", members.df.loc())
    print("GoogleSheetparse04_End")


def GoogleSheetSaveXlsx():
    print("testsqlpandas_Init")
    # parse member from google sheet
    googleSheet = GoogleSheet(diving_center)
    #scope = ['https://www.googleapis.com/auth/spreadsheets']
    #
    #creds = ServiceAccountCredentials.from_service_account_file("gs_credentials.json", scopes=scope)
    #gs = gspread.authorize(creds)
    #
    # sheet = gs.open_by_url('https://docs.google.com/spreadsheets/d/1ZdqwqFj9gUKzCbA4NQ2SATYCaxV4OL017tMhFUJBMoA/edit#gid=0')
    #worksheet = sheet.get_worksheet(0)
    name = "06A"
    members = googleSheet.parseSaveXlsx(doc_key=google_sheet_doc_key_06, name=name, sheet=6)


def ThisMonthNumberOfPeopleRegistered():
    print("ThisMonthNumberOfPeopleRegistered_Init")

    mysqlDataMsg = MysqlStore.mysqltest()
    print("ThisMonthNumberOfPeopleRegistered_mysqlData", mysqlDataMsg)

    LineNotifyAPI.lineNotifyMessageTest(mysqlDataMsg)
    print("ThisMonthNumberOfPeopleRegistered_linenotifyapi")


def DailyDataCollection():
    print("DailyDataCollection_Init")
    # 1 每天一次，確認表單當天有無新交易紀錄
    # 2 查詢mysql有無這筆紀錄
    # 3 有的話新增到mysql裡面，通知我有資料新增並註記這筆異常  沒有的話新增到mysql裡面通知我有資料新增
    # parse member from google sheet
    googleSheet = GoogleSheet(diving_center)
    name = "04A"
    # tradingdata=Null
    dfmembers = googleSheet.parse04CourseDayTrading(doc_key=google_sheet_doc_key_04, name=name, sheet=0, tradingdata=Null)
    print("GoogleSheetparse04_members", dfmembers)
    print("GoogleSheetparse04_members_no", len(dfmembers.index))
    for colno in range(len(dfmembers.index)):
        mysqlTradeMsg = MysqlStore.TransactionRecordQuery(
            dfmembers.iat[colno, 2], dfmembers.iat[colno, 4])
        mysqlBasicpersonalMsg = MysqlStore.BasicPersonalDataQuery(
            dfmembers.iat[colno, 2], dfmembers.iat[colno, 3])
        if mysqlTradeMsg == 'norepeat':
            print("GoogleSheetparse04_norepeat")
            MysqlStore.TransactionRecorAdd(
                dfmembers=dfmembers, intno=colno, state="")
            if mysqlBasicpersonalMsg == 'nodata':
                MysqlStore.BasicPersonalDataAdd(
                    dfmembers=dfmembers, intno=colno, state="")
        else:
            print("GoogleSheetparse04_count")
            MysqlStore.TransactionRecorAdd(
                dfmembers=dfmembers, intno=colno, state="repeat")

        TradeMsg = mysqlTradeMsg
        colno = colno + 1

    if len(dfmembers.index) == 0:
        LineNotifyAPI.lineNotifyMessageDaily('無資料新增')
    elif len(dfmembers.index) > 0 and TradeMsg == 'norepeat':
        print("GoogleSheetparse04_norepeat")
        LineNotifyAPI.lineNotifyMessageDaily('有資料新增')
    else:
        print("GoogleSheetparse04_count")
        LineNotifyAPI.lineNotifyMessageDaily('有資料 異常 新增，需整理TransactionRecor表單')

    print("GoogleSheetparse04_End")


def BirthdayMaturity():
    print("BirthdayMaturity_Init")


def MemberMaturity():
    print("MemberMaturity_Init")

def SendTest():
    LineNotifyAPI.lineNotifyMessageDaily('傳送測試訊息')


def addMemberSaveCSV():
    print("addMemberSaveCSV_Init")
    # parse member from google sheet
    googleSheet = GoogleSheet(diving_center)

    # 檢查檔案是否存在
    if not os.path.exists(members_file):
        print('start to parse google sheet')
        log_file = codecs.open('parse_failed.log', 'w', encoding='utf-8')
        print('log_file is', log_file)
        # 3 4504
        # test MAX 72
        #members = googleSheet.parseMember(start_row=3, end_row=52, doc_key=google_sheet_doc_key, log_file=log_file, sheet=0)
        members = googleSheet.parseSaveCSV(start_row=3, end_row=4510, doc_key=google_sheet_doc_key, log_file=log_file, sheet=0)
    else:
        print('found old data, use old data')
        with open(members_file, 'rb') as f:
            members = pickle.load(f)

    #mongodbstore = MongodbStore(diving_center)
    # mongodbstore.addMembers(members)
    print("addMemberSaveCSV_END")


def addMemberToMongoDB():
    print("addMemberToMongoDB_Init")
    # parse member from google sheet
    googleSheet = GoogleSheet(diving_center)

    # 檢查檔案是否存在
    if not os.path.exists(members_file):
        print('start to parse google sheet')
        log_file = codecs.open('parse_failed.log', 'w', encoding='utf-8')
        print('log_file is', log_file)
        # 3 4504
        # test MAX 72
        members = googleSheet.parseMember(start_row=2, end_row=4510, doc_key=google_sheet_doc_key, log_file=log_file, sheet=0)
    else:
        print('found old data, use old data')
        with open(members_file, 'rb') as f:
            members = pickle.load(f)

    mongodbstore = MongodbStore(diving_center)
    mongodbstore.addMembers(members)
    print("addMemberToMongoDB_END")

# commodity


def addCommodityToMongoDB():
    print("addCommodityToMongoDB_Init")


def MongoDBTest():
    mongodbstore = MongodbStore(diving_center)
    mongodbstore.addone()


def main1():
    print("main1")
    DailyDataCollection()


def main(argv):
    print("main")

    if argv[1] == '-Da':
        addMemberToMongoDB()
    elif argv[1] == '-Sc':
        addMemberSaveCSV()
    elif argv[1] == '-Ddc':
        DailyDataCollection()
    elif argv[1] == '-Tt':
        SendTest()
    else:
        DailyDataCollection()
        # ThisMonthNumberOfPeopleRegistered()
        # GoogleSheetparse04()
        # addMemberSaveCSV()
        # addMemberToMongoDB()
        # MongoDBTest()


if __name__ == '__main__':
    main(sys.argv)
    #main1()

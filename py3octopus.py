# coding=utf-8

import os, sys
import codecs
import pickle

from googleSheet import GoogleSheet
from mongodbstore import MongodbStore
from mysqlstore import MysqlStore
from linenotifyapi import LineNotifyAPI

import gspread
from oauth2client.service_account import ServiceAccountCredentials

#py3importor_co.py -> py3octopus.py

diving_center = 'idiving'
#google_sheet_doc_key = '199CaQ4LvE0iPr-XtkhtsLCLob1cSQhTNvNo1E4iyDdM'
#test
google_sheet_doc_key_test = '18oBoHh4YjPcPHLn5m59r4v6_QI3CpgYqgD4rzLdS8Ds'
#01 個人資料 Member
google_sheet_doc_key = '1ZdqwqFj9gUKzCbA4NQ2SATYCaxV4OL017tMhFUJBMoA'
#04 課程報名表
google_sheet_doc_key_04 = '1sS9nUtXOg7JLSTVJVIQwXNYbNlbaxAu9b0Z_aDdVN-4'
#06 出團報名表
google_sheet_doc_key_06 = '1XLkvfo8UR_JDv7ZZYgbUHoUTdnnhEUsY8x6WEZ79mvA'
#21_年度價格表 Price List
#21_google_sheet_doc_key = '1ZdqwqFj9gUKzCbA4NQ2SATYCaxV4OL017tMhFUJBMoA'
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
    #sheet = gs.open_by_url('https://docs.google.com/spreadsheets/d/1ZdqwqFj9gUKzCbA4NQ2SATYCaxV4OL017tMhFUJBMoA/edit#gid=0')
    #worksheet = sheet.get_worksheet(0)
    name = "06A"
    members = googleSheet.parseSaveXlsx(doc_key=google_sheet_doc_key_06, name=name, sheet=6)

def ThisMonthNumberOfPeopleRegistered():
    print("ThisMonthNumberOfPeopleRegistered_Init")
    mysqlStore = MysqlStore(diving_center)
    mysqlData = mysqlStore.mysqltest(diving_center)
    print("ThisMonthNumberOfPeopleRegistered_mysqlData", mysqlData)
    LineNotifyAPI.lineNotifyMessageTest(mysqlData)
    print("ThisMonthNumberOfPeopleRegistered_linenotifyapi")

def BirthdayMaturity():
    print("BirthdayMaturity_Init")

def MemberMaturity():
    print("MemberMaturity_Init")


def addMemberSaveCSV():
    print("addMemberSaveCSV_Init")
    # parse member from google sheet
    googleSheet = GoogleSheet(diving_center)
    
    #檢查檔案是否存在
    if not os.path.exists(members_file):
        print('start to parse google sheet')
        log_file = codecs.open('parse_failed.log', 'w', encoding='utf-8')
        print('log_file is', log_file)
        #3 4504
        #test MAX 72
        #members = googleSheet.parseMember(start_row=3, end_row=52, doc_key=google_sheet_doc_key, log_file=log_file, sheet=0)
        members = googleSheet.parseSaveCSV(start_row=3, end_row=4510, doc_key=google_sheet_doc_key, log_file=log_file, sheet=0)
    else:
        print('found old data, use old data')
        with open(members_file, 'rb') as f:
            members = pickle.load(f)
    
    #mongodbstore = MongodbStore(diving_center)
    #mongodbstore.addMembers(members)
    print("addMemberSaveCSV_END")

def addMemberToMongoDB():
    print("addMemberToMongoDB_Init")
    # parse member from google sheet
    googleSheet = GoogleSheet(diving_center)
    
    #檢查檔案是否存在
    if not os.path.exists(members_file):
        print('start to parse google sheet')
        log_file = codecs.open('parse_failed.log', 'w', encoding='utf-8')
        print('log_file is', log_file)
        #3 4504
        #test MAX 72
        members = googleSheet.parseMember(start_row=2, end_row=4510, doc_key=google_sheet_doc_key, log_file=log_file, sheet=0)
    else:
        print('found old data, use old data')
        with open(members_file, 'rb') as f:
            members = pickle.load(f)
    
    mongodbstore = MongodbStore(diving_center)
    mongodbstore.addMembers(members)
    print("addMemberToMongoDB_END")

#commodity
def addCommodityToMongoDB():
    print("addCommodityToMongoDB_Init")

def MongoDBTest():
    mongodbstore = MongodbStore(diving_center)
    mongodbstore.addone()

def main(argv):
    print("main")
    ThisMonthNumberOfPeopleRegistered()
    
    #GoogleSheetparse04()
    
    #addMemberSaveCSV()
    #addMemberToMongoDB()
    #MongoDBTest()
    #if argv[1] == '-Da':
    #    addMemberToMongoDB()
    #elif argv[1] == '-Sc':
    #    addMemberSaveCSV()

if __name__ == '__main__':
    main(sys.argv)



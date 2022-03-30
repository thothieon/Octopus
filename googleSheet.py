# coding=utf-8

import os
import csv
import copy
import json
import time
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pyasn1.type.univ import Null
from processMember import ProcessMember
from dotty_dict import dotty
import pandas as pd

# 參考 Google Sheet
# https://yanwei-liu.medium.com/%E5%A6%82%E4%BD%95%E9%80%8F%E9%81%8Epython%E5%BB%BA%E7%AB%8Bgoogle%E8%A1%A8%E5%96%AE-%E4%BD%BF%E7%94%A8google-sheet-api-314927f7a601
# 參考 Save CSV
# https://ithelp.ithome.com.tw/articles/10231217
# 參考 Save excel
# https://officeguide.cc/python-openpyxl-read-write-excel-file-tutorial-examples/


class GoogleSheet():
    def __init__(self, diving_center):
        print("GoogleSheet_init_")
        scriptdir = os.path.dirname(os.path.abspath(__file__))
        cred_file = os.path.join(scriptdir, 'credential', diving_center, 'gcp_service_account.json')
        #cred_file = os.path.join(os.getcwd(), 'credential', diving_center, 'gcp_service_account.json')
        print("GoogleSheet_init_cred_file->", cred_file)
        scopes = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

        credential = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scopes)
        self.google_cred = gspread.authorize(credential)
        self.diving_center = diving_center

    def parseMember(self, start_row, end_row, doc_key, log_file, sheet):
        # print("GoogleSheet_parseMember")
        members = []
        processMember = ProcessMember(self.diving_center)

        with open(os.path.join(os.getcwd(), 'keyMapping', self.diving_center, 'member_basic.json')) as f:
            basic_dict = dotty(json.load(f))

        with open(os.path.join(os.getcwd(), 'keyMapping', self.diving_center, 'member.json')) as f:
            mapping_dict = json.load(f)

        sheets = self.google_cred.open_by_key(doc_key)
        worksheet = sheets.get_worksheet(sheet)
        #worksheet = sheets.sheet1
        worksheetcol = worksheet.get_all_values()
        print("GoogleSheet_postscolname worksheetcol no  ", len(worksheetcol))

        row = start_row
        #print("GoogleSheet_parseMember_row", row)
        #print("GoogleSheet_parseMember_mapping_dict.items()", mapping_dict.items())
        while row <= end_row:
            if row % 200 == 0:
                print('Now process > %s row' % row)

            currentCell = ''
            keyIdx = 0
            try:
                # 取一列
                #values = worksheet.row_values(row)
                values = worksheetcol[row]
                for key, notation in mapping_dict.items():
                    if (notation):
                        currentCell = key
                        #print('Now process try (notation)-> %s: currentCell-> %s: key-> %s' % (notation, currentCell, key))
                        # 抓欄位名稱
                        basic_dict[notation] = processMember.processCell(
                            notation, values[keyIdx])
                    keyIdx = keyIdx + 1

                member_info = processMember.postProcess(
                    copy.deepcopy(basic_dict.to_dict()))
                members.append(member_info)
                #print('Now process try ')
                row = row + 1
            except gspread.exceptions.APIError as e:
                e = json.loads(e.args[0])
                print('Now process except Exception Error ',e['error']['code'])
                if e['error']['code'] == 401:
                    print('Auth timeout, re-login')
                    gss_client.login()
                elif e['error']['code'] == 429:
                    print('Exceed the limitation on row %s, sleep 10 seconds (%s)' % (
                        row, datetime.datetime.now()))
                    time.sleep(10)
                else:
                    print(e)
            except Exception as e:
                print(
                    'Now process except Exception Error [%s:%s] - %s' % (row, currentCell, e))
                log_file.write('Error [%s:%s] - %s\n' % (row, currentCell, e))
                row = row + 1

        print('total member count: %s' % len(members))
        return members

    def parse04course(self, doc_key, name, sheet):
        print("GoogleSheet_parse04course")

        # 參考
        # https://www.learncodewithmike.com/2021/04/pandas-data-filtering.html

        sheets = self.google_cred.open_by_key(doc_key)
        worksheet = sheets.get_worksheet(sheet)
        worksheetname = worksheet.title
        worksheetcol = worksheet.get_all_values()
        filt_value = ['匯款']  # 想要的值
        self.df = pd.DataFrame(worksheetcol)
        # print(df)
        # filt = df[4].isin(filt_value)  #篩選Job欄位有filt_value串列中的資料
        # 分析欄位[0] 登入年分
        # 分析欄位[4]] 繳費月份 & (關鍵字 定金 全額)
        # 分析欄位[5]] 繳費月份 & (關鍵字 定金 全額)
        # 年份
        yearvalue = "2022"
        # 月份
        monthvalue = "01/"
        filt = self.df[0].str.contains(yearvalue, na=False) & ((self.df[4].str.contains(monthvalue) & (self.df[4].str.contains('定金', na=False) | self.df[4].str.contains(
            '全額', na=False))) | (self.df[5].str.contains(monthvalue) & (self.df[5].str.contains('定金', na=False) | self.df[5].str.contains('全額', na=False))))
        print(self.df.loc[filt, [0, 1, 4, 5, 6]])
        sdff = self.df.loc[filt, [0, 1, 4, 5, 6]]
        print("Finished")
        return sdff

    def parse04CourseDayTrading(self, doc_key, name, sheet, tradingdata):
        print("GoogleSheet_parse04CourseDayTrading")

        # 參考
        # https://www.learncodewithmike.com/2021/04/pandas-data-filtering.html

        datetime_dt = datetime.datetime.today()
        print("GoogleSheet_parse04CourseDayTrading_datetime ", datetime_dt.strftime("%Y%m%d%H%M%S"))
        yearno = datetime_dt.strftime("%m")
        print("GoogleSheet_parse04CourseDayTrading_year ", yearno)
        moonno = datetime_dt.strftime("%m")
        print("GoogleSheet_parse04CourseDayTrading_moon ", moonno)
        dayno = datetime_dt.strftime("%d")
        print("GoogleSheet_parse04CourseDayTrading_day ", dayno)

        sheets = self.google_cred.open_by_key(doc_key)
        worksheet = sheets.get_worksheet(sheet)
        worksheetcol = worksheet.get_all_values()

        self.df = pd.DataFrame(worksheetcol)
        # print(df)
        # filt = df[4].isin(filt_value)  #篩選Job欄位有filt_value串列中的資料
        # 分析欄位[0] 登入年分
        # 分析欄位[4]] 繳費月份 & (關鍵字 定金 全額)
        # 分析欄位[5]] 繳費月份 & (關鍵字 定金 全額)
        # 年份
        yearvalue = "2022"
        # 繳費日期
        if tradingdata == Null:
            tradingdata = str(moonno) + "/" + str(dayno)

        print("GoogleSheet_parse04CourseDayTrading_tradingdata ", tradingdata)
        filt = self.df[0].str.contains(yearvalue, na=False) & ((self.df[4].str.contains(tradingdata) & (self.df[4].str.contains('訂金', na=False) | self.df[4].str.contains('定金', na=False) | self.df[4].str.contains(
            '全額', na=False))) | (self.df[5].str.contains(tradingdata) & (self.df[5].str.contains('訂金', na=False) | self.df[5].str.contains('定金', na=False) | self.df[5].str.contains('全額', na=False))))
        #print(self.df.loc[filt, [0, 1, 4, 5, 6]])
        #sdff = self.df.loc[filt, [0, 1, 4, 5, 6]]
        print(self.df.loc[filt])
        sdff = self.df.loc[filt]
        print("Finished")
        return sdff

    def parse04coursesearchpaid(self, doc_key, name, sheet):
        print("GoogleSheet_parse04coursesearchpaid")

        # 參考
        # https://www.learncodewithmike.com/2021/04/pandas-data-filtering.html

        sheets = self.google_cred.open_by_key(doc_key)
        worksheet = sheets.get_worksheet(sheet)
        worksheetcol = worksheet.get_all_values()

        self.df = pd.DataFrame(worksheetcol)
        # print(df)
        # filt = df[4].isin(filt_value)  #篩選Job欄位有filt_value串列中的資料
        # 分析欄位[0] 登入年分
        # 分析欄位[4]] 繳費月份 & (關鍵字 定金 全額)
        # 分析欄位[5]] 繳費月份 & (關鍵字 定金 全額)
        # 年份
        yearvalue = "2022"
        # 月份
        monthvalue = "1/"
        filt = self.df[0].str.contains(yearvalue, na=False) & ((df[4].str.contains(monthvalue) & (df[4].str.contains('定金', na=False) | df[4].str.contains(
            '全額', na=False))) | (df[5].str.contains(monthvalue) & (df[5].str.contains('定金', na=False) | df[5].str.contains('全額', na=False))))
        print(self.df.loc[filt, [0, 1, 4, 5, 6]])

        print("Finished")

    def parseSaveCSV(self, start_row, end_row, doc_key, log_file, sheet):
        print("GoogleSheet_parseSaveCSV")
        datetime_dt = datetime.datetime.today()
        print("GoogleSheet_datetime ", datetime_dt.strftime("%Y%m%d%H%M%S"))
        postscolname = "postscol_" + \
            datetime_dt.strftime("%Y%m%d%H%M%S") + ".csv"
        print("GoogleSheet_postscolname ", postscolname)

        sheets = self.google_cred.open_by_key(doc_key)
        worksheet = sheets.get_worksheet(sheet)
        worksheetcol = worksheet.get_all_values()

        print("GoogleSheet_postscolname worksheetcol no  ", len(worksheetcol))
        totalrow = len(worksheetcol)
        row = 0

        with open(postscolname, mode='w') as employee_file:
            employee_writer = csv.writer(
                employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, index=False, encoding='utf-8')

            #employee_writer.writerow(['John Smith', 'Accounting', 'November'])
            #employee_writer.writerow(['Erica Meyers', 'IT', 'March'])
            #values = worksheetcol[row]
            for row in range(totalrow):
                employee_writer.writerow(worksheetcol[row])
                row = row + 1

            #keyIdx = 0
            # for key, notation in mapping_dict.items():

        employee_file.close()

        print("Finished")

    def parseSaveXlsx(self, doc_key, name, sheet):
        print("GoogleSheet_parseSaveXlsx")

        # Generate file name
        datetime_dt = datetime.datetime.today()
        print("GoogleSheet_datetime ", datetime_dt.strftime("%Y%m%d%H%M%S"))
        #postscolname = "postscol_" + name + "_" + str(sheet) + "_" + datetime_dt.strftime("%Y%m%d%H%M%S") + ".csv"
        postscolnamexlsx = "postscol_" + name + "_" + \
            datetime_dt.strftime("%Y%m%d%H%M%S") + ".xlsx"
        #postscolname = "postscol_" + "_" + str(sheet) + "_" + datetime_dt.strftime("%Y%m%d%H%M%S") + ".csv"
        #print("GoogleSheet_postscolname ", postscolname )

        writer = pd.ExcelWriter(postscolnamexlsx)

        sheets = self.google_cred.open_by_key(doc_key)
        i = 0
        for i in range(sheet):
            print(i)
            worksheet = sheets.get_worksheet(i)
            worksheetname = worksheet.title
            worksheetcol = worksheet.get_all_values()

            df = pd.DataFrame(worksheetcol)
            # print(df)
            #df.to_csv(postscolname, encoding="utf_8_sig")
            df.to_excel(writer, sheet_name=worksheetname,
                        index=False, encoding="utf_8_sig")

            i = i + 1

        writer.save()

        print("Finished")

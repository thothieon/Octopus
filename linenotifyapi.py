# coding=utf-8
import os, sys, datetime
import requests

#https://ithelp.ithome.com.tw/articles/10223413

msg = ''
#出團小幫手群組
tokenTest = 'FIGXSo5MEA1RJ23q7vLN5WuhkkYcdDp6JsjNmfyWvn7'
#iD. 櫃檯  出團小幫手 提醒
tokencounter = '0WMuxpiX6tYbAUkzYopqVz2Nq0APASHkrh2AWPAHU9b'
#iD. 教學  出團小幫手 提醒
tokencourse = 'zPvvFjzISmV2yv3xZ8j1B51l2uuFgwDspCevDmdVqEe'
#iD. 活動 / 俱樂部  出團小幫手 提醒
tokenactivity= 'WngiJSUOPfOi2xV1SNVkhlaQWtuyCu2bJgVUoxJtJs9'
#iD. 網路  出團小幫手 提醒
tokennetwork = 'Von2PNVHOxND2IWKrhbfb5KR0AJA9fa8EheD12AgiJ9'


class LineNotifyAPI():
    def lineNotifyMessage(token, msg):
        headers = {
            "Authorization": "Bearer " + token, 
            "Content-Type" : "application/x-www-form-urlencoded"
        }
        
        payload = {'message': msg}
        r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
        return r.status_code
    
    def lineNotifyMessageTest(msg):
        headers = {
            "Authorization": "Bearer " + tokenTest, 
            "Content-Type" : "application/x-www-form-urlencoded"
        }
        
        payload = {'message': msg}
        r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
        return r.status_code

# coding=utf-8
import os
import sys
import datetime

from pyshorteners import Shortener
import bitly_api
#

# https://www.geeksforgeeks.org/url-shorteners-and-its-api-in-python-set-1/

API_USER = "o_773c5s2str"
API_KEY = "fa63ebbe07d8bc1ccf26534bc0019ce629fd165c"
BITLY_ACCESS_TOKEN ="fa63ebbe07d8bc1ccf26534bc0019ce629fd165c"

long_url = 'http://www.google.com'
API_Key = 'fa63ebbe07d8bc1ccf26534bc0019ce629fd165c'

msg = ''

# 
tokenTest = 'FIGXSo5MEA1RJ23q7vLN5WuhkkYcdDp6JsjNmfyWvn7'

#短網址轉換
class URLShortener():
    def bitlychangurl():
        print("bitlychangurl_Init")
        b = bitly_api.Connection(access_token = BITLY_ACCESS_TOKEN)
        response = b.shorten('http://google.com/')
        print(response)
        #bitly = bitly_api.Connection(API_USER, API_KEY)
        #response = bitly.shorten('http://google.com/')
        #print(response)

        return 'ok'

    def googlechangurl():
        bitly = bitly_api.Connection(API_USER, API_KEY)
        response = bitly.shorten('http://google.com/')
        print(response)

        return 'ok'


# -*- coding: utf-8 -*-
import os
import codecs
# https://codertw.com/%E7%A8%8B%E5%BC%8F%E8%AA%9E%E8%A8%80/372308/
import pickle
# https://www.itread01.com/content/1541722469.html

from googleSheet import GoogleSheet
from mongodbstore import MongoDBStore

diving_center = 'idiving'
google_sheet_doc_key = '1ZdqwqFj9gUKzCbA4NQ2SATYCaxV4OL017tMhFUJBMoA'
mongo_url = 'mongodb://myUserAdmin:abc123@122.116.22.125:27018/admin'
mongodb_name = 'test'
collection_name = 'test_collection'
members_file = 'members.pickle'


def GetMongodb():
    mongodbstore = MongoDBStore(mongo_url, mongodb_name)
    #mongodbstore.addMembers('test_collection')

def GetMember():
    # parse member from google sheet
    googleSheet = GoogleSheet(diving_center)
    
    if not os.path.exists(members_file):
        print('GetMember() no file')
        log_file = codecs.open('parse_failed.log', 'w', encoding='utf-8')
        members = googleSheet.parseMember(start_row=3, end_row=5, doc_key=google_sheet_doc_key, log_file=log_file, sheet=0)
        
        with open(members_file, 'wb') as f:
            pickle.dump(members, f)
    else:
        print('GetMember() open file')
        with open(members_file, 'rb') as f:
            members = pickle.load(f)
    
    mongodbstore = MongoDBStore(mongo_url, mongodb_name)
    mongodbstore.addMembers(collection_name, members)

def main():
    #GetMongodb()
    GetMember()
    print("main() -> ", google_sheet_doc_key)

if __name__ == '__main__':
    main()

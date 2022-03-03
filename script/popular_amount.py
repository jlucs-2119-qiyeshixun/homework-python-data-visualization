import json
import os
from datetime import datetime

cwd = os.getcwd()

file_tag = cwd + '/data/popular_process_result/rcmd_tag_amount.json'
file_tid = cwd + '/data/popular_process_result/tid_rate_amount.json'

def get_rcmd_tag():
    fp = open(file_tag,'r',encoding='utf-8')
    tag_list = json.load(fp)
    fp.close()

    favorate = {
        "list":[],
        "time":[]
    }

    values = {
        "watch":{
            "list":[],
            "time":[]
        },
        "favorate":{
            "list":[],
            "time":[]
        },
        "shared":{
            "list":[],
            "time":[]
        },
        "popular":{
            "list":[],
            "time":[]
        },
        "other":{
            "list":[],
            "time":[]
        },
        "search":{
            "list":[],
            "time":[]
        },
        "notag":{
            "list":[],
            "time":[]
        }
    }

    list2 = [{
        "date":datetime.strptime(date,"%Y-%m-%d %H:%M:%S"),
        "item":item
    }for date,item in tag_list.items()]
    
    list2 = sorted(list2,key=lambda item : item['date'])
    date_list = []

    cnt = 0
    for elem in list2:
        tme = elem['date']
        item = elem['item']
        if tme.minute != 0:
            continue
        date_list.append(tme)
        for k in values:
            values[k]['list'].append(item[k]['rate'])
            values[k]['time'].append(f'{tme.day}日/{tme.hour}时')
    return values,date_list

def get_by_datetime(tme):
    fp = open(file_tag,'r',encoding='utf-8')
    tag_list = json.load(fp)
    fp.close()

    for date,item in tag_list.items():
        if datetime.strptime(date,"%Y-%m-%d %H:%M:%S") == tme:
            return item
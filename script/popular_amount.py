import json
import os
from datetime import datetime
import config

cwd = os.getcwd()

file_tag = cwd + '/data/popular_process_result/rcmd_tag_amount.json'
file_tid = cwd + '/data/popular_process_result/tid_rate_amount.json'

def get_tid_by_datetime(date):
    fp = open(file_tid,'r',encoding='utf-8')
    tid_list = json.load(fp)
    fp.close()

    for k,v in tid_list.items():
        if date == datetime.strptime(k,"%Y-%m-%d %H:%M:%S"):
            return v

    return 

def get_tid_list():
    fp = open(file_tid,'r',encoding='utf-8')
    tid_list = json.load(fp)
    fp.close()

    list2 = [{
        "date":datetime.strptime(date,"%Y-%m-%d %H:%M:%S"),
        "item":item
    }for date,item in tid_list.items()]
    list2 = sorted(list2,key=lambda item : item['date'])

    values = {}
    date_list = []

    for listitem in list2:
        date = listitem['date']
        item = listitem['item']
        if date.minute != 0:
            continue
        date_list.append(date)
        # print(date)
        for tag in item:
            tid = tag['tid']
            if tid not in values:
                values[tid] = {
                    "list":[],
                    "date":[]
                }
            values[tid]["list"].append(tag['count'])
            values[tid]["date"].append(f'{date.hour}时')
    
    values = {k:v for k,v in values.items() if len(v['list']) > 10}
    # for k,v in values.items():
    #     print(k,len(v["list"]),config.region_info[str(k)])
    return values,date_list

def get_rcmd_tag():
    fp = open(file_tag,'r',encoding='utf-8')
    tag_list = json.load(fp)
    fp.close()

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
            values[k]['time'].append(f'{tme.hour}时')
    return values,date_list

def get_rcmd_by_datetime(tme):
    fp = open(file_tag,'r',encoding='utf-8')
    tag_list = json.load(fp)
    fp.close()

    for date,item in tag_list.items():
        if datetime.strptime(date,"%Y-%m-%d %H:%M:%S") == tme:
            return item


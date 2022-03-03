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

    cnt = 0
    for date,item in tag_list.items():
        
        tme = datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
        if tme.minute != 0:
            continue

        for k in values:
            values[k]['list'].append(item[k]['rate'])
            values[k]['time'].append(f'{tme.day}d/{tme.hour}h')
    return values

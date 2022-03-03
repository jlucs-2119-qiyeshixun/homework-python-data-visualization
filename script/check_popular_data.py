from ast import parse
import os
import json
from unicodedata import name
import config


def parse_list(list) :
    tid_cnt = {}
    for item in list:
        if item['tid'] in tid_cnt:
            tid_cnt[item['tid']] += 1
        else:
            tid_cnt[item['tid']] = 1
    return tid_cnt


def get_tid_rage(file):
    fp = open(file,'r',encoding='utf-8')
    list = json.load(fp)
    fp.close()

    tid_cnt = parse_list(list)
    # print(tid_cnt)

    tid_cnt_parent = {}
    tot = 0

    for k,v in tid_cnt.items():
        parent = config.region_info[str(k)]
        if parent['parent'] not in tid_cnt_parent:
            tid_cnt_parent[parent['parent']] = {
                "name":parent['name'],
                "count":0
            }
        tid_cnt_parent[parent['parent']]['count'] += v
        tot += v

    return [
        {
            "tid":k,
            "name":v['name'],
            "count":v['count'],
            "rage":str(round(v['count'] / tot * 100,2)) + '%'
        }
        for k,v in tid_cnt_parent.items()
    ]


def process_tid_amount():
    dir = cwd + '/data/popular/'

    tid_rate_amount = {}
    for root,dirs,files in os.walk(dir):
        for file in files :
            li = get_tid_rage(dir + '/' + file)
            tid_rate_amount[file.split('.')[0]] = li

    dir = cwd + '/data/popular_process_result/tid_rate_amount.json'
    fp = open(dir,'w',encoding='utf-8')
    json.dump(tid_rate_amount,fp,ensure_ascii=False)
    print('done')


cwd = os.getcwd()

process_tid_amount()
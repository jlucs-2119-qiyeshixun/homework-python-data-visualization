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
            "rage":round(v['count'] / tot * 100,2)
        }
        for k,v in tid_cnt_parent.items()
    ]

# 处理tid数据
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
    print('process tid amount done')

def get_tag_list(file):
    fp = open(file,'r',encoding='utf-8')
    list = json.load(fp)
    fp.close()

    tag_lists = {
        "watch":[],
        "favorate":[],
        "shared":[],
        "popular":[],
        "other":[],
        "search":[],
        "notag":[]
    }

    for item in list:
        rcmd = item['rcmd_reason']
        element = {
            "aid":item['aid'],
            "title":item['title'],
            "rcmd_content":rcmd['content']
        }
        if rcmd['corner_mark'] == 1:
            if rcmd['content'].__contains__('播放'):
                tag_lists['watch'].append(element)
            elif rcmd['content'].__contains__('点赞'):
                tag_lists['favorate'].append(element)
            elif rcmd['content'].__contains__('分享'):
                tag_lists['shared'].append(element)
            elif rcmd['content'].__contains__('人气'):
                tag_lists['popular'].append(element)
            elif rcmd['content'].__contains__('搜'):
                tag_lists['search'].append(element)
            else:
                tag_lists['other'].append(element)
        else:
            tag_lists['notag'].append(element)

    return {
        k:{
            "list":v,
            "rate":round(len(v) / len(list) * 100)
        }for k,v in tag_lists.items()
    }

def process_tag_amount():
    rcmd_tag_amount = {}
    dir = cwd + '/data/popular/'
    for root,dirs,files in os.walk(dir):
        for file in files:
            rcmd_tag_amount[file.split('.')[0]] = get_tag_list(dir + '/' + file)

    dir = cwd + '/data/popular_process_result/rcmd_tag_amount.json'
    fp = open(dir,'w',encoding='utf-8')
    json.dump(rcmd_tag_amount,fp,ensure_ascii=False)
    print('process tag amount done')


cwd = os.getcwd()

process_tid_amount()
process_tag_amount()
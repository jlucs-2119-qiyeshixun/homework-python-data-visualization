import requests
import json
import os

cwd = os.getcwd()
time_from = "20220202"
time_to = "20220302"
# dm click stow coin
# 获取每个分区 在指定时间内 按照播放量排序的top(50) 视频信息

region_config = [
    {
        "name": "动画",
        "list": [24, 25, 47, 210, 86, 27]
    },
    {
        "name": "音乐",
        "list": [28, 31, 30, 194, 59, 193, 29, 130]
    },
    {
        "name": "游戏",
        "list": [17, 171, 172, 65, 173, 121, 136, 19]
    },
    {
        "name": "知识",
        "list": [201, 124, 228, 207, 208, 209, 229, 122]
    },
    {
        "name": "美食",
        "list": [76, 212, 213, 214, 215]
    },
    {
        "name": "资讯",
        "list": [203, 204, 205, 206]
    },
    {
        "name": "生活",
        "list": [138, 239, 161, 162, 21]
    }
]


def complete(bvid, tp):

    url = 'https://api.bilibili.com/x/web-interface/archive/stat'
    params = {
        "bvid": bvid
    }
    header = {
        "User-Agent": "Mozilla / 5.0(X11; Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 77.0.3865.120 Safari / 537.36"
    }
    resp = requests.request('GET', headers=header, url=url, params=params)
    text = json.loads(resp.text)
    if text["code"] != 0:
        return tp

    data = text["data"]
    tp["play"] = data["view"]
    tp["danmaku"] = data["danmaku"]
    tp["reply"] = data["reply"]
    tp["favorite"] = data["favorite"]
    tp["coin"] = data["coin"]
    tp["share"] = data["share"]
    tp["like"] = data["like"]
    return tp


def get_small_region_radios(rid, order):
    url = 'https://s.search.bilibili.com/cate/search'
    params = {
        "main_ver": "v3",
        "search_type": "video",
        "view_type": "hot_rank",
        "order": order,
        "copy_right": "-1",
        "cate_id": rid,
        "page": 1,
        "pagesize": 50,
        "jsonp": "jsonp",
        "time_from": time_from,
        "time_to": time_to
    }
    resp = requests.request('GET', url=url, params=params)
    print(json.loads(resp.text))
    list = json.loads(resp.text)["result"]
    data = []
    for x in list:
        tp = {
            "author": x["author"],
            "bvid": x["bvid"],
            "mid": x["mid"],
            "title": x["title"],
            "play": int(x["play"]),
            "url": "https://www.bilibili.com/video/" + x["bvid"]
        }
        # tp = complete(tp["bvid"], tp)
        print(tp)
        data.append(tp)
    return data


def get_region_radios():
    for tmp in region_config:
        list = tmp["list"]
        data = []
        for tid in list:
            data += get_small_region_radios(tid, "click")
        f = open(cwd + "/data/data_" + tmp["name"] + ".json", "w", encoding='utf-8')
        f.write(json.dumps(data, ensure_ascii=False))


get_region_radios()
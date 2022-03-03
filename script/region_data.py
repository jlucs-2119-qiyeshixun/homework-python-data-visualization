# 获取每个分区 在指定时间内 按照播放量排序的top(50) 视频信息

import time
import requests
import json
import sys
from tqdm import tqdm
import logging
from datetime import datetime
from config import region_config, region_info

def getTime():
    curr = datetime.now()
    return f'{curr.year}-{curr.month}-{curr.day} {curr.hour}:{curr.minute}'

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

time_from = "20220202"
time_to = "20220302"

def complete(bvid, tp):

    url = 'http://api.bilibili.com/x/web-interface/view'
    params = {
        "bvid": bvid
    }
    header = {
        "User-Agent": "Mozilla / 5.0(X11; Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 77.0.3865.120 Safari / 537.36"
    }
    resp = requests.request('GET', headers=header, url=url, params=params)
    text = json.loads(resp.text)
    if text["code"] != 0:
        if text["code"] == -412:
            while text["code"] == -412:
                time.sleep(5)
                resp = requests.request('GET', headers=header, url=url, params=params)
                text = json.loads(resp.text)
                print(text)
        else:
            return tp

    data = text["data"]["stat"]
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
    list = json.loads(resp.text)["result"]
    data = []

    pbar = tqdm(total=len(list))
    pbar.set_description(f"补全分区{rid}信息")
    for x in list:
        tp = {
            "author": x["author"],
            "bvid": x["bvid"],
            "mid": x["mid"],
            "title": x["title"],
            "play": int(x["play"]),
            "url": "https://www.bilibili.com/video/" + x["bvid"]
        }
        #tp = complete(tp["bvid"], tp)
        data.append(tp)
        pbar.update(1)
    pbar.close()
    return data


def get_region_radios():
    for tmp in region_config:
        list = tmp["list"]
        data = []
        name = tmp["name"]
        total = 0

        logging.info(f"{name}区分区如下: {list}")
        for tid in list:
            r_name = region_info[str(tid)]["name"]
            r_data = get_small_region_radios(tid, "click")
            data.append({
                "name": r_name,
                "list": r_data
            })
            logging.info(f"成功爬取{name}区_{r_name}分区数据共{len(r_data)}条")
            total += len(r_data)

        f = open(f"../data/region_data/{time_from}_{time_to}/data_{name}.json", "w", encoding='utf-8')
        ans = {
            "data": data,
            "total": total
        }
        f.write(json.dumps(ans, ensure_ascii=False))
        logging.info(f"--------------------------------{name}区全部爬取完毕，共{total}条数据-----------------------------")


get_region_radios()
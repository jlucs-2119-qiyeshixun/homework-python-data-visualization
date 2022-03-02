from nturl2path import url2pathname
import requests
import json
import os
from datetime import datetime


def getTime():
    curr = datetime.now()
    return f'{curr.year}-{curr.month}-{curr.day} {curr.hour}:{curr.minute}:{curr.second}'


cwd = os.getcwd()

url = 'https://api.bilibili.com/x/web-interface/popular'
params = {
    'ps' : 50,
    'pn' : 1
}
headers = {
    "User-Agent": "Mozilla / 5.0(X11; Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 77.0.3865.120 Safari / 537.36"
}

tot = 0
tot_li = []
while True:
    resp = requests.request("GET",url = url,params=params,headers = headers)
    resp = json.loads(resp.text)
    data = resp['data']
    li = data['list']
    no_more = data['no_more']
    # print(len(li))
    # print(no_more)
    tot += len(li)
    tot_li += li
    if no_more == False:
        params['pn'] += 1
    else:
        break

#print(json.dumps(tot_li,ensure_ascii=False))
f = open(cwd + f'/data/popular/{getTime()}.json','w',encoding='utf-8')
json.dump(tot_li,f,ensure_ascii=False)
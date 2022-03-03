import requests
from lxml import etree
import time
import random
import os
import pandas as pd

def get_target(keyword, page, saveName):
    result = pd.DataFrame()

    for i in range(1, page + 1):
        url = 'https://search.bilibili.com/all?keyword={}&from_source=nav_suggest_new0&page={}'.format(keyword, i)
        html = requests.get(url.format(i))
        bs = etree.HTML(html.text)
        items = bs.xpath('//li[@class = "video-item matrix"]')
        for item in items:
            video_url = item.xpath('div[@class = "info"]/div/a/@href')[0].replace("//","") #每个视频的来源地址
            bvid = video_url[video_url.find('BV'):video_url.find('?from')]
            #print(bvid)#每个视频bvid
            title = item.xpath('div[@class = "info"]/div/a/@title')[0]#每个视频的标题
            region = item.xpath('div[@class = "info"]/div[1]/span[1]/text()')[0].strip('\n        ')#每个视频的分类版块如动画
            view_num = item.xpath('div[@class = "info"]/div[3]/span[1]/text()')[0].strip('\n        ')#每个视频的播放量
            danmu = item.xpath('div[@class = "info"]/div[3]/span[2]/text()')[0].strip('\n        ')#弹幕
            upload_time  = item.xpath('div[@class = "info"]/div[3]/span[3]/text()')[0].strip('\n        ') # 上传日期
            up_author = item.xpath('div[@class = "info"]/div[3]/span[4]/a/text()')[0].strip('\n        ')#up主

            df = pd.DataFrame({'region': [region],'title': [title], 'view_num': [view_num], 'danmu': [danmu], 'upload_time': [upload_time], 'up_author': [up_author], 'bvid': [bvid], 'video_url': [video_url]})
            result = pd.concat([result, df])

        time.sleep(random.random() + 1)
        print('已经完成b站第 {} 页爬取'.format(i))
    cwd = os.getcwd()
    cwd = cwd[:cwd.find('script')]
    saveName = cwd + 'data/search_data/' + saveName + ".csv"
    result.to_csv(saveName, encoding='utf-8-sig',index=False)  # 保存为csv格式的文件
    return result

keyword = '俄乌'
page = 50
saveName = 'ewu'
get_target(keyword, page,saveName)
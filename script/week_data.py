import requests
import json
import os
import pandas as pd

INDEX_URL = 'https://api.bilibili.com/x/web-interface/popular/series/one?number={page}'

def scrape_api(url):
    response = requests.get(url)
    return response.json()

def scrape_index(page):
    url = INDEX_URL.format(page=page)
    return scrape_api(url)

def get_video_info(item):
    bvid = item.get('bvid')
    title = item.get('title')
    author = item.get('owner').get('name')
    mid = item.get('owner').get('mid')
    play = item.get('stat').get('view')
    danmu = item.get('stat').get('danmaku')
    comment = item.get('stat').get('reply')
    like = item.get('stat').get('like')
    coin = item.get('stat').get('coin')
    collect = item.get('stat').get('favorite')
    video = {
        'bvid': bvid,
        'title': title,
        'mid': mid,
        'author': author,
        'play': play,
        'danmu': danmu,
        'comment': comment,
        'like': like,
        'coin': coin,
        'collect': collect
    }
    #bv号，视频标题，up主mid，up主名称，播放量，弹幕量，评论量，点赞量，投币量，收藏量
    return video

def get_week_info(first, TOTAL_PAGE):
    for page in range(TOTAL_PAGE):
        data = []
        nowNum = first - page
        index_data = scrape_index(nowNum)
        allvideos = index_data.get('data')
        videolist = allvideos.get('list')
        for item in videolist:
            data.append(get_video_info(item))
            # df = pd.DataFrame(data,columns=['bvid', 'title', 'mid', 'author', 'play', 'danmu', 'comment', 'like', 'coin', 'collect'])
            json_str = json.dumps(data, ensure_ascii=False, indent=4)
            cwd = os.getcwd()
            with open(cwd + '/data/weekly-recommend/' + str(nowNum) + '.json', 'w', encoding='utf-8') as json_file:
                json_file.write(json_str)
    return data

data = get_week_info(153, 30)

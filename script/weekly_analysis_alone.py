import json
import os
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

path = "../data/weekly-recommend/"
fileList = os.listdir(path)
fileList.sort()

#读取数据
DataList = []
for file in fileList:
    if file == '.DS_Store':
        continue
    with open(path + file, "r") as f:
        json_data = json.load(f)
        DataList.append(json_data)
#print(DataList)

name = ['播放量','弹幕量','评论量','点赞','硬币数量','收藏']
type = ['play','danmu','comment','like','coin','collect']
rate = [1e8, 1e4, 1e4, 1e4, 1e4, 1e4]
dw = ["亿", "万", "万", "万", "万", "万"]
ext = [0.35, 0.38, 0.35, 0.5, 0.39, 0.4]
# 显示高度
def autolabel(rects, cnt):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2 - ext[cnt], height + 5, '%s' % round(float(height/rate[cnt]),1))

#绘图
x = np.arange(1,31)
cnt = 0
for i in type:
    plt.figure(figsize=(16, 4))
    Weeks = []
    for oneWeek in DataList:
        num = 0
        for item in oneWeek:
            num += item[type[cnt]]
        Weeks.append(num)
    autolabel(plt.bar(range(len(Weeks)), Weeks, tick_label=x, width=0.8, lw=1), cnt)
    plt.title('B站每周必看分区 近三十周'+ name[cnt] +'走势' + f"(单位:{dw[cnt]})")

    plt.savefig(f'../picture/weely_pic_alone/{name[cnt]}.jpg')
    cnt += 1
#    plt.show()

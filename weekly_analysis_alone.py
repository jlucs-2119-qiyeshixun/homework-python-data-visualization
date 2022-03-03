import json
import os
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

path = "data/weekly-recommend/"
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

# 显示高度
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2.- 0.2, 1.03*height, '%s' % int(height))


#绘图
x = np.arange(1,31)
cnt = 0
for i in type:
    Weeks = []
    for oneWeek in DataList:
        num = 0
        for item in oneWeek:
            num += item[type[cnt]]
        Weeks.append(num)
    autolabel(plt.bar(range(len(Weeks)), Weeks, tick_label=x))
    plt.title('B站每周必看分区 近三十周'+ name[cnt] +'走势')
    cnt += 1
    plt.show()
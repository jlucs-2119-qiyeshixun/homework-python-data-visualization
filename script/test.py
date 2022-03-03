
# import json

# f = open('da.json', "r")
# data = f.readline()

# data = json.loads(data)
# data = data["data"]["typelist"]

# ans = {}
# for x in data:
#     ans[x["id"]] = {
#         "name": x["name"],
#         "parent": x["parent"],
#         "desc": x["desc"]
#     }
#     for y in x["children"]:
#         ans[y["id"]] = {
#             "name": y["name"],
#             "parent": y["parent"],
#             "desc": y["desc"]
#         }

# with open('ans.json', "w", encoding="utf-8") as f:
#     f.write(json.dumps(ans, ensure_ascii=False))




from cProfile import label
from random import random
from time import time
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np
import popular_amount as amount
import random


# fig = plt.figure()
# ax = fig.add_subplot(2,2,1)

# plt.ion()  # 开启交互模式
# # ax.subplots()

# for j in range(20):
#     fig.clf()     # 清空画布
#     ax.xlim(0, 10)      # 因为清空了画布，所以要重新设置坐标轴的范围
#     ax.ylim(0, 10)
    
#     x = [random.randint(1,9) for i in range(10)]
#     y = [random.randint(1,9) for i in range(10)]
    
#     ax.scatter(x, y)
#     ax.pause(0.2)
    
# ax.ioff()
# plt.show()

name_dict = {
    "favorate":"高点赞",
    "other":"其他",
    "shared":"高分享",
    "watch":"高播放量",
    "notag":"无标签",
    "search":"高搜索",
    "popular":"人气飙升"
}

def draw_fig1():
    for k,v in rcmd_tag_amount.items():
        ax1.plot(v['time'],v['list'],label=name_dict[k])
    ax1.legend()
    ax1.set_title('哔哩哔哩热榜标签占比')

def draw_fig2(idx):

    sizes = []
    labels = []
    explode = []
    if idx < 0 or idx >= len(date_list):
        return
    key = date_list[idx]
    print(key,idx)
    item = amount.get_by_datetime(key)
    
    
    sizes = [len(v['list']) for k,v in item.items()]
    labels = [name_dict[k] for k,v in item.items()]
    explode = [0.01 for k in item.items()]

    # print(sizes)
    # print(labels)

    ax2.clear()
    ax2.set_title(f'热榜标签占比 {key.day}日 {key.hour}时 数据')
    ax2.pie(sizes,pctdistance=1.12,autopct='%1.2f%%',explode = explode)
    ax2.legend(labels=labels,loc='lower right')
    ax2.figure.canvas.draw()


def on_press(event):
    if event.inaxes != ax1:
        return
    print(event)
    idx = round(event.xdata)
    draw_fig2(idx)
    plt.draw()


plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
fig = plt.figure()
fig.canvas.mpl_connect("button_press_event",on_press)

ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

rcmd_tag_amount,date_list = amount.get_rcmd_tag()

draw_fig1()
draw_fig2(0)

plt.show()




from cProfile import label
from random import random
from time import time
import matplotlib.pyplot as plt
import numpy as np
import popular_amount as amount

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
ax2 = fig.add_subplot(2,2,3)

rcmd_tag_amount,date_list = amount.get_rcmd_tag()

draw_fig1()
draw_fig2(0)

plt.show()




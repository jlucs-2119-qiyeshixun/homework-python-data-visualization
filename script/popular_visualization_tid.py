from random import random
from time import time
from turtle import left
from gevent import config
import matplotlib.pyplot as plt
import numpy as np
import popular_amount as amount
import config

def draw_fig1():

    for k,v in tid_amount.items():
        # print(v)
        ax1.plot(v['date'],v['list'],label=config.region_info[str(k)]['name'])
    ax1.legend()
    ax1.set(xlabel='(日期自2020-3-3日开始)',ylabel='大类所占百分比',title='哔哩哔哩热榜视频所属大类占比')

def draw_fig2(idx):

    sizes = []
    labels = []
    explode = []
    if idx < 0 or idx >= len(date_list):
        return
    key = date_list[idx]
    # print(key,idx)
    item = amount.get_tid_by_datetime(key)
    
    
    sizes = [v['count'] for v in item]
    labels = [v['name'] for v in item]
    explode = [0.01 for k in item]

    # print(sizes)
    # print(labels)

    ax2.clear()
    ax2.set_title(f'热榜标签占比 {key.day}日 {key.hour}时 数据')
    ax2.pie(sizes,pctdistance=1.12,autopct='%1.2f%%',explode = explode,radius=1.2)
    ax2.legend(labels=labels,loc='right',borderaxespad=-12)
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

tid_amount,date_list = amount.get_tid_list()

draw_fig1()
draw_fig2(0)

plt.show()




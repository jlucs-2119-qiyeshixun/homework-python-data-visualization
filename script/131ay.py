import json
import os
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

path = "../data/weekly-recommend/"

with open(path + "126.json") as f:
    data = json.load(f)
    labels = []
    values = []
    for x in data:
        labels.append(x["title"])
        values.append(x["play"])
    la = range(len(data))
    ig, ax = plt.subplots()
    b = ax.barh(labels, values, color='#6699CC')

    plt.title("第126期每周必看播放量")
    plt.show()

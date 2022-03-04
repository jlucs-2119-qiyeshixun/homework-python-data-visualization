import json
import os
import matplotlib.pyplot as plt
import numpy as np

time_from = 20220202
time_to = 20220302

data_dir = f"../data/region_data/{time_from}_{time_to}/"
result_dir = f"../result/region_data/{time_from}_{time_to}/"
picture_dir = '../picture/region/'
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def get_result():
    for file in os.listdir(data_dir):
        if file.split(".")[-1] != "json":
            continue
        region_name = file.split("_")[-1].split(".")[0]
        final_ans = {
            "r_name": region_name,
            "data": [],
            "max_play": 0,
            "min_play": 100000000000,
            "total_play": 0
        }
        ans = []
        with open(data_dir + file, "r", encoding="utf-8") as f:
            line_data = f.readline()
            line_data = json.loads(line_data)["data"]
            for x in line_data:
                name = x["name"]
                lt = x["list"]

                sum = 0
                maxx= 0
                minn = 10000000000

                for tp in lt:
                    sum += tp["play"]
                    maxx = max(maxx,tp["play"])
                    minn = min(minn,tp["play"])
                ans.append({
                    "name": name,
                    "total_play": sum,
                    "max_play": maxx,
                    "min_play": minn,
                    "avg_play": float(sum/len(lt))
                })
                final_ans["max_play"] = max(final_ans["max_play"], maxx)
                final_ans["min_play"] = min(final_ans["min_play"], minn)
                final_ans["total_play"] += sum

        final_ans["data"] = ans
        with open(result_dir + f"result_{region_name}.json", "w", encoding='utf-8') as ff:
            ff.write(json.dumps(final_ans, ensure_ascii=False))


def analysis():
    for file in os.listdir(result_dir):
        if file.split(".")[-1] != "json":
            continue
        region_name = file.split("_")[-1].split(".")[0]
        with open(result_dir + file, "r", encoding="utf-8") as f:
            line_data = f.readline()
            line_data = json.loads(line_data)["data"]

            total = 0
            labels = []
            values = []
            for x in line_data:
                labels.append(x["name"])
                values.append(x["total_play"])
                total += x["total_play"]

            plt.figure(figsize=(20, 20))
            explode = [0.05 for i in range(len(line_data))]
            patches, l_text, p_text = plt.pie(values,
                                            explode=explode,
                                            labels=labels,
                                            autopct='%0.1f%%')
            for t in l_text:
                t.set_size(30)
            for t in p_text:
                t.set_size(25)

            fl = "{:.2f}".format(total/1e8)
            plt.text(-0.3, -1.4, f"总播放量：{fl}亿次", family='Arial Unicode MS', fontsize=30, style='italic')
            plt.title(f'B站{region_name}区 热门视频播放量占比\n\n 20220202～20220302', fontsize=30)
            plt.savefig(f'{picture_dir}B站{region_name}区 热门视频播放量占比.jpg')
            #plt.show()

def analysis_all_region():
    labels = []
    values = []
    for file in os.listdir(result_dir):
        if file.split(".")[-1] != "json":
            continue
        region_name = file.split("_")[-1].split(".")[0]
        labels.append(region_name)
        with open(result_dir + file, "r", encoding="utf-8") as f:
            line_data = f.readline()
            total = "{:.2f}".format(json.loads(line_data)["total_play"]/1e8)
            values.append(float(total))

    print(labels)
    print(values)
    plt.figure(figsize=(10, 10))
    plt.yticks(np.arange(0, 8, 0.5))
    plt.bar(range(len(labels)), values, tick_label=labels, color=['r', 'g', 'b', 'y', 'c', 'm', 'k'])
    plt.tick_params(axis='both', labelsize=15)
    plt.xlabel('\nB站各区热榜播放量柱形图', fontsize=20)

    for a, b in zip(range(len(labels)), values):
        plt.text(a, b + 0.05, '%.2f亿' % b, ha='center', va='bottom', fontsize=15)

    plt.savefig(picture_dir + 'B站各区热榜播放量柱形图.jpg')


#get_result()
#analysis()
#analysis_all_region()
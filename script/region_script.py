import json
import os
time_from = 20220202
time_to = 20220302

data_dir = f"../data/region_data/{time_from}_{time_to}/"
result_dir = f"../result/region_data/{time_from}_{time_to}/"


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
        print(region_name)

#get_result()
analysis()
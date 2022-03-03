
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




import matplotlib.pyplot as plt
import numpy as np
import popular_amount as amount





def on_press(event):
    print(event)


fig = plt.figure()
fig.canvas.mpl_connect("button_press_event",on_press)

ax1 = fig.add_subplot(2,1,1)

# ax1.plot([1,2,3,4],["h","j","k","l"],linewidth=1,marker='o',markersize=4)
# ax1.plot([1,2,3,4],["h","j","k","l"])
# ax2.plot(x, y_sin, 'go--', linewidth=2, markersize=12)
# ax3.plot(x, y_cos, color='red', marker='+', linestyle='dashed')

rcmd_tag_amount = amount.get_rcmd_tag()

# print(rcmd_tag_amount)
for k,v in rcmd_tag_amount.items():
    print(k,v['list'][0])
    ax1.plot(v['time'],v['list'])


plt.show()



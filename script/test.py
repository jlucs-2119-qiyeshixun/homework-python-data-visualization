import json

f = open('da.json', "r")
data = f.readline()

data = json.loads(data)
data = data["data"]["typelist"]

ans = {}
for x in data:
    ans[x["id"]] = {
        "name": x["name"],
        "parent": x["parent"],
        "desc": x["desc"]
    }
    for y in x["children"]:
        ans[y["id"]] = {
            "name": y["name"],
            "parent": y["parent"],
            "desc": y["desc"]
        }

with open('ans.json', "w", encoding="utf-8") as f:
    f.write(json.dumps(ans, ensure_ascii=False))

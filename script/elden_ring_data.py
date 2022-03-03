#"stand_alone"
import requests

url = "https://api.bilibili.com/x/web-interface/newlist"
params = {
    "rid": 17,
    "type": 0,
    "pn": 1,
    "ps": 20
}
for i in range(10000):
    resp = requests.request('GET', url=url, params=params)
    print(resp.text)
    params["pn"] = i

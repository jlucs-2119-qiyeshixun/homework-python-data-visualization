import shlex

f = open('da.txt', "r")
lines = f.readlines()
flag = 0
mp = {}
zid = 0
for x in lines:
    if x == "\n":
        flag = 1
        continue

    id = x.split(': ')[0]
    if flag:
        zid = id
        flag = 0
    else:
        mp[id] = zid

ff = open()
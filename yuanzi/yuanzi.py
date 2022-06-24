def merge(files):
    doc = []
    for x in files:
        a = open(x).read().splitlines()
        doc += a
    doc = [x for x in doc if x]
    Ji = set(doc)
    print(len(Ji))
    return Ji


files = ["BiHua/BiHua.txt", "BuJian/BuJian.txt",         "DuTiZi/DuTiZi.txt"]
JiZi = merge(files)

files = ["BiHua/BiHua.txt",    "BuJian/BuJianIds.txt", "DuTiZi/DuTiZi.txt"]
JiZiIds = merge(files)

fresh = JiZiIds-JiZi
fresh = list(fresh)
fresh.sort()
fresh = ''.join(fresh)
print(len(fresh), fresh)


def save(JiZi, path):

    JiZi = list(JiZi)
    JiZi.sort()

    with open(path, "w") as f:
        for x in JiZi:
            f.write(x+'\n')
    print(len(JiZi))

path = "YuanZi/YuanZi.txt"  
save(JiZi, path)
path = "YuanZi/YuanZiIds.txt"  
save(JiZiIds, path)

"""
1719
1773
54 αℓ↔↷①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑲△いよりコサ全車龜龜丹女年華龜？𛂦𠦮𡋬𢚎𭔥乁凵北卑及多尢㠯衣豕𰀁
1719
1773
"""


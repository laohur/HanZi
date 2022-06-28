from logzero import logger
from UnicodeTokenizer.UnicodeTokenizer import detect_hanzi


def merge(files):
    doc = []
    for x in files:
        a = open(x).read().splitlines()
        doc += a
    doc = [x for x in doc if x]
    Ji = set()
    for x in doc:
        if detect_hanzi(x):
            Ji.add(x)
        else:
            logger.warning(x)
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
[W 220629 01:32:29 YuanZi:16] �
1717
[W 220629 01:32:29 YuanZi:16] �
1741
24 全車龜龜丹女年華龜𠦮𡋬𢚎𭔥乁凵北卑及多尢㠯衣豕𰀁
1717
1741
"""


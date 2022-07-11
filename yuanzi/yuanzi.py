from logzero import logger
from UnicodeTokenizer.UnicodeTokenizer import detect_hanzi


def merge(files):
    doc = []
    for x in files:
        a = open(x).read().splitlines()
        doc += a
    doc = [x for x in doc if x]
    Ji = set(x for x in doc if detect_hanzi(x))
    notHanzi = set(x for x in doc if not detect_hanzi(x))
    logger.warning(''.join(notHanzi))
    logger.info(len(Ji))
    return Ji


files = ["BiHua/BiHua.txt", "BuJian/BuJian.txt",         "DuTiZi/DuTiZi.txt"]
JiZi = merge(files)

files = ["BiHua/BiHua.txt",    "BuJian/BuJianIds.txt", "DuTiZi/DuTiZi.txt"]
JiZiIds = merge(files)

fresh = JiZiIds-JiZi
fresh = list(fresh)
fresh.sort()
fresh = ''.join(fresh)
logger.info((len(fresh), fresh))


def save(JiZi, path):

    JiZi = list(JiZi)
    JiZi.sort()

    with open(path, "w") as f:
        for x in JiZi:
            f.write(x+'\n')
    logger.info(len(JiZi))


path = "YuanZi/YuanZi.txt"
save(JiZi, path)
path = "YuanZi/YuanZiIds.txt"
save(JiZiIds, path)

"""
[W 220712 04:11:06 YuanZi:13] �
[I 220712 04:11:06 YuanZi:14] 1128
[W 220712 04:11:06 YuanZi:13] �
[I 220712 04:11:06 YuanZi:14] 1168
[I 220712 04:11:06 YuanZi:28] (40, '全車龜龜丹女年卑既者辶華龜𠁧𠁾𠃉𠤬𠦮𡋬𡰣𢎗𢎜𢎧𢚎𤰃𬼂𬼄𭔥𮍌乁凵北卑及多尢㠯衣豕𰀁')
[I 220712 04:11:06 YuanZi:39] 1128
[I 220712 04:11:06 YuanZi:39] 1168
"""

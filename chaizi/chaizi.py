import random
import collections
from logzero import logger

JieGou = "〾⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻"
JieGou2 = "⿰⿱⿴⿵⿶⿷⿸⿹⿺⿻"
JieGou3 = "⿲⿳"

stars1 = 'αℓ↔↷①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑲△'
stars1 = set(stars1)
stars2 = '𛂦𠦮𡋬𡰣𢚎𤣩𨪐𬼂𬼄𭔥乁𰀁'
star = '𱍊'

path = "ChaiZi/Ids1.txt"
doc = open(path).read().splitlines()
doc = [x.split('\t') for x in doc]
ids = {k: v for k, v in doc}
logger.info(f"{path} --> {len(ids)}")  # ChaiZi/Ids1.txt --> 94265


def automic(dic0):
    dic1 = {}
    for k, v in dic0.items():
        u = ''.join(dic0.get(x, x) for x in v)
        dic1[k] = u
    return dic1


YuanZi = open("YuanZi/YuanZi.txt").read().splitlines()
YuanZi = set(x for x in YuanZi if x)
for x in YuanZi:
    ids[x] = x


def seg(dic0):
    bujians0 = set(''.join(dic0.values()))
    for i in range(5):
        dic1 = automic(dic0)
        bujians1 = set(''.join(dic1.values()))
        logger.info((i, len(bujians0), len(bujians1),
                    ''.join(bujians0-bujians1)[:10]))
        dic0 = dic1
        bujians0 = bujians1
    return dic0


dic = seg(ids)



def save(ChaiZi, path):
    ChaiZi.sort(key=lambda x: x[0])

    with open(path, "w") as f:
        for x in ChaiZi:
            r = '\t'.join(x)
            f.write(r+'\n')
    logger.info(f"{len(ChaiZi)} --> {path}")

ChaiZi = [ (k,v) for k, v in ids.items()  ]
path = "ChaiZi/ChaiZi.txt"
save(ChaiZi,path)



"""
[I 220625 06:37:08 ChaiZi:18] ChaiZi/Ids1.txt --> 94282
[I 220625 06:37:10 ChaiZi:40] (0, 11105, 3036, '𥦮枚芩暹揚僧歧包廸鞍')
[I 220625 06:37:12 ChaiZi:40] (1, 3036, 1788, '貞爯樂孝𬙙於𢀡素𤕫守')
[I 220625 06:37:15 ChaiZi:40] (2, 1788, 1771, '倠𭥍𡵂𠮷𠔼𠄠𢆶𫧇𠮥冃')
[I 220625 06:37:17 ChaiZi:40] (3, 1771, 1771, '')
[I 220625 06:37:20 ChaiZi:40] (4, 1771, 1771, '')
[I 220625 06:37:20 ChaiZi:58] 94462 --> ChaiZi/ChaiZi.txt
"""

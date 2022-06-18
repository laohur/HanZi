
JieGou = '〾⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻'
# for x in JieGou:
# print(ord(x))


def slim(v):
    if len(v) <= 3:
        return v
    for x in v[1:-1]:
        if x < '⿰' or x > '⿻':
            w = v[0]+x+v[-1]
            return w
    return v


def loadHeZi(path, lite=True):
    HeZi = {}
    for l in open(path):
        w = l.strip().split('\t')
        k, v = w
        if k[0] == "𱊮":
            d = 0
        if lite:
            v = slim(v)
        HeZi[k] = v
    return HeZi


path = "HeZi/HeZi.txt"
HeZi = loadHeZi(path)

from logzero import logger
logger.info(f"{path} --> loadHeZi {len(HeZi)}")
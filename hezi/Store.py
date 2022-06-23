
from logzero import logger
JieGou = '〾⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻'
# for x in JieGou:
# print(ord(x))

star = "𱊮"


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
        if k[0] == star:
            d = 0
        if lite:
            v = slim(v)
        HeZi[k] = v
    logger.info(f"{path} --> loadHeZi {len(HeZi)}")
    return HeZi


He2Yuan = loadHeZi("HeZi/He2Yuan.txt")
He2Ji = loadHeZi("HeZi/He2Ji.txt")

if __name__ == "__main__":

    print(star, He2Yuan.get(star, star))
    print(star, He2Ji.get(star, star))
    """
    𱊮 ⿵亡鳥
    𱊮 ⿵亡鳥
    """

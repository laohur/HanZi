import unicodedata

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

class ZiCutter:
    def __init__(self,HanZiBase="Ji"):
        if HanZiBase=='Ji':
            self.HeZi = loadHeZi("HeZi/He2Ji.txt")
        else:
            self.HeZi = loadHeZi("HeZi/He2Yuan.txt")

    def cutHan(self, zi,shrink=True):
        ids=self.HeZi.get(zi,zi)
        if shrink:
            s=slim(ids)
            return s
        return ids

    def cutRare(self,char):
        assert len(char)==1
        tokens=[]
        try:
            name = unicodedata.name(char)
            l = name[:2].lower().split('-')[0].split()[0]
            r = name[-1].lower()
            tokens += [l, '#'+r]
        except:
            r=ord(char)%100
            s='#'+f'0{r}'[-2:]
            tokens=[ s ]
        return tokens

    def cutChar(self,char):
        assert len(char)==1
        if char in self.HeZi:
            t=self.cutHan(char)
            return list(t)
        else:
            t= self.cutRare(char)
            return t



if __name__ == "__main__":

    He2Yuan = loadHeZi("HeZi/He2Yuan.txt")
    He2Ji = loadHeZi("HeZi/He2Ji.txt")


    print(star, He2Yuan.get(star, star))
    print(star, He2Ji.get(star, star))
    """
    𱊮 ⿵亡鳥
    𱊮 ⿵亡鳥
    """
    line="'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)'"
    cutter=ZiCutter()
    for c in line:
        if c=='夏':
            d=0
        print(cutter.cutChar(c))

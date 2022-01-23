YuanZi = open("yuanzi.txt").read().splitlines()
ChangYongZi = open("changyongzi.txt").read().splitlines()

JiZi = YuanZi+ChangYongZi
JiZi = [x for x in JiZi if x]
JiZi = list(set(JiZi))
JiZi.sort()
with open("jizi.txt", "w") as f:
    for x in JiZi:
        f.write(x+'\n')

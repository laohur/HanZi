BiHua = open("BiHua.txt").read().splitlines()
Bujian = open("BuJian.txt").read().splitlines()
DuTiZi = open("DuTiZi.txt").read().splitlines()

JiZi = BiHua+Bujian+DuTiZi
JiZi = [x for x in JiZi if x]
JiZi = list(set(JiZi))
JiZi.sort()
with open("YuanZi.txt", "w") as f:
    for x in JiZi:
        f.write(x+'\n')

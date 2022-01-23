BiHua = open("bihua.txt").read().splitlines()
Bujian = open("bujian.txt").read().splitlines()
DuTiZi = open("dutizi.txt").read().splitlines()

JiZi = BiHua+Bujian+DuTiZi
JiZi = [x for x in JiZi if x]
JiZi = list(set(JiZi))
JiZi.sort()
with open("yuanzi.txt", "w") as f:
    for x in JiZi:
        f.write(x+'\n')

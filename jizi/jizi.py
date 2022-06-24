YuanZi = open("YuanZi/YuanZi.txt").read().splitlines()
ChangYongZi = open("ChangYongZi/ChangYongZi.txt").read().splitlines()

JiZi = YuanZi+ChangYongZi
JiZi = [x for x in JiZi if x]
JiZi = list(set(JiZi))
JiZi.sort()
with open("JiZi/JiZi.txt", "w") as f:
    for x in JiZi:
        f.write(x+'\n')
print(len(JiZi))

"""
9799
"""

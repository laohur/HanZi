from logzero import logger
from UnicodeTokenizer.UnicodeTokenizer import detect_hanzi


YuanZi = open("YuanZi/YuanZi.txt").read().splitlines()
ChangYongZi = open("ChangYongZi/ChangYongZi.txt").read().splitlines()

doc = YuanZi+ChangYongZi
doc = [x for x in doc if x]
doc = set(doc)
JiZi = []
for x in doc:
    if detect_hanzi(x):
        JiZi.append(x)
    else:
        logger.warning(x)

JiZi.sort()
with open("JiZi/JiZi.txt", "w") as f:
    for x in JiZi:
        f.write(x+'\n')
print(len(JiZi))

"""
9799
"""

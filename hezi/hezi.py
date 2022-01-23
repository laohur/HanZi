
HeZi = {}

YiTiZi = open("chaizi.txt").read().splitlines()
for l in YiTiZi:
    w = l.split('\t')
    if len(w) != 2:
        continue
    k, v = w
    HeZi[k] = v

JiZi = open("jizi.txt").read().splitlines()
JiZi = [x for x in JiZi if x]
JiZi = set(JiZi)
for x in JiZi:
    HeZi[x] = x

"""
𤍽	𤑔 k,v
HeZi[𤑔]=HeZi[𤍽] if 𤍽 in 𤑔
HeZi[v]=HeZi[k] if k in v
"""
YiTiZi = open("yitizi.txt").read().splitlines()
for l in YiTiZi:
    a = '𱌪'
    b = '𱌛'
    if a in l or b in l:
        d=0
    w = l.split('\t')
    if len(w) != 2:
        continue
    k, v = w
    if v not in HeZi:
        k, v = v, k
    if k in JiZi:
        v = k
    if k in HeZi[v]:
        HeZi[v] = HeZi[k]
    if v in HeZi:
        HeZi[k] = HeZi[v]
    elif k in HeZi:
        print(k, v)


def split(dic0, epoch=0):
    dic1 = {}
    for k, v in dic0.items():
        dic1[k] = ''.join(dic0[x] for x in v)

    base0 = set(''.join(x for x in dic0.values()))
    base1 = set(''.join(x for x in dic1.values()))
    print(f"epoch:{epoch} base:{len(base0)} --> {len(base1)} ")
    return dic1


dic0 = {k: v for k, v in HeZi.items()}
for i in range(5):
    dic1 = split(dic0, i)
    dic0 = dic1
base0 = list(set(''.join(x for x in dic0.values())))
base0.sort()
with open("base.txt", "w") as f:
    for x in base0:
        f.write(x+'\n')
print(set(base0)-JiZi)

chars = list(dic0)
chars.sort()
with open("hezi.txt", "w") as f:
    for x in chars:
        l = '\t'.join(dic0[x])
        f.write(l+'\n')

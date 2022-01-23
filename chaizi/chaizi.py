
def get_bujians(dic):
    bujians = set(dic.values())
    for i in range(10):
        bujians = set(''.join(dic.get(x, x) for x in bujians))
        print(i, len(bujians))
    bujians = list(bujians)
    bujians.sort()
    bujians = ''.join(bujians)
    return bujians


def read_ids(path):
    doc = []
    with open(path, encoding="utf-8") as f:
        # U+6717	朗	⿰⿱丶⑤月[GTJV]	⿰良月[K]
        for line in f:
            if not line or not line.startswith('U+'):
                continue
            line = line.strip()
            # line="U+2EBC9\t𮯉\t⿰齒⿱人米\t⿰齒籴"
            tokens = line.split('\t')
            char = tokens[1]
            metas = [x.split('[')[0] for x in tokens[2:]]
            metas.sort(key=lambda x: len(x))
            doc.append([char, metas])
    return doc


doc = read_ids("ids.txt")

print(len(doc), doc[0])

ids0 = {}
for cols in doc:
    k, v = cols[:2]
    ids0[k] = v[0]

# ids=[ cols[:2] for cols in doc ]

ZiXing = open("zixing.txt").read().splitlines()
for l in ZiXing:
    w = l.split()
    if not w:
        continue
    if len(w) == 1:
        k = w[0]
        v = k
    if len(w) >= 2:
        k, v = w[:2]
    if k not in ids0:
        ids0[k] = v
        # print(k, v)


bujians = get_bujians(ids0)
print(bujians)

YuanZi = open("../yuanzi/yuanzi.txt").read().splitlines()
YuanZi = set(x for x in YuanZi if x)

ChaiZi = []
for k, v in ids0.items():
    if k in YuanZi:
        v = k
    ChaiZi.append((k, v))
ChaiZi.sort(key=lambda x: x[0])

with open("chaizi.txt", "w") as f:
    for x in ChaiZi:
        r = '\t'.join(x)
        f.write(r+'\n')

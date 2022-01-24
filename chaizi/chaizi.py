
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


def read_ids2(path):
    doc = []
    for l in open(path).read().splitlines():
        l = l.strip()
        if not l:
            continue
        # 与	⿹⿺㇉一一(.);⿻[b]⿺㇉一一(J);⿹⿺㇉一丨(qgs);⿺𠚣一(qzp);⿹⿺𠃑一丨(qzs)
        w = l.split()
        k = w[0]
        v = w[1].split('(')[0]
        v = v.split(';')[0]
        if v == '#':
            v = k
        # v = ''
        # for x in w[1]:
        #     if ord(x) >= 128:
        #         v += x
        #     else:
        #         break
        # if not v:
        #     v = k
        doc.append((k, v))
    return doc


doc = read_ids2("ids_lv2.txt")
print(len(doc), doc[0])

# ids0 = {}
for k, v in doc:
    if min(ord(x) for x in v) > 128:
        if k not in ids0:
            ids0[k] = v
        elif len(ids0[k]) > len(v):
            if len(v) == 1:
                print("l2", k, ids0[k], v)
            ids0[k] = v

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
    if "？" in v or len(v) < 3:
        continue
    if k not in ids0:
        ids0[k] = v
        print("字形", k, v)
    # elif len(ids0[k]) > len(v) >= 3:
    #     print("字形", k, ids0[k], v)
    #     ids0[k] = v


def get_bujians(dic):
    bujians0 = set(dic.values())
    for i in range(10):
        bujians1 = set(''.join(dic.get(x, x) for x in bujians0))
        print(i, len(bujians1), ''.join(bujians0-bujians1)[:10])
        bujians0 = bujians1
    bujians = list(bujians0)
    bujians.sort()
    bujians = ''.join(bujians)
    return bujians


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

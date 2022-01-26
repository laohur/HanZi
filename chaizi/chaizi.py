
JieGou = "⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻"
JieGou2 = "⿰⿱⿴⿵⿶⿷⿸⿹⿺⿻"
JieGou3 = "⿲⿳"


def valid_ids(seq):
    # print(seq)
    if len(seq) == 1:
        return 1
    if len(seq) == 0 or len(seq) == 2:
        return 0
    for i in range(len(seq)-1, -1, -1):
        if seq[i] not in JieGou:
            continue
        if seq[i] in JieGou2:
            if i+2 > len(seq)-1:
                return 0
            s = seq[:i]+"*"
            if i+2 < len(seq)-1:
                s += seq[i+3:]
            return valid_ids(s)
        if seq[i] in JieGou3:
            if i+3 > len(seq)-1:
                return 0
            s = seq[:i]+'*'
            if i+3 < len(seq)-1:
                s += seq[i+4:]
            return valid_ids(s)
    return 0


print(valid_ids('⿱艹⿳⿲止自巳八夂'))


def read_ids(path):
    doc = []
    # U+6717	朗	⿰⿱丶⑤月[GTJV]	⿰良月[K]
    for line in open(path).read().splitlines():
        if not line or not line.startswith('U+'):
            continue
        line = line.strip()
        # line="U+2EBC9\t𮯉\t⿰齒⿱人米\t⿰齒籴"
        tokens = line.split('\t')
        k = tokens[1]
        seqs = [x.split('[')[0] for x in tokens[2:]]
        seqs = [x for x in seqs if valid_ids(x)]
        seqs.sort(key=lambda x: len(x))
        if not seqs:
            v = k
        else:
            v = seqs[0]
        doc.append([k, v])
    return doc


doc = read_ids("ids.txt")
print(len(doc), doc[0])

ids0 = {k: v for k, v in doc}


def read_ids2(path):
    doc = []
    for l in open(path).read().splitlines():
        l = l.strip()
        if not l:
            continue
        # 与	⿹⿺㇉一一(.);⿻[b]⿺㇉一一(J);⿹⿺㇉一丨(qgs);⿺𠚣一(qzp);⿹⿺𠃑一丨(qzs)
        w = l.split("\t")
        k = w[0]
        seqs = w[1].split(";")
        seqs = [x.split('(')[0] for x in seqs]
        seqs = [x for x in seqs if min(ord(y) for y in x) > 128]
        seqs = [x for x in seqs if valid_ids(x)]
        seqs.sort(key=lambda x: len(x))
        if not seqs:
            v = k
            # continue
        else:
            v = seqs[0]
        if len(v) <= 1:
            v = k
        doc.append((k, v))
    return doc


doc = read_ids2("ids_lv2.txt")
print(len(doc), doc[0])

for k, v in doc:
    if ord(k) <= 128:
        continue
    if k not in ids0:
        ids0[k] = v
        # print("字形增", k, v)
    elif len(ids0[k]) > len(v) >= 3:
        ids0[k] = v

ZiXing = open("zixing.txt").read().splitlines()
for l in ZiXing:
    if '偺' in l:
        d = 0
    w = l.split('\t')
    if not w:
        continue
    if len(w) <= 1:
        k = w[0]
        v = k
    if len(w) >= 2:
        k, v = w[:2]
    if "？" in v:
        continue
    if not valid_ids(v):
        # continue
        v = k
    if k not in ids0:
        ids0[k] = v
        print("字形增", k, v)
    elif len(ids0[k]) > len(v) >= 3:
        # if min(ord(x) for x in ids0[k]) < ord("⺀"):
        print("字形替", k, ids0[k], valid_ids(ids0[k]), v, valid_ids(v))
        ids0[k] = v


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

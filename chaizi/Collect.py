import random
import collections
from logzero import logger

JieGou = "〾⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻"
JieGou2 = "⿰⿱⿴⿵⿶⿷⿸⿹⿺⿻"
JieGou3 = "⿲⿳"

stars1 = 'αℓ↔↷①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑲△'
stars1 = set(stars1)
stars2 = '𛂦𠦮𡋬𡰣𢚎𤣩𨪐𬼂𬼄𭔥乁𰀁'
star = '𦞝'

YuanZi = open("YuanZi/YuanZi.txt").read().splitlines()
YuanZi = set(x for x in YuanZi if x)

YuanZiIds = open("YuanZi/YuanZiIds.txt").read().splitlines()
YuanZiIds = set(x for x in YuanZiIds if x)
bad = YuanZiIds-YuanZi


def odd(v):
    t = 0
    for x in v:
        if x in bad:
            t + 1
    return t


def read_ids(path="ChaiZi/ids.txt"):
    doc = []
    # U+6717	朗	⿰⿱丶⑤月[GTJV]	⿰良月[K]
    for line in open(path).read().splitlines():
        if not line or not line.startswith('U+'):
            continue
        line = line.strip()
        # line="U+2EBC9\t𮯉\t⿰齒⿱人米\t⿰齒籴"
        tokens = line.split('\t')
        k = tokens[1]
        if k == star:
            logger.info(tokens)
        seqs = [x.split('[')[0] for x in tokens[2:]]
        seqs = [x for x in seqs if x and x != k]
        # seqs = [x for x in seqs if valid_ids(x)]
        # seqs.sort(key=lambda x: seq_score(x))
        doc.append([k, seqs])
    return doc


def read_ids2(path="ChaiZi/ids_lv2.txt"):
    doc = []
    for l in open(path).read().splitlines():
        l = l.strip()
        if not l:
            continue
        # 与	⿹⿺㇉一一(.);⿻[b]⿺㇉一一(J);⿹⿺㇉一丨(qgs);⿺𠚣一(qzp);⿹⿺𠃑一丨(qzs)
        w = l.split("\t")
        k = w[0]
        if k == star:
            logger.info(w)
        if ord(k) < 128:
            continue
        seqs = w[1].split(";")
        seqs = [x.split('(')[0] for x in seqs]
        # seqs = [x for x in seqs if min(ord(y) for y in x) > 128]
        seqs = [''.join(x for x in s if ord(x) >= 128) for s in seqs]
        seqs = [x for x in seqs if x and x != k]
        # seqs = [x for x in seqs if valid_ids(x)]
        # seqs.sort(key=lambda x: seq_score(x))
        seqs = list(set(seqs))
        doc.append((k, seqs))
    return doc


def read_ZiXing(path="ChaiZi/ZiXing.txt"):
    doc = []
    raw = open(path).read().splitlines()
    raw = [x.split('\t') for x in raw]
    for w in raw:
        k = w[0]
        if k == star:
            logger.info(w)
        seqs = w[1:]
        seqs = [x for x in seqs if x and x != k]
        seqs = list(set(seqs))
        doc.append((k, seqs))
    return doc


def valid_ids(seq):
    if len(seq) <= 2:
        return 0
    if seq[0] not in JieGou:
        return 0
    if seq[-1] in JieGou or seq[-2] in JieGou:
        return 0

    return 1


def seq_score(seq):
    v = valid_ids(seq)
    o = odd(seq)
    score = v*100-len(seq)-10*o
    return score


def merge(doc, path):
    store = {}
    for k, v in doc:
        seqs = store.get(k, [])+v
        store[k] = seqs

    f = open(path, 'w')
    values = set()
    for k, seqs in store.items():
        if k == star:
            logger.info((k, seqs))
        seqs = [x for x in seqs if x and len(x) >= 2]
        if len(seqs) >= 3:
            c = collections.Counter(seqs)
            # logger.info((k,seqs))
            top = max(c.values())
            seqs = [x for x in seqs if c[x] == top]
        seqs = list(set(seqs))
        seqs.sort(key=lambda x: -seq_score(x))
        store[k] = seqs
        for x in seqs:
            values |= set(x)
        # 有k无v 有v无k
        t = [k]+seqs
        l = '\t'.join(t)
        f.write(l+'\n')

    keys = set(store)
    logger.info(
        f"keys:{len(keys)} values:{len(values)}  k-v:{len(keys-values)} v-k:{len(values-keys)} {''.join(values-keys)}")
    # keys:94265 values:11453  k-v:82832 v-k:20 、⿹⿵〾⿴⿻?⿲↔⿶⿷⿸⿰↷⿳⿺？⿱U
    # for x in values:
    #     if x not in store:
    #         store[x]=[]
    return store


def choice(store, path):
    # for x in YuanZi:
    # store[x] = x

    doc = open("ChaiZi/Valid.txt").read().splitlines()
    doc = [x.split('\t') for x in doc]
    for k, v in doc:
        store[k] = v

    ids = {}
    for k, seqs in store.items():
        if k in stars1:
            logger.info((k, seqs))
            d = 0
        if seqs:
            v = seqs[0]
        else:
            v = k
        ids[k] = v
    values = set(''.join(ids.values()))-set(ids)
    logger.info((len(values), ''.join(values)))  # (16, '↷⿶⿳⿵⿻⿴〾↔⿸⿹⿰？⿲⿱⿷⿺')
    for x in values:
        ids[x] = x

    doc = [(k, v) for k, v in ids.items()]
    doc.sort(key=lambda x: (x[0]))
    with open(path, 'w') as f:
        for k, v in doc:
            l = f"{k}\t{v}"
            f.write(l+'\n')
    keys = set(''.join(x[0] for x in doc))
    values = set(''.join(x[1] for x in doc))
    logger.info((len(keys), len(values)))
    logger.info((len(keys-values), len(values-keys)))


if __name__ == "__main__":

    logger.info(valid_ids('⿱艹⿳⿲止自巳八夂'))

    Ids = read_ids()
    logger.info((len(Ids), random.choice(Ids)))  # (88937, ['𦵀', ['⿱艹面']])

    Ids2 = read_ids2()
    logger.info((len(Ids2), random.choice(Ids2)))  # (92898, ('𥉲', ['⿰目展']))

    ZiXing = read_ZiXing()
    # (94227, ('𢐏', ['弛', '⿰弓𰲚']))
    logger.info((len(ZiXing), random.choice(ZiXing)))

    doc = Ids+Ids2+ZiXing
    chars = set(x[0] for x in doc)
    logger.info(("chars", len(chars)))  # ('chars', 94266)

    store = merge(doc, path="ChaiZi/IdsAll.txt")
    logger.info((star, store[star]))

    path = "ChaiZi/Ids1.txt"
    choice(store, path)

"""
[I 220625 06:35:42 Collect:165] (17, '⿲？⿷⿶⿹↔⿳⿴⿸↷⿵〾⿱\ue817⿻⿺⿰')
[I 220625 06:35:43 Collect:177] (94282, 10812)
[I 220625 06:35:43 Collect:178] (83470, 0)
"""

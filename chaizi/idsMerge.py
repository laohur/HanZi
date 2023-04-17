# -*- coding: utf-8 -*-

import random
import unicodedata
import re

from logzero import logger

JieGou1 = "〾↔↷"
JieGou2 = "⿰⿱⿴⿵⿶⿷⿸⿹⿺⿻"
JieGou3 = "⿲⿳"
JieGou = JieGou1+JieGou2+JieGou3

stars1 = 'αℓ↔↷①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑲△'
stars1 = set(stars1)
stars2 = '𠦮𡋬𡰣𢚎𤣩𨪐𬼄𭔥乁'
star = '𤆚'


def valid_ids(seq):
    if len(seq) <= 2:
        return False
    S = seq+' '
    flag = '㇣'
    for i in range(len(S)-2, -1, -1):
        x = S[i]
        if x in JieGou1:
            S = S[:i]+'㇣'+S[i+2:]
        elif x in JieGou2:
            S = S[:i]+'㇣'+S[i+3:]
        elif x in JieGou3:
            S = S[:i]+'㇣'+S[i+4:]
        else:
            if x not in '〇'+JieGou and unicodedata.category(x)[0] != 'L':
                return False
    if S == '㇣ ':
        return True
    return False

# U+4E0E	与	⿹②一[GTKV]	⿻②一[J]


def readIds(path="ChaiZi/ids.txt"):
    doc = []
    for line in open(path):
        if not line or not line.startswith('U+'):
            continue
        t = line.strip().split('\t')
        if len(t) < 3:
            continue
        k = t[1]
        if len(k) != 1 or ord(k) < 128:
            continue
        # v=[  x for x in t[2:]  if valid_ids(x)  ]
        v = t[2:]
        if k == star:
            logger.info(t)
        if v:
            doc.append((k, v))
    logger.info((path, len(doc), random.choice(doc)))
    return doc

# 丹	⿴⿻⺆一丶(.);⿴⿻冂一丶(pd);⿴⿻⺆一丨(q0662.);⿴⿻冂一丨(q0662s)


def readLv2(path="ChaiZi/ids_lv2.txt"):
    doc = []
    for l in open(path):
        t = l.strip().split('\t')
        if len(t) < 2:
            continue
        k = t[0]
        if len(k) != 1 or ord(k) < 128:
            continue
        v = [x.split('(')[0] for x in t[1].split(';')]
        # v=[  x for x in v  if valid_ids(x)  ]
        if k == star:
            logger.info(t)
        if not v:
            continue
        if v:
            doc.append((k, v))
    logger.info((path, len(doc), random.choice(doc)))
    return doc

# U+4E4C	乌	⿹&CDP-89DE;一


def readAll(path="ChaiZi/IdsAll.txt"):
    doc = []
    for l in open(path).read().splitlines():
        l = l.strip()
        t = l.split("\t")
        if len(t) != 3:
            continue
        k = t[1]
        if len(k) != 1 or ord(k) < 128:
            continue
        # v=[  x for x in t[2].split(';') if valid_ids(x)  ]
        v = [x for x in t[2].split(';')]
        if k == star:
            logger.info(t)
        if v:
            doc.append((k, v))
    logger.info((path, len(doc), random.choice(doc)))
    return doc

# 㕟	⿰⿱⺊𠕁又	喟


def readZixing(path="ChaiZi/ZiXing.txt"):
    doc = []
    for l in open(path).read().splitlines():
        l = l.strip()
        if not l:
            continue
        t = l.split("\t")
        if len(t) < 2:
            continue
        k = t[0]
        if len(k) != 1 or ord(k) < 128:
            continue
        # v=[  x for x in t[1:]  if valid_ids(x)  ]
        v = t[1:]
        if k == star:
            logger.info(t)
        if v:
            doc.append((k, v))
    logger.info((path, len(doc), random.choice(doc)))
    return doc


def merge():
    doc = []
    doc += readIds()
    doc += readLv2()
    doc += readAll()
    doc += readZixing()

    store = {}
    for k, v in doc:
        if k not in store:
            store[k] = []
        store[k] += v

    doc1 = []
    for k, vs in store.items():
        if k == star:
            R = valid_ids(vs[0])
            logger.info(v)
        v = [x for x in vs if valid_ids(x)]
        v.sort(key=lambda x: (len(x), -sum(ord(x) for x in x[1])))
        if v:
            doc1.append((k, v[0]))

    keys = set(''.join(x[0] for x in doc1))
    values = set(''.join(x[1] for x in doc1))
    logger.info(
        f"keys:{len(keys)} values:{len(values)}  k-v:{len(keys-values)} v-k:{len(values-keys)} {''.join(values-keys)}")

    tgt = "ChaiZi/ChaiZi.txt"
    with open(tgt, "w") as f:
        for k, v in doc1:
            f.write(f"{k}\t{v}\n")

    logger.info((tgt, len(doc1), random.choice(doc1)))

    return store


if __name__ == "__main__":

    logger.info(valid_ids('⿱艹⿳⿲止自巳八夂'))

    store = merge()


"""
[I 230409 23:38:08 idsMerge:178] True
[I 230409 23:38:08 idsMerge:74] ['U+4E4C', '乌', '⿹③一']
[I 230409 23:38:09 idsMerge:77] ('ChaiZi/ids.txt', 83626, ('霳', ['⿱雨隆']))
[I 230409 23:38:09 idsMerge:93] ['乌', '⿱丿⿹#(𠃌㇉^)一(.)']
[I 230409 23:38:09 idsMerge:98] ('ChaiZi/ids_lv2.txt', 93915, ('𮑂', ['⿱艹奢']))
[I 230409 23:38:09 idsMerge:114] ['U+4E4C', '乌', '⿹&CDP-89DE;一']
[I 230409 23:38:10 idsMerge:117] ('ChaiZi/IdsAll.txt', 83168, ('𧛊', ['⿰衤昔']))
[I 230409 23:38:10 idsMerge:135] ['乌', '乌']
[I 230409 23:38:10 idsMerge:138] ('ChaiZi/ZiXing.txt', 89968, ('暀', ['⿰日往']))
[I 230409 23:38:11 idsMerge:164] keys:96638 values:11140  k-v:85770 v-k:272 𢿝卥𠥻ス亞𭂬𠧸𢄉𠧚𠪕丶乀月𠀁𧰨甲曰丐𠄘𠘽歺廌兼𮍌𠕄斗凵𤵶曳𨺅𠄎桌𭣔车𢨋𰀰毋凸
𛂦书𠃊𭭧丿函𢽋㐆𭺛舟占典𠥓𬺷卐𡰣戼𠆢末戊卂卝貞𬻇𡕫𪚾乁𠘧𠚣虍𣦶𰆄㐧𥸦𭙌釒戉丝癶𰀫头𠃉㠭亙𠦑⿱卩水弓𤣩乛然乙飞人廴己之冫𡭔枣爲𭾛卣𥆞𬻞鼠𢑚𧇩女㔽�𠃍⿳⿳辶 
龜𠄌且〇乌丨𠂂丽𠃨丂㠯承臿⿸𫠣贞匚角光𨳇𠃋𦏲止饣𡧧𠖼⿲𠃛𡗫仒卨𭨘臦𨙨艹由乐𪚴𭅰㐁𠣧𦣝当𣦵欠尸飛冉曲巳慶𠀍母𢼾𤴐𡚇𠃎𮠕𧯽α发㣇芻即𦥑𠃌㕟ℓ⿹黽𦥙𭀠𥛓攴𢎘丮𦥓
𭕆上⿺𡖈亅𨤐𠔥𦉭𤊱牜囗𤉷女九𣫬川鹽禹永𣇓刁㐅育冖事𠄏卢⿰东疌虱訁尚豸既齊𠧧熏罒⿶孑𠁁几⿻冂𠙖⿴犭乚厂周𭴺𠧢𪟽𭁈𨈐𮓗〾讠凹卓𮙲㔾尽𤋳𠂆𬺻瓦𭁭𠘨阝⿷コ𠧪勤𠧒
𢊁⿵皮奐扌
[I 230409 23:38:11 idsMerge:172] ('ChaiZi/ChaiZi.txt', 96638, ('𪦥', '⿱絲女'))
"""

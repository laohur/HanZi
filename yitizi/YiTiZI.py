# -*- coding: utf-8 -*-

from logzero import logger

star = '竜'


def choose(doc, YuanZi):
    doc.sort(key=lambda x: (len(x[1]), x[0]))

    doc1=[]
    seen = set()
    for k, v in doc:
        # if k in seen:
        #     logger.warning("key seen "+k)
            # continue
        vs=[ x for x in v if x!=k ]
        vs1=''
        for u in vs[1:]:
            if u in YuanZi:
                logger.warning((k,v,u,"YuanZi"))
                continue
            if u in seen:
                logger.warning((k, v, u, "seen"))
                continue
            seen.add(u)
            vs1+=u
        if vs1:
            doc1.append((k,vs1))
    logger.info((len(doc),len(doc1)))
    return doc1



def get_varriants():
    YuanZi = open("YuanZi/YuanZi.txt").read().splitlines()
    YuanZi = set([x for x in YuanZi if x])

    doc = open('YiTiZi/YiTi.txt').read().splitlines()
    doc = [x.split() for x in doc]
    # doc.sort(key=lambda x: (len(x[1]), x[0]))  # 少数更准确
    doc.sort(key=lambda x: ( x[0],len(x[1])))  # 少数更准确


    # 元字异体
    seen=set()
    doc1=[ (k,v) for k,v in doc if k in YuanZi]
    YuanYiTi = choose(doc1, YuanZi)

    seen = set()
    for k,v in YuanYiTi:
        for x in k+v:
            seen.add(x)

    YiTi = {}
    doc2=[ (k,v) for k,v in doc if k not in YuanZi]
    doc3=choose(doc2,YuanZi)

    YiTiZi = YuanYiTi+doc3

    seen=set()
    varriants = {}
    for k, v in YiTiZi:
        if k in seen:
            exit
        # seen.add(k)
        for u in v:
            if u in seen:
                exit
            if k == u:
                exit
            varriants[u] = k
            seen.add(u)
    print(len(varriants))  # 42514
    chars = list(varriants)
    chars.sort()
    with open("YiTiZi/YiTiZi.txt", 'w') as f:
        for x in chars:
            l = f"{x}\t{varriants[x]}\n"
            f.write(l)


if __name__ == "__main__":
    get_varriants()
    """
[I 220627 00:58:39 YiTiZI:42] (20031, 9354)
27440
    """

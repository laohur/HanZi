from logzero import logger

star = '閵'


def split(dic0, epoch=0):
    dic1 = {}
    for k, v in dic0.items():
        if k == star:
            d = 0
        u = [dic0[x] for x in v]
        u = ''.join(x.strip() for x in u if x)
        dic1[k] = u
    base0 = set(''.join(x for x in dic0.values()))
    base1 = set(''.join(x for x in dic1.values()))
    logger.info((f"epoch:{epoch} base:{len(base0)} --> {len(base1)} "))
    return dic1


def chai(vocab_path, tgt, base_path):

    HeZi = {}

    YiTiZi = open("ChaiZi/ChaiZi.txt").read().splitlines()
    for l in YiTiZi:
        w = l.split('\t')
        if len(w) != 2:
            continue
        k, v = w
        HeZi[k] = v

    JiZi = open(vocab_path).read().splitlines()
    JiZi = [x for x in JiZi if x]
    JiZi = set(JiZi)
    for x in JiZi:
        HeZi[x] = x

    """
    𤍽	𤑔 k,v  异体字\t本体字
    HeZi[𤑔]=HeZi[𤍽] if 𤍽 in 𤑔
    HeZi[v]=HeZi[k] if k in v
    """
    YiTiZi = open("YiTiZi/YiTiZi.txt").read().splitlines()
    YiTiZi = [x.split('\t') for x in YiTiZi]
    for k, v in YiTiZi:
        if k == star:
            d = 0  # '帽'  层次拆字 新构件
            if not k or not v:
                continue
        if v not in HeZi:  # v罕见
            k, v = v, k
        if v not in HeZi:  # v罕见
            logger.warning((k, v))
            continue
        if k in JiZi:
            # v = k
            continue
        if k in HeZi[v]:  # 更细
            HeZi[v] = HeZi[k]
        if v < k and v in HeZi:
            HeZi[k] = HeZi[v]
        elif k in HeZi:
            # logger.info((k, v)
            continue

    dic0 = {k: v for k, v in HeZi.items() if k and v}
    for i in range(5):
        dic1 = split(dic0, i)
        dic0 = dic1

    dic0 = {k: v for k, v in dic0.items() if k and v}

    base0 = list(set(''.join(x for x in dic0.values())))
    base0.sort()
    with open(base_path, "w") as f:
        for x in base0:
            f.write(x+'\n')
    logger.info(''.join(set(base0)-JiZi))  #
    logger.info((JiZi-set(base0)))

    chars = list(dic0)
    chars.sort()
    with open(tgt, "w") as f:
        for x in chars:
            l = f"{x}\t{dic0[x]}"
            f.write(l+'\n')


if __name__ == "__main__":
    chai("JiZi/JiZi.txt", "HeZi/He2Ji.txt", "HeZi/BaseJi.txt")
    chai("YuanZi/YuanZi.txt", "HeZi/He2Yuan.txt", "HeZi/BaseYuanZi.txt")

"""
[I 220622 03:59:07 HeZi:68] 𭔥𬼁𰨇𪛗𭨘𬻞𪛝𰒥𰢷𭣔𰟑䶹ユス𪛙𪛛𰎘𰲞𰀀𪛘
[I 220622 03:59:21 HeZi:68] 𭔥閵𬼁𰨇𪛗𭨘𬻞𪛝𰒥𰢷𭣔𰟑䶹ユス𪛙𪛛藺𰎘𰲞𰀀𪛘
"""

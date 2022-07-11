from logzero import logger

from UnicodeTokenizer import UnicodeTokenizer
import collections

star = '䖵'

"""
    𤍽	𤑔 k,v  异体字\t本体字
    HeZi[𤑔]=HeZi[𤍽] if 𤍽 in 𤑔
    HeZi[v]=HeZi[k] if k in v
异体字 冃	帽
    """


def slim(v):
    if len(v) <= 3:
        return v
    for x in v[1:-1]:
        if x < '⿰' or x > '⿻':
            w = v[0]+x+v[-1]
            return w
    return v


def valid(seq, Ji):
    # s = slim(seq)
    for x in seq:
        if x not in Ji:
            return 0
    return 1


def odd(seq):
    s = slim(seq)
    for x in s:
        if not UnicodeTokenizer.detect_hanzi(x):
            return 1
    return 0


def split(dic0: dict, JiZi: set, YiTi: set, epoch=0):
    dic1 = {}
    for k, v in dic0.items():
        if epoch >= 4 and star in v:
            logger.info((k, v))

        if valid(v, JiZi):
            dic1[k] = v
            continue

        if epoch >= 4:
            if k in YiTi:
                u = YiTi[k]
                u = dic0.get(u, u)
                if valid(u, JiZi):
                    dic1[k] = u
                    continue

        if epoch >= 5:
            u = ''.join(YiTi.get(x, x) for x in v)
            dic1[k] = u
            continue

        u = ''.join(dic0.get(x, x) for x in v)
        dic1[k] = u

    base0 = set(''.join(x for x in dic0.values()))
    base1 = set(''.join(x for x in dic1.values()))
    logger.info((f"epoch:{epoch} base:{len(base0)} --> {len(base1)} "))
    return dic1


def chai(JiZi: set, ChaiZi: list, YiTiZi: list):
    HeZi = {}
    for k, v in ChaiZi:
        if not UnicodeTokenizer.detect_hanzi(k):
            continue
        v = (k if odd(v) else v)
        HeZi[k] = v

    for x in JiZi:
        # if UnicodeTokenizer.detect_hanzi(x):
        HeZi[x] = x

    YiTi = {k: v for k, v in YiTiZi}

    dic0 = HeZi
    for i in range(8):
        dic1 = split(dic0, JiZi, YiTi, epoch=i)
        dic0 = dic1

    dic1 = {}
    giveup = []
    useless = []
    for k, v in dic0.items():
        if UnicodeTokenizer.detect_hanzi(k):
            if valid(v, JiZi):
                dic1[k] = v
            else:
                giveup.append(k)
        else:
            useless.append(k)
    giveup.sort()
    logger.info(f"giveup:{len(giveup)} {''.join(giveup)}")
    logger.info(f"useless:{len(useless)} {''.join(useless)}")

    return dic1


def build(JiZi, ChaiZiPath, YiTiZiPath,  HeZiPath, JiZiPath):
    JiZi = [x for x in JiZi if x]
    JiZi = set(JiZi)

    doc = open(YiTiZiPath).read().splitlines()
    YiTiZi = [x.split('\t') for x in doc]

    doc = open(ChaiZiPath).read().splitlines()
    ChaiZi = [x.split('\t') for x in doc]
    # ChaiZi = [x for x in doc if len(x)==2]
    ChaiZi = [x for x in ChaiZi if UnicodeTokenizer.detect_hanzi(x[0])]

    logger.info(f"JiZi:{len(JiZi)} ChaiZi:{len(ChaiZi)} YiTiZi:{len(YiTiZi)}")
    HeZi = chai(JiZi, ChaiZi, YiTiZi)

    # 剔除冗余基字，管他呢

    Base = set(''.join(slim(x) for x in HeZi.values()))
    logger.info(f"HeZi:{len(HeZi)} Base:{len(Base)} ")
    logger.info(f" useless:{''.join(JiZi-Base)} ")
    diff = Base-JiZi
    logger.info((len(JiZi),  len(diff)))  # (1719, 1719, 0)
    logger.info(''.join(diff))  #
    assert len(diff) == 0

    Base = list(Base)
    Base.sort()
    with open(JiZiPath, "w") as f:
        for x in Base:
            f.write(x+'\n')

    chars = list(HeZi)
    chars.sort()
    with open(HeZiPath, "w") as f:
        for x in chars:
            l = f"{x}\t{HeZi[x]}"
            f.write(l+'\n')

    logger.info(f"HeZi build success -> {HeZiPath}  {JiZiPath}")


if __name__ == "__main__":
    JiZi = open("YuanZi/YuanZi.txt").read().splitlines()
    build(JiZi, ChaiZiPath="ChaiZi/ChaiZi.txt", YiTiZiPath="YiTiZi/YiTiZi.txt",
          HeZiPath="HeZi/He2Yuan.txt", JiZiPath="HeZi/YuanZi.txt")
    JiZi = open("JiZi/JiZi.txt").read().splitlines()
    build(JiZi, ChaiZiPath="ChaiZi/ChaiZi.txt", YiTiZiPath="YiTiZi/YiTiZi.txt",
          HeZiPath="HeZi/He2Ji.txt", JiZiPath="HeZi/JiZi.txt")


"""
sup="候侯𢀖枭島"
[I 220712 04:11:37 He2Zi:123] JiZi:1128 ChaiZi:94235 YiTiZi:27440
[I 220712 04:11:40 He2Zi:70] epoch:0 base:10982 --> 2832 
[I 220712 04:11:41 He2Zi:70] epoch:1 base:2832 --> 1388 
[I 220712 04:11:42 He2Zi:70] epoch:2 base:1388 --> 1346 
[I 220712 04:11:43 He2Zi:70] epoch:3 base:1346 --> 1346 
[I 220712 04:11:43 He2Zi:70] epoch:4 base:1346 --> 1239 
[I 220712 04:11:44 He2Zi:70] epoch:5 base:1239 --> 1232 
[I 220712 04:11:45 He2Zi:70] epoch:6 base:1232 --> 1231 
[I 220712 04:11:45 He2Zi:70] epoch:7 base:1231 --> 1231 
[I 220712 04:11:46 He2Zi:105] giveup:228 㤙㨮㯛䒭䚃兜凫卣叏囙壺嬝嬽岛捣梟篼蔸蟂袅裊逌鄡不女都卑既暑碑署者辶爵𠁧𠁰𠁾𠂣𠂼𠃉𠄏𠇡𠉀𠍋𠎖𠐲𠑹𠑼𠒂𠒎𠕄𠖁𠗦𠝷𠤬𠦁𠧠𠩳𠪕𠬫𠳧𡀮𡆢𡋬
𡏭𡐝𡑩𡕏𡖣𡗒𡙞𡚇𡠿𡭳𡰣𡷊𢆴𢇭𢉺𢉻𢊇𢋵𢍴𢎗𢎜𢎧𢏻𢦐𢦘𢳚𣀨𣀴𣘖𣘛𣚝𣝄𣤝𣤦𣤼𣥒𣪃𣹋𣻴𤂏𤆿𤋅𤒉𤜓𤟨𤤏𤨗𤩤𤰃𥅤𥉼𥛪𥦪𥧻𥸨𦄓𦆚𦈮𦔗𦚀𦣩𦥢𦥫𦥮𦬝𦭢𦮙𦳓𦷿𦺟𧃭𧐳𧒬𧙊𧱊𧳱𨁳𨄭𨒝𨗰𨙃𨛕𨝧𨥻�𨭤𨺅𩓆𩡧𩤷𩮷𪜭𪾏𫑃𫝖𫩦𫸪𫽲𬀘𬂔𬅌𬋢𬔨𬬢𬵈𬻑𬻒𬻘𬻞𬻥𬼂𬼄𬼺𬽡𭁐𭄩𭆴𭇩𭒭𭔥𭖀𭖲𭚡𭜤𭥟𭬍𭬢𭭧𭮴𭱃𭱎𭱐𭱽𭲞��𭴚𭴭𭵄𭾏𮅏𮍇𮍌𮎳𮒮𮓢𮗙𮚊𮡭𮬁𮭹乁凵堍㠯㨮𥚚𰅜𰒥𰗧𰙌𰨇𰲞𰳞𰷾�
[I 220712 04:11:46 He2Zi:106] useless:0
[I 220712 04:11:47 He2Zi:129] HeZi:94059 Base:1128 
[I 220712 04:11:47 He2Zi:130]  useless:
[I 220712 04:11:47 He2Zi:132] (1128, 0)
[I 220712 04:11:47 He2Zi:133]
[I 220712 04:11:47 He2Zi:149] HeZi build success -> HeZi/He2Yuan.txt  HeZi/YuanZi.txt
[I 220712 04:11:47 He2Zi:123] JiZi:9797 ChaiZi:94235 YiTiZi:27440
[I 220712 04:11:51 He2Zi:70] epoch:0 base:15554 --> 10490 
[I 220712 04:11:51 He2Zi:70] epoch:1 base:10490 --> 9982 
[I 220712 04:11:52 He2Zi:70] epoch:2 base:9982 --> 9977 
[I 220712 04:11:53 He2Zi:70] epoch:3 base:9977 --> 9977 
[I 220712 04:11:53 He2Zi:70] epoch:4 base:9977 --> 9869 
[I 220712 04:11:54 He2Zi:70] epoch:5 base:9869 --> 9863 
[I 220712 04:11:55 He2Zi:70] epoch:6 base:9863 --> 9862 
[I 220712 04:11:55 He2Zi:70] epoch:7 base:9862 --> 9862 
[I 220712 04:11:56 He2Zi:105] giveup:130 㤙䒭叏囙嬽不女爵𠄏𠇡𠉀𠍋𠎖𠐲𠑼𠖁𠗦𠝷𠩳𠪕𠬫𠳧𡆢𡋬𡐝𡖣𡙞𡚇𡭳𢆴𢇭𢉺𢉻𢊇𢋵𢍴𢏻𢦘𣀨𣀴𣝄𣤝𣤼𣥒𤂏𤆿𤒉𤜓𤟨𤤏𥅤𥛪𥦪𥧻𦔗𦚀𦣩𦥢𦬝𦮙𦳓𧃭𧐳𧙊
𧱊𧳱𨁳𨄭𨒝𨝧𨥻𨬀𨭤𨺅𩡧𩤷𪜭𫑃𫸪𬅌𬋢𬔨𬬢𬵈𬻑𬻘𬻞𬻥𭁐𭄩𭆴𭇩𭒭𭔥𭖀𭖲𭚡𭜤𭥟𭬍𭬢𭭧𭮴𭱃𭱎𭱐𭱽𭲞𭵄𮅏𮍇𮎳𮒮𮓢𮗙𮚊𮡭𮬁𮭹乁凵㠯㨮𥚚𰅜𰒥𰙌𰨇𰲞𰷾
[I 220712 04:11:56 He2Zi:106] useless:0
[I 220712 04:11:56 He2Zi:129] HeZi:94296 Base:9797 
[I 220712 04:11:56 He2Zi:130]  useless:
[I 220712 04:11:56 He2Zi:132] (9797, 0)
[I 220712 04:11:56 He2Zi:133]
[I 220712 04:11:57 He2Zi:149] HeZi build success -> HeZi/He2Ji.txt  HeZi/JiZi.txt
"""

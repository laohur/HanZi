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
        # if epoch >= 4 and star in v:
        #     logger.info((k, v))

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
    JiZi = open("ChaiZi/GouJian.txt").read().splitlines()
    build(JiZi, ChaiZiPath="ChaiZi/ChaiZi.txt", YiTiZiPath="YiTiZi/YiTiZi.txt",
          HeZiPath="HeZi/He2Ji.txt", JiZiPath="HeZi/JiZi.txt")


"""
sup="候侯𢀖枭島"
[I 220713 02:06:47 He2Zi:123] JiZi:1128 ChaiZi:94235 YiTiZi:27440
[I 220713 02:06:49 He2Zi:70] epoch:0 base:10774 --> 2752 
[I 220713 02:06:50 He2Zi:70] epoch:1 base:2752 --> 1355 
[I 220713 02:06:50 He2Zi:70] epoch:2 base:1355 --> 1313 
[I 220713 02:06:51 He2Zi:70] epoch:3 base:1313 --> 1313 
[I 220713 02:06:51 He2Zi:70] epoch:4 base:1313 --> 1273 
[I 220713 02:06:52 He2Zi:70] epoch:5 base:1273 --> 1269 
[I 220713 02:06:52 He2Zi:70] epoch:6 base:1269 --> 1269 
[I 220713 02:06:53 He2Zi:70] epoch:7 base:1269 --> 1269 
[I 220713 02:06:53 He2Zi:105] giveup:465 㕽㤙㨮㯛䅮䌲䒭䗼䙧䚃䢢䤌以似倉傖兜凔凫卣嗆嚑囙场壺姒娰嬝嬽岛嵢愴戧扬拟拣捣搶旸曛杨梟槍殇汤泤滄炀炼烫熏熗燻爋牄獊獯玚瑲畅疡瘡矄砀笖篬篼纁练肠臐艙
苡荡蒼蔸薰蘍螥蟂袅裊觞謒賶蹌逌鄡醺鉯鑂钖铴飏饧鶬不女都卑既暑碑署者辶爵𠀀𠀈𠀉𠀌𠀍𠀑𠀟𠀳𠁣𠁦𠁧𠁩𠁰𠁱𠁾𠂀𠂂𠂍𠂣𠂼𠃉𠃓𠃢𠄏𠄓𠄙𠇡𠉀𠍋𠎖𠏧𠏳�𠑜𠑹𠑼𠒂𠒎𠕄𠖁𠙧𠚒𠛖𠝎𠠈𠤬𠥃𠥐𠥻𠦁𠧠𠨝𠩳𠬫𠳎𠳧𡀮��𡆢𡆵𡋬𡏭𡐝𡑩𡒝𡓕𡓽𡕏𡖣𡗒𡚇𡚎𡜏𡠿𡤂𡭳𡯁𡰣𡰴𡳿𡷊𡸁𡼻𢁹𢁺𢆴𢉺𢊇𢋵𢌰𢍴𢎗𢎜𢎧𢎱𢏻𢜁𢣤𢦐𢦘𢮮𢳚𢷠𣀨𣀴𣅲𣋃��𣎰𣒚𣘖𣘛𣝄𣢔𣤝𣤦𣥒𣦶𣪃𣫬𣯙𣴁𤂏𤋅𤏬𤐁𤑕𤒉𤓂𤘍𤚬𤜓𤤃𤤳𤦓𤦡𤨗𤩤𤪠𤰃𤸣𥃅𥄤𥅤𥆞𥉼𥏲𥙩𥪈𥴻�𥵯𥸨𥻲𦃹𦄓𦆚𦇟𦈮𦉭𦋦𦜸𦞛𦢁𦣩𦥒𦥫𦥺𦧀𦨃𦫯𦫵𦭢𦭩𦲿𦷿𦺟𦼃𧃭𧒬𧙊𧰣𧰾𧱊𧳱𧽜𨈏𨈐𨈑𨒝𨔍𨗰𨙃𨙡𨛕𨜾𨭤𨮤𨳇𨳈𨶆𨷒𨷔𨺅𨺪𩂚𩇦𩇧𩇨𩕹𩙱𩝞𩪱𩮩𩮷𩰊𩰋𪇑𪈧𪓕𪓝𪙎𪚦𪛉𪛙𪜀𪜭𪟮𪤇𪦔𪰻𪼧𪾏𫀞𫄸𫈄𫚊𫝖𫠣𫠪𫡆𫣵𫤤�𫲊𫵵𫸪𫼟𫽲𫾙𬀘𬂱𬅌𬅑𬋢𬍡𬐂𬐠𬒃𬓸𬔎𬚤𬛹𬟝𬟾𬠊𬡧𬦅𬦏𬫤𬬡𬬢𬰌𬲰𬵈𬺷𬺻𬻆𬻒𬻘𬻴𬼂𬼄𬼘𬼺𬽡𬿠𬿿𭂄𭂸𭂺𭆴𭇩��𭔈𭔥𭖀𭖲𭙪𭚡𭜤𭞶𭟇𭣔𭣚𭥟𭨘𭬍𭬝𭬢𭭧𭭪𭮴𭯸𭱎𭱐𭱽𭲞𭲰𭳄𭳵𭴭𭵄𭸳𭺪𭾊𭾏𮅏𮍌𮍠𮎳𮒮𮓢𮖥𮗙𮚊�𮛸𮠕𮡭𮭹乁㠯㨮𰀤𰅜𰆶𰑓𰒥𰓋𰗧𰙌𰝔𰤓𰧕𰨇𰰢𰲞𰷟𱁱
[I 220713 02:06:53 He2Zi:106] useless:0
[I 220713 02:06:54 He2Zi:129] HeZi:93822 Base:1128 
[I 220713 02:06:54 He2Zi:130]  useless:
[I 220713 02:06:54 He2Zi:132] (1128, 0)
[I 220713 02:06:54 He2Zi:133]
[I 220713 02:06:54 He2Zi:149] HeZi build success -> HeZi/He2Yuan.txt  HeZi/YuanZi.txt
[I 220713 02:06:54 He2Zi:123] JiZi:2365 ChaiZi:94235 YiTiZi:27440
[I 220713 02:06:56 He2Zi:70] epoch:0 base:10720 --> 3254 
[I 220713 02:06:56 He2Zi:70] epoch:1 base:3254 --> 2894 
[I 220713 02:06:56 He2Zi:70] epoch:2 base:2894 --> 2893 
[I 220713 02:06:57 He2Zi:70] epoch:3 base:2893 --> 2893 
[I 220713 02:06:57 He2Zi:70] epoch:4 base:2893 --> 2853 
[I 220713 02:06:58 He2Zi:70] epoch:5 base:2853 --> 2849 
[I 220713 02:06:58 He2Zi:70] epoch:6 base:2849 --> 2849 
[I 220713 02:06:58 He2Zi:70] epoch:7 base:2849 --> 2849 
[I 220713 02:06:59 He2Zi:105] giveup:541 ⺁⺂⺃⺅⺇⺉⺋⺍⺎⺏⺐⺑⺒⺓⺔⺖⺗⺘⺙⺛⺜⺞⺟⺠⺡⺢⺣⺤⺥⺦⺧⺨⺩⺪⺫⺬⺭⺮⺯⺰⺱⺲⺳⺴⺵⺶⺷⺹⺺⺽⺾⺿⻀⻁⻂⻃⻄⻅⻆⻇⻈⻉⻊⻋⻌⻍⻎⻏⻐⻑⻒⻓
⻔⻕⻖⻗⻘⻙⻚⻛⻜⻝⻞⻟⻠⻡⻢⻣⻤⻥⻦⻧⻨⻩⻪⻫⻬⻭⻮⻯⻰⻱⻲⻳⼀⼁⼂⼃⼄⼅⼆⼇⼈⼉⼊⼋⼌⼍⼎⼏⼐⼑⼒⼓⼔⼕⼖⼗⼘⼙⼚⼛⼜⼝⼞⼟⼠⼡⼢⼣⼤⼥⼦⼧⼨⼩⼪⼫⼬⼭⼮⼯⼰⼱⼲⼳⼴⼵⼶⼷⼸⼹⼺⼻ 
⼼⼽⼾⼿⽀⽁⽂⽃⽄⽅⽆⽇⽈⽉⽊⽋⽌⽍⽎⽏⽐⽑⽒⽓⽔⽕⽖⽗⽘⽙⽚⽛⽜⽝⽞⽟⽠⽡⽢⽣⽤⽥⽦⽧⽨⽩⽪⽫⽬⽭⽮⽯⽰⽱⽲⽳⽴⽵⽶⽷⽸⽹⽺⽻⽼⽽⽾⽿⾀⾁⾂⾃⾄⾅⾆⾇⾈⾉⾊⾋⾌⾍⾎⾏⾐⾑⾒⾓⾔⾕⾖⾗ 
⾘⾙⾚⾛⾜⾝⾞⾟⾠⾡⾢⾣⾤⾥⾦⾧⾨⾩⾪⾫⾬⾭⾮⾯⾰⾱⾲⾳⾴⾵⾶⾷⾸⾹⾺⾻⾼⾽⾾⾿⿀⿁⿂⿃⿄⿅⿆⿇⿈⿉⿊⿋⿌⿍⿎⿏⿐⿑⿒⿓⿔⿕〇㇀㇃㇅㇆㇊㇋㇌㇍㇎㇏㇐㇑㇒㇔㇕㇖㇗㇘㇙㇚㇛㇜㇝㇞㇟㇠㇡㇢㇣ 
㐃㐆㐧㔔㪳㫈䍏乁乄书亊亪円凫卍卐嬝嬽孒孓岛捣曱枭袅裊不女卑既碑辶爵𠀀𠀈𠀌𠀍𠀑𠀟𠁢𠁦𠁧𠁩𠁰𠁱𠁾𠂀𠂂𠂍𠂣𠂼𠃉𠃛𠃢𠄏𠄓𠄙𠑹𠑼𠒂𠒎𠕄𠖁𠙴𠝎𠤬�𠥻𠦁𠩳𠳧𡀮𡆢𡆵𡋬𡑩𡗒𡚇𡜏𡭔𡭳𡯁𡰴𡳿𡷊𢁺𢆴𢌰𢍴𢎗𢎜𢎧��𢏻𢦐𢩯𢩴𢮮𣀴𣅲𣒚𣗭𣤝𣥒𣦶𣫬𣴁𤐁𤘍𤜓𤤃𤦡𤰃𤽆𥃅𥆞𥝌𥸨𦆚𦉭𦣵𦤄𦥒𦥫𦥺𦨃𦫵𦭩𦱫𧺐𨈏𨈐𨈑𨳇𨳈𩂚𩇦𩇧𩇨𩙱𩰊𩰋��𪓝𪚦𪛉𪛙𪛛𪭣𫇧𫝖𫩦𫽐𫽲𬇼𬫬𬺷𬻆𬻘𬼁𬼂𬼄𬼘𬼺𬽡𭅫𭇩𭔥𭖀𭖲𭚡𭣔𭣚𭥟𭨘𭬢𭮱𭮴𭱐𭱽𭲰𭳄𭺪𮍠𮎳�𮒮𮠕乁㠯𰁈𰑓𰒥𰨇
[I 220713 02:06:59 He2Zi:106] useless:8 ③？コ↔↷⑦ユ④
[I 220713 02:06:59 He2Zi:129] HeZi:93706 Base:2357 
[I 220713 02:06:59 He2Zi:130]  useless:コ③ユ↔？↷④⑦
[I 220713 02:06:59 He2Zi:132] (2365, 0)
[I 220713 02:06:59 He2Zi:133]
[I 220713 02:06:59 He2Zi:149] HeZi build success -> HeZi/He2Ji.txt  HeZi/JiZi.txt
"""

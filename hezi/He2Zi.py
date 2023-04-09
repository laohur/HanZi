# -*- coding: utf-8 -*-

from logzero import logger

star = '䖵'

"""
    𤍽	𤑔 k,v  异体字\t本体字
    HeZi[𤑔]=HeZi[𤍽] if 𤍽 in 𤑔
    HeZi[v]=HeZi[k] if k in v
异体字 冃	帽
    """
JieGou = "〾⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻"

def valid(seq, Ji):
    for x in seq:
        if x not in Ji:
            return 0
    return 1

def split(dic0: dict, JiZi: set,  epoch=0):
    dic1 = {}
    for k, v in dic0.items():
        if valid(v, JiZi):
            dic1[k] = v
        else:
            u = ''.join(dic0.get(x, x) for x in v)
            dic1[k] = u

    base0 = set(''.join(x for x in dic0.values()))
    base1 = set(''.join(x for x in dic1.values()))
    logger.info((f"epoch:{epoch} base:{len(base0)} --> {len(base1)} "))
    return dic1


def chai(JiZi: set, ChaiZi: list, YiTi:dict):
    HeZi = {}
    for k, v in ChaiZi:
        if k in JiZi:
            HeZi[k] = k
        elif k in YiTi and YiTi[k] in JiZi:
            HeZi[k] =  YiTi[k] 
        else:
            HeZi[k] = v

    dic0 = HeZi
    for i in range(4):
        dic1 = split(dic0, JiZi, epoch=i)
        dic0 = dic1

    dic1 = {}
    giveup = []
    useless = []
    for k, v in dic0.items():
        if ord(k)>10000:
            if valid(v, JiZi):
                dic1[k] = v
            else:
                giveup.append(k)
        else:
            useless.append(k)
    giveup.sort()
    logger.info(f"giveup v:{len(giveup)} {''.join(giveup)[:1000]}")
    logger.info(f"useless k:{len(useless)} {''.join(useless)[:1000]}")
    return dic1


def build(JiZi, ChaiZiPath, YiTiZiPath,  HeZiPath, JiZiPath):
    JiZi = [x for x in JiZi if x]
    JiZi = set(JiZi)

    doc = open(YiTiZiPath).read().splitlines()
    YiTiZi = [x.split('\t') for x in doc]
    YiTiZi={k:v for k,v in YiTiZi}

    doc = open(ChaiZiPath).read().splitlines()
    ChaiZi = [x.split('\t') for x in doc]

    logger.info(f"JiZi:{len(JiZi)} ChaiZi:{len(ChaiZi)} YiTiZi:{len(YiTiZi)}")
    HeZi = chai(JiZi, ChaiZi, YiTiZi)

    Base = set(''.join(x for x in HeZi.values()))
    logger.info(f"HeZi:{len(HeZi)} Base:{len(Base)} ")

    logger.info(f" JiZi-Base: {len(JiZi-Base)} {''.join(JiZi-Base)[:1000]} ")
    diff = Base-JiZi
    logger.info(f"Base-JiZi:{len(diff)}  {''.join(diff)[:1000]}")
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
    JiZi = open("ZiGen/ZiGen.txt").read().splitlines()
    build(JiZi, ChaiZiPath="ChaiZi/ChaiZi.txt", YiTiZiPath="YiTiZi/YiTiZi.txt",
          HeZiPath="HeZi/He2ZiGen.txt", JiZiPath="HeZi/ZiGen.txt")
    # JiZi = open("ChaiZi/GouJian.txt").read().splitlines()
    # build(JiZi, ChaiZiPath="ChaiZi/ChaiZi.txt", YiTiZiPath="YiTiZi/YiTiZi.txt",
    #       HeZiPath="HeZi/He2Ji.txt", JiZiPath="HeZi/JiZi.txt")


"""
[I 230410 01:07:38 He2Zi:79] JiZi:1043 ChaiZi:96638 YiTiZi:24237
[I 230410 01:07:39 He2Zi:32] epoch:0 base:11180 --> 2566 
[I 230410 01:07:39 He2Zi:32] epoch:1 base:2566 --> 1082 
[I 230410 01:07:39 He2Zi:32] epoch:2 base:1082 --> 1037 
[I 230410 01:07:39 He2Zi:32] epoch:3 base:1037 --> 1037 
[I 230410 01:07:39 He2Zi:63] giveup v:1410 ⺕㑳㒄㒯㓠㓥㕡㕢㗙㘢㚲㜣㞡㠟㣌㤐㤙㥈㥎㥮㦓㦸㨪㪕㪫㪱㫇㫈㬇㬗㮚㮲㰀㱀㲃㷹㸃㹰㹿㼭㽕㿛㿠䀡䁜䂽䅳䆪䇖䈇䈛䉫䊍䍄
䐢䑲䑼䓬䔳䕻䖿䚕䛸䜜䜭䝲䡠䦓䨔䩇䩞䪓䪥䪮䬯䮓䯑䳿䴴䴻䵿乩乻佔侊侦侭倬偵儷兤剓叡呫咝咣唢唹啅喚嘫嚟嚸囇囙坫垆垙垱壑壡奌姯婥婯媜媰嬽孋寊寏尡岾帖帧幀幌店廲彲
怗恍悼惉惦愌愰战扂扵拈挄挡掂掉揁換搊撚攦敁敹於旕晃晄晫曬枮栆栌桄桢档梷棃棜棹楨榥槕橪檆櫦欐毡沾泸洸浈浕淖淤渙湞滉濬灑炶点烬焯煔煥煼熀燃燛犂犓玷珖珰琐琸瑍
璿瓈痁瘀瘓皝皩皺睝睿矖砧硄碵祯禎秥穲窧站竨笘筜箊篘籭粘絖綽緽縐縨繎繛纚绰罩羄羻耀胋胪胱臩舻苫茪荩菞菸萜蒧蒭蔾藜蛅袩裆襹覘觇觥詀謅貼贴赆赪赬趈趠趨跕踔踮蹨
躧輄輝轳辉迠逴遉邌邐鄒酈酟釃鉆銧鋽錅鍞鎤鑗钻铛锁閼阏阽雛霑靗韑頕颅颭飐駫騶驪鮎鯬鯲鯴鱺鲇鲈鲺鵫鵹鶵鸝鸬鸶麗黇黋黎黏點黧齺龼驪麗黎撚禎節𠁅𠁲𠁵𠃵𠈎𠈑𠉝𠌩𠏊
𠏻𠐲𠒗𠒝𠒡𠒥𠒦𠒪𠒫𠒬𠒵𠒸𠒼𠒽𠒿𠓁𠓂𠓃𠓅𠓇𠓉𠓊𠓋𠓌𠓐𠓑𠓒𠓓𠓖𠓚𠕟𠕭𠗀𠗁𠗫𠘍𠙚𠚱𠛤𠛾𠜷𠞃𠟫𠟮𠠍𠠫𠡴𠣱𠣳𠣿𠥛𠥳𠦲𠦷𠦺𠧄𠧇𠧰𠧴𠧵𠧺𠧾𠨋𠪳𠭹𠮔𠮤𠰷𠰸𠱨𠵁𠵗𠵰𠶁𠶧𠶵
𠸞𠸩𠸿𠹘𠻔𠾆𡁇𡁿𡂻𡆢𡋤𡌐𡌓𡌧𡌽𡍎𡍏𡎞𡎱𡏶𡑋𡓝𡔂𡔉𡕽𡖞𡖡𡖣𡖵𡗭𡙉𡙞𡙦𡚄𡚥𡛸𡝫𡞵𡣣𡥧𡦅𡧑𡪝𡪥𡫟𡫳𡫼𡮫𡯴𡱇𡱘𡴰𡵊𡵋𡷀𡺌𡾡𢀾𢁞𢆴𢇒𢋁𢋟𢎙𢐨𢒛𢒟𢒢𢒪𢓕𢓥𢔄𢔤𢙦𢛂𢛈
𢛨𢜋𢝭𢢙𢤂𢤑𢤧𢥛𢥜𢥬𢦻𢧗𢧪𢩊𢩶𢪀𢪜𢫘𢮁𢮃𢮸𢰯𢰷𢴃𢵚𢹤𢻛𢼯𢼴𢽆𢽭𢾃𢾓𢾨𢿡𢿭𢿶𣀨𣀷𣂢𣂣𣃲𣃶𣃷𣄒𣄙𣆐𣆤𣆥𣈔𣈘𣉵𣊸𣍊𣍽𣎀𣐗𣗴𣛔𣡃𣡶𣡷𣡼𣢤𣣧𣣸𣦓𣦖𣦻𣨝𣨦𣩚𣪙𣫋𣫜𣭥
𣮋𣰂𣰮𣰿𣱄𣲁𣴸𣶓𣷀𣸎𣸾𣺥𣻶𣽊𣿚𣿤𤂈𤂏𤂱𤂷𤃒𤅳𤅸𤇀𤇆𤇻𤈛𤉋𤉪𤉽𤊁𤊪𤋒𤋧𤋺𤌉𤌽𤎆𤎉𤏑𤑬𤑰𤑵𤒉𤒓𤓛𤓧𤓫𤕂𤖄𤖊𤘇𤙴𤚙𤚷𤛃𤛼𤛿𤜛𤜩𤝓𤞁𤠮𤡞𤡮𤢅𤤨𤥽𤦥𤦹𤨆𤩅𤩞𤩡𤩰𤪇
𤪎𤫀𤫟𤭜𤭥𤱳𤲤𤳿𤴗𤴘𤵵𤶏𤷘𤸘𤺱𤽗𤾗𥂂𥃅𥃐𥅤𥆄𥇍𥇞𥈉𥊶𥋽𥌑𥌛𥍄𥍕𥎁𥏥𥕫𥗍𥗷𥙑𥛡𥜨𥜰𥝢𥝨𥟖𥟫𥠅𥠖𥠯𥡎𥢅𥢆𥢔𥢯𥣥𥣵𥣹𥤟𥦺𥧻𥨹𥪥𥭔𥮒𥮠𥮸𥯎𥱱𥲖𥳚𥴄𥴐𥴙𥵙𥵤𥶈𥸗𥹄
𥹥𥺦𥻆𥻤𥼡𥽝𥽽𥾄𥾪𥿕𦁦𦁨𦄹𦅕𦇊𦊫𦋇𦋐𦋚𦌿𦏧𦒉𦒻𦒾𦓪𦕒𦕤𦖥𦘐𦘸𦚌𦚯𦜰𦝝𦝿𦞔𦟶𦠰𦡿𦣩𦥰𦥿𦨻𦬿𦮵𦰈𦱥𦳋𦵄𦵵𦵽𦷕𦷙𦷝𦹫𦺙𦺩𦻐𦻛𦽗𦾗𦿥𦿺𧃁𧅏𧇲𧇺𧋅𧌡𧌸𧍈𧎑𧎷𧐼𧑇𧒢
𧓣𧔌𧕯𧖉𧗯𧗽𧙊𧚩𧛸𧝑𧝣𧡑𧡹𧣺𧥑𧥖𧧯𧨳𧨼𧪊𧮪𧮷𧯕𧲸𧳝𧳹𧴇𧵦𧶃𧶸𧷁𧷎𧹍𧾝𧾩𨃊𨃘𨄵𨉁𨉔𨋤𨌬𨎆𨏆𨏽𨐈𨒺𨔁𨔆𨔟𨖏𨗋𨘯𨘵𨛄𨛜𨛫𨛹𨜓𨞠𨞰𨟀𨠵𨤎𨤒𨦸𨨈𨨡𨩉𨪕𨬀𨬏𨮠𨯙𨰣𨱬
𨵍𨵣𨷽𨹂𨺑𨺟𨻙𨼱𨽄𨽝𨽡𨽩𨽴𨽵𨿧𨿯𨿾𩁟𩄷𩅎𩇓𩉄𩉟𩊠𩌄𩌓𩎉𩐣𩒚𩖝𩘀𩙩𩚋𩜏𩝆𩢬𩤎𩦄𩦅𩧋𩧝𩧠𩩘𩩦𩬑𩭂𩭟𩱈𩱦𩲦𩳁𩳨𩳩𩵿𩶸𩷹𩸢𩹰𩺋𩺥𩻳𩼽𩾤𩿮𪀄𪀯𪂱𪄞𪆈𪇺𪈳𪉜𪋨𪋭𪍆𪍈
𪍕𪎋𪎪𪏯𪐅𪐇𪑳𪒺𪕐𪕓𪕗𪕾𪖚𪗚𪗦𪘫𪙗𪙚𪜭𪝚𪝽𪞀𪞃𪞆𪞟𪞲𪟂𪟷𪟿𪠀𪠽𪡦𪡽𪣷
[I 230410 01:07:39 He2Zi:64] useless k:0 
[I 230410 01:07:39 He2Zi:83] HeZi:95228 Base:941 
[I 230410 01:07:39 He2Zi:85]  JiZi-Base: 102 𬻆㇍𠁢㇉𠂀𬻫𫞓曱𬂛𭺛亊𦫵㇡㇑𦥮㇂㇥𬼘𢎧㇗㇝𠄙㇠𡗾𪚦𠀀㐃𭴚㇪㇭㇔⿾𠁾㇆乄㇩𬻒㇧𫝖𦥺𪓝𠙴㇏⿿㇄𤦡𢎗㇕㇘𠁧𠁘㇙𬼂
㇛㇟㇅㇢𤰃𩇧㇌⿽㇁𭐳㇜𠂣㇊㇒⿼𬼄㇫㇎㇃𪛉㇓㇐㇚𠀑𠀟㇣㇈𢎜㇯㇦卍𠤬辶𠃢㇮㇇㇖㇨㇬𠁰㇀𫞪𠁱㇋㇞𫬯𦥫㇤𠀈
[I 230410 01:07:39 He2Zi:87] Base-JiZi:0
[I 230410 01:07:40 He2Zi:103] HeZi build success -> HeZi/He2ZiGen.txt  HeZi/ZiGen.txt
"""

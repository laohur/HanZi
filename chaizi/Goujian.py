import collections
from logzero import logger


JieGou = "〾⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻"
JieGou2 = "⿰⿱⿴⿵⿶⿷⿸⿹⿺⿻"
JieGou3 = "⿲⿳"

stars2 = '𛂦𠦮𡋬𡰣𢚎𤣩𨪐𬼂𬼄𭔥乁𰀁'
star = stars2[0]

path = "ChaiZi/ChaiZi.txt"
doc = open(path).read().splitlines()
doc = [x.split('\t') for x in doc]
ids = {k: v for k, v in doc}


isolate = ''.join(k for k, v in ids.items()
                  if not v or k == v and ord(k)>10000)
logger.info(("isolate", len(isolate), ''.join(isolate)))


def automic(dic0, base):
    for x in base:
        dic0[x] = x
    dic1 = {}
    for k, v in dic0.items():
        u = ''.join(dic0.get(x, x) for x in v)
        dic1[k] = u
    return dic1


def get_hot(dic0, min_freq=500):
    values = ''.join(dic0.values())
    freq = collections.Counter(values)
    hot = [k for k in freq if freq[k] >= min_freq]
    logger.info((len(hot), ''.join(hot)))
    return hot


dic0 = {k: v for k, v in ids.items()}
base = set()


def slim(dic0, base, min_freq=2):
    hot = get_hot(dic0, min_freq)
    # base = set(isolate) | set(hot)
    base1 = base | set(hot)
    dic1 = automic(dic0, base1)
    logger.info(f"{len(base)} -> {len(base1)}")
    return dic1, base1


logger.info(f"epoch:{0}")
dic1, base = slim(dic0, base, 10)

logger.info(f"epoch:{1}")
dic2, base = slim(dic1, base, 5)

values = ''.join(dic2.values())
freq = collections.Counter(values)

giveup = [k for k, v in freq.items() if v <= 4]
giveup.sort()
logger.info((f"giveup {len(giveup)}", ''.join(giveup)))

GouJianFreq = [(k, v) for k, v in freq.items()]
GouJianFreq.sort(key=lambda x: (-x[1], x[0]))
with open("ChaiZi/GouJianFreq.tsv", 'w') as f:
    for k, v in GouJianFreq:
        f.write(f"{k}\t{v}"+'\n')

GouJian = [x[0] for x in GouJianFreq if x[1] >=5 ]
GouJian.sort()
with open("ChaiZi/GouJian.txt", 'w') as f:
    for x in GouJian:
        f.write(x+'\n')

"""
[I 220713 02:05:41 Goujian:22] ('isolate', 764, '⺁⺂⺃⺄⺅⺆⺇⺉⺋⺌⺍⺎⺏⺐⺑⺒⺓⺔⺖⺗⺘⺙⺛⺜⺞⺟⺠⺡⺢⺣⺤⺥⺦⺧⺨⺩⺪⺫⺬⺭⺮⺯⺰⺱⺲⺳⺴⺵⺶⺷⺹⺺⺽⺾⺿⻀⻁⻂⻃⻄⻅⻆⻇⻈⻉⻊⻋⻌
⻍⻎⻏⻐⻑⻒⻓⻔⻕⻖⻗⻘⻙⻚⻛⻜⻝⻞⻟⻠⻡⻢⻣⻤⻥⻦⻧⻨⻩⻪⻫⻬⻭⻮⻯⻰⻱⻲⻳⼀⼁⼂⼃⼄⼅⼆⼇⼈⼉⼊⼋⼌⼍⼎⼏⼐⼑⼒⼓⼔⼕⼖⼗⼘⼙⼚⼛⼜⼝⼞⼟⼠⼡⼢⼣⼤⼥⼦⼧⼨⼩⼪⼫⼬⼭⼮⼯⼰⼱⼲⼳⼴ 
⼵⼶⼷⼸⼹⼺⼻⼼⼽⼾⼿⽀⽁⽂⽃⽄⽅⽆⽇⽈⽉⽊⽋⽌⽍⽎⽏⽐⽑⽒⽓⽔⽕⽖⽗⽘⽙⽚⽛⽜⽝⽞⽟⽠⽡⽢⽣⽤⽥⽦⽧⽨⽩⽪⽫⽬⽭⽮⽯⽰⽱⽲⽳⽴⽵⽶⽷⽸⽹⽺⽻⽼⽽⽾⽿⾀⾁⾂⾃⾄⾅⾆⾇⾈⾉⾊⾋⾌⾍⾎⾏⾐ 
⾑⾒⾓⾔⾕⾖⾗⾘⾙⾚⾛⾜⾝⾞⾟⾠⾡⾢⾣⾤⾥⾦⾧⾨⾩⾪⾫⾬⾭⾮⾯⾰⾱⾲⾳⾴⾵⾶⾷⾸⾹⾺⾻⾼⾽⾾⾿⿀⿁⿂⿃⿄⿅⿆⿇⿈⿉⿊⿋⿌⿍⿎⿏⿐⿑⿒⿓⿔⿕〇㇀㇁㇂㇃㇄㇅㇆㇇㇈㇉㇊㇋㇌㇍㇎㇏㇐㇑㇒㇓㇔㇕ 
㇖㇗㇘㇙㇚㇛㇜㇝㇞㇟㇠㇡㇢㇣㐁㐃㐄㐅㐆㐧㔾㠯㸦䍏一丈丏丐丑专且世丘东丣严丨丩丬丱丶丷丹为丿乀乁乄久之乌乍乎乐乑乗乙乚乛乜九也乡书亅亊事于井亜亞人亻以兂兆兜入八冂円冉册冖冘冫几凵凸凹刂勹 
匚匸十卌卍卐卜卝卩厂厶又及发口史囗夂夊央头女子孑孒孓宀寸小尢尸尺山川州工巨己已巳巴巾干年广廴廿弓彐彑彡彳心忄戉戊我戼手扌才承攵斗旡日曰曱曲曳月木朩未末本朱朿束来東柬欠止毋毌母比氏民氵永 
灬為熏爪爲爿片牙牛牜犬犭瓜瓦甘生田由甲申疋疌疒白皮皿目示礻禹禺米粛纟缶罒耂耳肃肅肉臣自臼舟艮虍虫衤襾见角言訁讠谷豆豸贝身車车辶酉重釒钅长门阝隶隹非革韦頁页飛飞饣黽齿龜龰龴龵龶車龜龜丹女 
年卑既者艹辶華龜𠀀𠀈𠀉𠀌𠀍𠀑𠀟𠁁𠁣𠁦𠁧𠁩𠁰𠁱𠁾𠂀𠂂𠂆𠂇𠂉𠂍𠂎𠂒𠂣𠂼𠃉𠃊𠃋𠃌𠃍𠃎𠃑𠃓𠃛𠃜𠃢𠄌𠄎𠄓𠄙𠆢𠑹𠕄𠘧𠘨𠙴𠚒𠤬𠥓𠥻𠦁𠦑𡆵𡗒𡦹𡭔𡯁𡰣𡰴𡳿𡸁𡿨𢀓𢁺𢎗𢎜𢎧𢎱𢑚𣅲𣎳𣎵𣒚𣥂𣦶𣫬𤓰𤕪𤣩𤦡𤰃𤴔𥆞𥘅�𥫗𥸨𦉭𦣝𦣞𦥒𦥫𦥺𦫵𧘇𧰨𨈏𨈐𨈑𨳇𨸏𩇦𩇧𩇨𩙱𩙿𩰊𩰋𪓕𪓝𪚦𪚴𪛉𪛙𪜀𫝀𫝖𫠣𬺷𬺻𬻆𬼂𬼄𬼘𭕄𭣔𭨘𭺪𮍌𮎳𮠕乁北卑��㠯'')

[I 220713 02:05:41 Goujian:56] epoch:0
[I 220713 02:05:41 Goujian:39] (2262, 

[I 220713 02:05:41 Goujian:52] 0 -> 2262
[I 220713 02:05:41 Goujian:59] epoch:1
[I 220713 02:05:41 Goujian:39] (2365,

[I 220713 02:05:42 Goujian:52] 2262 -> 2365
[I 220713 02:05:42 Goujian:67] ('giveup 475', '①②⑤⑥⑧⑩⺁⺂⺃⺅⺇⺉⺋⺍⺎⺏⺐⺑⺒⺓⺔⺖⺗⺘⺙⺛⺜⺞⺟⺠⺡⺢⺣⺤⺥⺦⺧⺨⺩⺪⺫⺬⺭⺮⺯⺰⺱⺲⺳⺴⺵⺶⺷⺹⺺⺽⺾⺿⻀⻁⻂⻃⻄⻅⻆⻇⻈⻉⻊⻋⻌⻍
⻎⻏⻐⻑⻒⻓⻔⻕⻖⻗⻘⻙⻚⻛⻜⻝⻞⻟⻠⻡⻢⻣⻤⻥⻦⻧⻨⻩⻪⻫⻬⻭⻮⻯⻰⻱⻲⻳⼀⼁⼂⼃⼄⼅⼆⼇⼈⼉⼊⼋⼌⼍⼎⼏⼐⼑⼒⼓⼔⼕⼖⼗⼘⼙⼚⼛⼜⼝⼞⼟⼠⼡⼢⼣⼤⼥⼦⼧⼨⼩⼪⼫⼬⼭⼮⼯⼰⼱⼲⼳⼴⼵ 
⼶⼷⼸⼹⼺⼻⼼⼽⼾⼿⽀⽁⽂⽃⽄⽅⽆⽇⽈⽉⽊⽋⽌⽍⽎⽏⽐⽑⽒⽓⽔⽕⽖⽗⽘⽙⽚⽛⽜⽝⽞⽟⽠⽡⽢⽣⽤⽥⽦⽧⽨⽩⽪⽫⽬⽭⽮⽯⽰⽱⽲⽳⽴⽵⽶⽷⽸⽹⽺⽻⽼⽽⽾⽿⾀⾁⾂⾃⾄⾅⾆⾇⾈⾉⾊⾋⾌⾍⾎⾏⾐⾑ 
⾒⾓⾔⾕⾖⾗⾘⾙⾚⾛⾜⾝⾞⾟⾠⾡⾢⾣⾤⾥⾦⾧⾨⾩⾪⾫⾬⾭⾮⾯⾰⾱⾲⾳⾴⾵⾶⾷⾸⾹⾺⾻⾼⾽⾾⾿⿀⿁⿂⿃⿄⿅⿆⿇⿈⿉⿊⿋⿌⿍⿎⿏⿐⿑⿒⿓⿔⿕〇〾スリ㇀㇃㇅㇆㇊㇋㇌㇍㇎㇏㇐㇑㇒㇔㇕㇖㇗㇘㇙㇚ 
㇛㇜㇝㇞㇟㇠㇡㇢㇣㐃㐆㐧䍏乁乄书亊円卍卐孒孓曱車龜龜丹女年卑既辶華龜𠀀𠀈𠀌𠀍𠀑𠀟𠁦𠁧𠁩𠁰𠁱𠁾𠂀𠂂𠂍𠂣𠂼𠃉𠃛𠃢𠄓𠄙𠑹𠕄𠙴𠤬𠥻𠦁𠦮𡆵𡋬𡗒𡦹𡭔𡯁𡰴𡳿𢀓𢁺𢎗𢎜𢎧𢎱𢚎𣅲𣒚𣦶𣫬𤆍𤕪𤦡𤰃𥆞𥝌𥸨𦉭𦥒𦥫�𦫵𨈏𨈐𨈑𨳇𩇦𩇧𩇨𩙱𩰊𩰋𪓕𪓝𪚦𪚴𪛉𪛙𫝖𬺷𬻆𬼂𬼄𬼘𭔥𭣔𭨘𭺪𮎳𮠕乁北卑多㠯'')

"""

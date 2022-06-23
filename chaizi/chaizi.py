import random
import collections
from logzero import logger

JieGou = "〾⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻"
JieGou2 = "⿰⿱⿴⿵⿶⿷⿸⿹⿺⿻"
JieGou3 = "⿲⿳"

stars1 = 'αℓ↔↷①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑲△'
stars1 = set(stars1)
stars2 = '𛂦𠦮𡋬𡰣𢚎𤣩𨪐𬼂𬼄𭔥乁𰀁'
star = stars2[0]


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


Ids = read_ids()
logger.info((len(Ids), random.choice(Ids)))  # (88937, ['𦵀', ['⿱艹面']])


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


Ids2 = read_ids2()
logger.info((len(Ids2), random.choice(Ids2)))  # (92898, ('𥉲', ['⿰目展']))


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


ZiXing = read_ZiXing()
# (94227, ('𢐏', ['弛', '⿰弓𰲚']))
logger.info((len(ZiXing), random.choice(ZiXing)))


doc = Ids+Ids2+ZiXing
chars = set(x[0] for x in doc)
logger.info(("chars", len(chars)))  # ('chars', 94266)


def valid_ids(seq):
    if len(seq) <= 2:
        return 0
    if seq[0] not in JieGou:
        return 0
    if seq[-1] in JieGou or seq[-2] in JieGou:
        return 0
    if '？' in seq:
        return 0
    if stars1 & set(seq):
        return 0.1
    return 1


def seq_score(seq):
    v = valid_ids(seq)
    score = len(seq)-v*100
    return score


logger.info(valid_ids('⿱艹⿳⿲止自巳八夂'))


def merge(doc, path="ChaiZi/IdsAll.txt"):
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
        seqs = list(set(seqs))
        seqs.sort(key=lambda x: seq_score(x))
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


store = merge(doc)
logger.info((star, store[star]))


def choice(store):
    store1 = {}
    for k, seqs in store.items():
        if k in stars1:
            logger.info((k, seqs))
            d = 0
        if seqs:
            v = seqs[0]
        else:
            v = ''
        # if len(v)<=1:
            # logger.info((k,seqs))
        store1[k] = v
    return store1


ids0 = choice(store)
doc = open("ChaiZi/Valid.txt").read().splitlines()
doc = [x.split('\t') for x in doc]
for k, v in doc:
    ids0[k] = v


keys = set(ids0)
values = ''.join(ids0.values())
c = collections.Counter(values)
doc = [(k, v) for k, v in c.items()]
doc.sort(key=lambda x: (-x[1], x[0]))
with open("ChaiZi/GouJianFreq.tsv", "w") as f:
    for k, v in doc:
        f.write(f"{k}\t{v}\n")

values = set(values)

logger.info(
    f"keys:{len(keys)} values:{len(values)}  k-v:{len(keys-values)} ")
#  keys:94265 values:10994  k-v:83288

isolate = ''.join(k for k, v in ids0.items() if not v or k == v)
logger.info(("isolate", len(isolate), ''.join(isolate)))
"""
 ('isolate', 460, 'αℓ①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑲△⺄⺆いよりコサ㇀㇇㇉㇋㇌㇍㇎㇓㇞㇢㇣𛂦一丨丶丿乀乁乙乚乛亅人冂冖几凵凸凹匚卐卩厂囗尸己巳弓阝㔾車龜龜
丹女年卑既者艹辶華龜𠁧𠁾𠂆𠃉𠃊𠃋𠃌𠃍𠃎𠃑𠃛𠄌𠄎𠆢𠘧𠘨𠙴𠤬𠥓𡰣𢎗𢎜𢎧𬼂𬼄𮍌乁凵北卑及多尢㠯衣豕〇㇁㇂㇄㇅㇈㇊㇘㇝⺁⺂⺃⺅⺇⺉⺋⺍⺎⺏⺐⺑⺒⺓⺔⺖⺗⺘⺙⺛⺜⺞⺟⺠⺡⺢⺣⺤⺥ 
⺦⺧⺨⺩⺪⺫⺬⺭⺮⺯⺰⺱⺲⺳⺴⺵⺶⺷⺹⺺⺽⺾⺿⻀⻁⻂⻃⻄⻅⻆⻇⻈⻉⻊⻋⻌⻍⻎⻏⻐⻑⻒⻓⻔⻕⻖⻗⻘⻙⻚⻛⻜⻝⻞⻟⻠⻡⻢⻣⻤⻥⻦⻧⻨⻩⻪⻫⻬⻭⻮⻯⻰⻱⻲⻳⼀⼁⼂⼃⼄⼅⼆⼇⼈ 
⼉⼊⼋⼌⼍⼎⼏⼐⼑⼒⼓⼔⼕⼖⼗⼘⼙⼚⼛⼜⼝⼞⼟⼠⼡⼢⼣⼤⼥⼦⼧⼨⼩⼪⼫⼬⼭⼮⼯⼰⼱⼲⼳⼴⼵⼶⼷⼸⼹⼺⼻⼼⼽⼾⼿⽀⽁⽂⽃⽄⽅⽆⽇⽈⽉⽊⽋⽌⽍⽎⽏⽐⽑⽒⽓⽔⽕⽖⽗⽘⽙⽚⽛⽜ 
⽝⽞⽟⽠⽡⽢⽣⽤⽥⽦⽧⽨⽩⽪⽫⽬⽭⽮⽯⽰⽱⽲⽳⽴⽵⽶⽷⽸⽹⽺⽻⽼⽽⽾⽿⾀⾁⾂⾃⾄⾅⾆⾇⾈⾉⾊⾋⾌⾍⾎⾏⾐⾑⾒⾓⾔⾕⾖⾗⾘⾙⾚⾛⾜⾝⾞⾟⾠⾡⾢⾣⾤⾥⾦⾧⾨⾩⾪⾫⾬⾭⾮⾯⾰ 
⾱⾲⾳⾴⾵⾶⾷⾸⾹⾺⾻⾼⾽⾾⾿⿀⿁⿂⿃⿄⿅⿆⿇⿈⿉⿊⿋⿌⿍⿎⿏⿐⿑⿒⿓⿔⿕㇃㇆㇏㇐㇑㇒㇔㇕㇖㇗㇙㇚㇛㇜㇟㇠㇡')
"""

bujians = values-keys  # (16, '⿷⿺⿰⿻⿸？⿱↷⿲↔⿹⿳⿶⿵〾⿴')
logger.info((len(bujians), ''.join(bujians)))
bujians |= set(isolate)

for x in isolate:
    ids0[x] = x 

bujians = sorted(list(bujians))
logger.info(("bujians", len(bujians), ''.join(bujians)))
"""
('bujians', 476, 'αℓ↔↷①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑲△⺁⺂⺃⺄⺅⺆⺇⺉⺋⺍⺎⺏⺐⺑⺒⺓⺔⺖⺗⺘⺙⺛⺜⺞⺟⺠⺡⺢⺣⺤⺥⺦⺧⺨⺩⺪⺫⺬⺭⺮⺯⺰⺱⺲⺳⺴⺵⺶⺷
⺹⺺⺽⺾⺿⻀⻁⻂⻃⻄⻅⻆⻇⻈⻉⻊⻋⻌⻍⻎⻏⻐⻑⻒⻓⻔⻕⻖⻗⻘⻙⻚⻛⻜⻝⻞⻟⻠⻡⻢⻣⻤⻥⻦⻧⻨⻩⻪⻫⻬⻭⻮⻯⻰⻱⻲⻳⼀⼁⼂⼃⼄⼅⼆⼇⼈⼉⼊⼋⼌⼍⼎⼏⼐⼑⼒⼓⼔⼕⼖⼗⼘⼙⼚ 
⼛⼜⼝⼞⼟⼠⼡⼢⼣⼤⼥⼦⼧⼨⼩⼪⼫⼬⼭⼮⼯⼰⼱⼲⼳⼴⼵⼶⼷⼸⼹⼺⼻⼼⼽⼾⼿⽀⽁⽂⽃⽄⽅⽆⽇⽈⽉⽊⽋⽌⽍⽎⽏⽐⽑⽒⽓⽔⽕⽖⽗⽘⽙⽚⽛⽜⽝⽞⽟⽠⽡⽢⽣⽤⽥⽦⽧⽨⽩⽪⽫⽬⽭⽮ 
⽯⽰⽱⽲⽳⽴⽵⽶⽷⽸⽹⽺⽻⽼⽽⽾⽿⾀⾁⾂⾃⾄⾅⾆⾇⾈⾉⾊⾋⾌⾍⾎⾏⾐⾑⾒⾓⾔⾕⾖⾗⾘⾙⾚⾛⾜⾝⾞⾟⾠⾡⾢⾣⾤⾥⾦⾧⾨⾩⾪⾫⾬⾭⾮⾯⾰⾱⾲⾳⾴⾵⾶⾷⾸⾹⾺⾻⾼⾽⾾⾿⿀⿁⿂ 
⿃⿄⿅⿆⿇⿈⿉⿊⿋⿌⿍⿎⿏⿐⿑⿒⿓⿔⿕⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻〇〾いよりコサ㇀㇁㇂㇃㇄㇅㇆㇇㇈㇉㇊㇋㇌㇍㇎㇏㇐㇑㇒㇓㇔㇕㇖㇗㇘㇙㇚㇛㇜㇝㇞㇟㇠㇡㇢㇣㔾一丨丶丿乀乁乙乚乛 
亅人冂冖几凵凸凹匚卐卩厂囗尸己巳弓阝車龜龜丹女年卑既者艹辶華龜？𛂦𠁧𠁾𠂆𠃉𠃊𠃋𠃌𠃍𠃎𠃑𠃛𠄌𠄎𠆢𠘧𠘨𠙴𠤬𠥓𡰣𢎗𢎜𢎧𬼂𬼄𮍌乁凵北卑及多尢㠯衣豕')
"""
bujians = set(bujians)


def automic(dic0):
    dic1 = {}
    for k, v in dic0.items():
        u = ''.join(dic0.get(x, x) for x in v)
        dic1[k] = u
    return dic1


def get_bujians(dic0):
    bujians0 = set(''.join(dic0.values()))
    for i in range(5):
        dic1 = automic(dic0)
        bujians1 = set(''.join(dic1.values()))
        logger.info((i, len(bujians0), len(bujians1),
                    ''.join(bujians0-bujians1)[:10]))
        dic0 = dic1
        bujians0 = bujians1
    bujians = list(bujians0)
    bujians.sort()
    bujians = ''.join(bujians)
    return bujians


"""
[I 220624 00:34:59 ChaiZi:226] (0, 11350, 2782, '毇翁炳咪𬺹醫郊讃𡘃抾')
[I 220624 00:35:02 ChaiZi:226] (1, 2782, 832, '危风匝癸𦮠諸度侖欶芥')
[I 220624 00:35:09 ChaiZi:226] (2, 832, 505, '刖𡿨𰆘戓氏果𠄐𠂌共𫩏')
[I 220624 00:35:19 ChaiZi:226] (3, 505, 504, '儿')
[I 220624 00:35:30 ChaiZi:226] (4, 504, 504, '')
"""

goujians = get_bujians(ids0)
logger.info((len(goujians), goujians))
"""
(501, 'αℓ↔↷①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑲△⺁⺂⺃⺄⺅⺆⺇⺉⺋⺍⺎⺏⺐⺑⺒⺓⺔⺖⺗⺘⺙⺛⺜⺞⺟⺠⺡⺢⺣⺤⺥⺦⺧⺨⺩⺪⺫⺬⺭⺮⺯⺰⺱⺲⺳⺴⺵⺶⺷⺹⺺⺽⺾⺿ 
⻀⻁⻂⻃⻄⻅⻆⻇⻈⻉⻊⻋⻌⻍⻎⻏⻐⻑⻒⻓⻔⻕⻖⻗⻘⻙⻚⻛⻜⻝⻞⻟⻠⻡⻢⻣⻤⻥⻦⻧⻨⻩⻪⻫⻬⻭⻮⻯⻰⻱⻲⻳⼀⼁⼂⼃⼄⼅⼆⼇⼈⼉⼊⼋⼌⼍⼎⼏⼐⼑⼒⼓⼔⼕⼖⼗⼘⼙⼚⼛⼜⼝⼞⼟ 
⼠⼡⼢⼣⼤⼥⼦⼧⼨⼩⼪⼫⼬⼭⼮⼯⼰⼱⼲⼳⼴⼵⼶⼷⼸⼹⼺⼻⼼⼽⼾⼿⽀⽁⽂⽃⽄⽅⽆⽇⽈⽉⽊⽋⽌⽍⽎⽏⽐⽑⽒⽓⽔⽕⽖⽗⽘⽙⽚⽛⽜⽝⽞⽟⽠⽡⽢⽣⽤⽥⽦⽧⽨⽩⽪⽫⽬⽭⽮⽯⽰⽱⽲⽳ 
⽴⽵⽶⽷⽸⽹⽺⽻⽼⽽⽾⽿⾀⾁⾂⾃⾄⾅⾆⾇⾈⾉⾊⾋⾌⾍⾎⾏⾐⾑⾒⾓⾔⾕⾖⾗⾘⾙⾚⾛⾜⾝⾞⾟⾠⾡⾢⾣⾤⾥⾦⾧⾨⾩⾪⾫⾬⾭⾮⾯⾰⾱⾲⾳⾴⾵⾶⾷⾸⾹⾺⾻⾼⾽⾾⾿⿀⿁⿂⿃⿄⿅⿆⿇ 
⿈⿉⿊⿋⿌⿍⿎⿏⿐⿑⿒⿓⿔⿕⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻〇〾いよりコサ㇀㇁㇂㇃㇄㇅㇆㇇㇈㇉㇊㇋㇌㇍㇎㇏㇐㇑㇒㇓㇔㇕㇖㇗㇘㇙㇚㇛㇜㇝㇞㇟㇠㇡㇢㇣㐅㔾一丨丶丷丿乀乁乙乚乛亅二亠 
人入全冂冖几凵凸凹匚十卐卜卩厂口囗土尸己巳弓曰末牜王訁釒阝車龜龜丹女年卑既者艹辶華龜？𛂦𠁧𠁾𠂆𠂉𠃉𠃊𠃋𠃌𠃍𠃎𠃑𠃛𠄌𠄎𠆢𠘧𠘨𠙴𠤬𠥓𠦮𡋬𡭔𡰣𢎗𢎜𢎧�𤣩𤰃𬼂𬼄𭔥𮍌乁凵北卑及多��㠯衣豕𰀁'')
"""
for x in goujians:
    ids0[x] = x

goujians = set(goujians)
logger.info((star, ids0.get(star, ''), star in goujians))

logger.info((len(bujians-goujians), len(goujians-bujians)))

YuanZi = open("YuanZi/YuanZi.txt").read().splitlines()
YuanZi = set(x for x in YuanZi if x)

ChaiZi = []
for k, v in ids0.items():
    if k in YuanZi:
        v = k
    ChaiZi.append((k, v))
ChaiZi.sort(key=lambda x: x[0])

with open("ChaiZi/ChaiZi.txt", "w") as f:
    for x in ChaiZi:
        r = '\t'.join(x)
        f.write(r+'\n')

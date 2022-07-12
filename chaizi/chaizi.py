import random
import collections
from logzero import logger
from UnicodeTokenizer import UnicodeTokenizer

JieGou = "〾⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻"
JieGou2 = "⿰⿱⿴⿵⿶⿷⿸⿹⿺⿻"
JieGou3 = "⿲⿳"

stars1 = 'αℓ↔↷①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑲△'
stars1 = set(stars1)
stars2 = '𠦮𡋬𡰣𢚎𤣩𨪐𬼄𭔥乁'
star = '乌'


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
        seqs = [x for x in seqs if x]
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
        seqs = [''.join(x for x in s if ord(x) >= 128) for s in seqs]
        seqs = [x for x in seqs if x ]
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
        seqs = [x for x in seqs if x ]
        seqs = list(set(seqs))
        doc.append((k, seqs))
    return doc


def odd(seq):
    for x in seq:
        if not UnicodeTokenizer.detect_hanzi(x):
            return 1
    return 0

def seq_score(seq):
    if seq[-1] in JieGou or len(seq)>=2 and seq[-2] in JieGou:
        return 0
    if odd(seq):
        return 1
    if seq[0] not in JieGou:
        return 2
    if len(seq) <= 2:
        return 3
    return 4


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
        seqs = [x for x in seqs if x ]
        if len(seqs) >= 3:
            c = collections.Counter(seqs)
            # logger.info((k,seqs))
            top = max(c.values())
            seqs = [x for x in seqs if c[x] == top]
        seqs = list(set(seqs))
        seqs.sort(key=lambda x: -seq_score(x))
        if seqs and odd(seqs[0]):
            logger.warning((k, seqs[0]))
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

    ids0 = {k: v for k, v in ids.items() if not odd(k)}
    keys = set(ids0)
    values = set(''.join(ids0.values()))
    # chars:94235 seqs:10830
    logger.info(f"chars:{len(keys)} seqs:{len(values)} ")

    odds = set(ids)-set(ids0)
    # ('odd keys', 30, '⑥⑯𛂦ヨ④⑧⑭△②⑮⑤よ⑦⑩いαユサ⑲⑨り③①リス⑬ℓ⑫コ⑪')
    logger.info(("odd keys", len(odds), ''.join(odds)))

    keys = set(k for k, v in ids0.items() if k == v)
    values = set(''.join(ids.values()))-set(ids0)
    logger.info(f"( base {len(keys)}, {''.join(keys)}''")
    logger.info(f"( odd values: {len(values)},  {''.join(values)}")

    doc = [(k, v) for k, v in ids0.items()]
    doc.sort(key=lambda x: (x[0]))
    with open(path, 'w') as f:
        for k, v in doc:
            l = f"{k}\t{v}"
            f.write(l+'\n')

    logger.info((len(keys), len(values)))
    logger.info((len(keys-values), len(values-keys)))


if __name__ == "__main__":

    logger.info(seq_score('⿱艹⿳⿲止自巳八夂'))

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

    path = "ChaiZi/ChaiZi.txt"
    choice(store, path)

"""
[I 220629 01:37:34 ChaiZi:160] chars:94235 seqs:10822 
[I 220629 01:37:34 ChaiZi:164] ('odd keys', 30, '②①④ヨユ⑯⑦③リ⑧コい⑫⑤サ⑮⑩αℓり⑬⑨⑪⑲ス⑭△よ⑥𛂦')
[I 220629 01:37:34 ChaiZi:168] ( base 434, ⼳⾊⾯⻍⺨𡰣⾉〇⼼⾍乛⼚尸𠘨⺒㇌⻨⺔⼋⻰⿅⼻⺥衣巳⼯⾪⼌⿁⼓⽈凵⿄⾴⺮⾌⾏⾓⾦⼧⿂㇝⻘乙⻋⺣⾈⽔⻔⾆㇏⽮𠃍⻥㇃⺺⽩⿃⺂⿑丹𠂆⼿
㇋⻑⼑⿒乁㇇⺿⾜⾁⾤⽢冂⼫⺰⼒⽆龜⺷⺅⼎⻂㠯⺜⽱⾨𢎧⺪厂⿎⻊乚⿓⻞⻚⻃⼶既⻬㇙⽕⽝冖⼊⾳⽊⻢⺠⺾⻟⾀⺩⻀⽃⼙⽜⽿⼹⺳⾔𠃌⼲⼐⽛𢎗⾑⺋⽙⽬⺉㇂㇢⺏⾕⺱㇎⽧⺃丿⾧⼆𠃑⻌⺴⻠�𬼂⻓⻓⺟⼏⽐者亅⿉⾛㇓⾾⻳⾶⻜⺗⻧⼠⼔⺘⺢⻒⺽⻱⻙⼪⼈𠃛⿔⺵⺤㇣⺭⽽⼞⼩⾫⼷⻎⻅龜⼁⻗⽦𠃋𠙴⽠⽓⻭㇐匚⻁⺹⽍⼾⾮𠃉⻩㇍⻄囗華𠄌⽒⺞⿇⾬𠁾⽡⻇⼅⻝⽟⽇⾅⾃⼀卑⻮⽏⺬龜⽁⾹ 
⻫⻯⾷⼄⾋𠁧⼨⺑⼬⾩㇀己⽼㇚⾣⼱⾵⽅⻦⼸⺇⾐⻈⻡⿈辶⼰⽤⽫⾻㇁⻐⺲⽋⾭⻲㇡㇕⾡⽳⺓㇗⽂凵⺶⾥人㇈⼣⿊㇉⺙㇒⾎⼴⾇⽑⽪⾘⻛㇖㇛𠆢⼟⿌㇑⻆⼛乁𠃊⿐㇆⾒⽘⼍丨⺍⺆⻉⼮車⽶⽣⻖ 
⾲𠥓⺄⼂⽨⼖⾼⾝㇜⺛几𠘧艹年⼉豕弓⺧及⼦⼇⽲⼝⽥⽰⼭⾽⼽⾠凹⿍⺖⼥一⽴𠃎⾂⽯⽉⽻⻤㇞⽸㇘⾄⻏⾸⽷⾱⼗⻪⿀⼡⿏㇠𮍌阝⻣⼤㇊⺁多丶㔾凸⼕⾞⺯卑㇟尢⽎⼺⼢⽞⿋⽹𬼄⾖㇄⼜⺦⻕⼃ 
乀⿕⾺⽭⽀⺐⺫⽌⾰⼘⺎⽚𠤬㇅⽾⽗卐⽄⽺㇔⾚⼵⾙⽵⽖女𢎜北⾢⾟⾗⾿⺡⿆''
[I 220629 01:37:34 ChaiZi:169] ( odd values: 46,  ②①④ヨ⿺ユ⑯⑦⿷↷⿱⿹〾③リ⑧⿴↔コい⑫⿸⑤⿰⑮サ⿻⑩αℓ⿵⑬⿳り⑪⑨⿶⑲？ス⑭△よ⑥⿲𛂦
[I 220629 01:37:34 ChaiZi:178] (434, 46)
[I 220629 01:37:34 ChaiZi:179] (434, 46)
"""

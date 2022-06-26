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

path = "ChaiZi/ChaiZi.txt"
doc=open(path).read().splitlines()
doc=[x.split('\t') for x in doc]
ids={k:v for k,v in doc}

keys = set(ids)
values = ''.join(ids.values())

c = collections.Counter(values)
doc = [(k, v) for k, v in c.items()]
doc.sort(key=lambda x: (-x[1], x[0]))
with open("ChaiZi/GouJianFreq.tsv", "w") as f:
    for k, v in doc:
        f.write(f"{k}\t{v}\n")

values = set(values)

logger.info(
    f"keys:{len(keys)} values:{len(values)}  k-v:{len(keys-values)} ")
#  [I 220625 03:32:11 Goujian:31] keys:94281 values:10807  k-v:83474

isolate = ''.join(k for k, v in ids.items() if not v or k == v)
logger.info(("isolate", len(isolate), ''.join(isolate)))
"""
 ('isolate', 477,
'αℓ↔↷①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑲△⺁⺂⺃⺄⺅⺆⺇⺉⺋⺍⺎⺏⺐⺑⺒⺓⺔⺖⺗⺘⺙⺛⺜⺞⺟⺠⺡⺢⺣⺤⺥⺦⺧⺨⺩⺪⺫⺬⺭⺮⺯⺰⺱⺲⺳⺴⺵⺶⺷⺹⺺⺽⺾⺿⻀⻁⻂⻃⻄⻅⻆⻇⻈⻉⻊⻋⻌⻍⻎⻏⻐⻑⻒⻓⻔⻕⻖⻗⻘⻙⻚⻛⻜⻝⻞⻟⻠⻡⻢⻣⻤⻥⻦⻧⻨⻩⻪⻫⻬⻭⻮⻯⻰⻱⻲⻳⼀⼁⼂⼃⼄⼅⼆⼇⼈⼉⼊⼋⼌⼍⼎⼏⼐⼑⼒⼓⼔⼕⼖⼗⼘⼙⼚⼛⼜⼝⼞⼟⼠⼡⼢⼣⼤⼥⼦⼧⼨⼩⼪⼫⼬⼭⼮⼯⼰⼱⼲⼳⼴⼵⼶⼷⼸⼹⼺⼻⼼⼽⼾⼿⽀⽁⽂⽃⽄⽅⽆⽇⽈⽉⽊⽋⽌⽍⽎⽏⽐⽑⽒⽓⽔⽕⽖⽗⽘⽙⽚⽛⽜⽝⽞⽟⽠⽡⽢⽣⽤⽥⽦⽧⽨⽩⽪⽫⽬⽭⽮⽯⽰⽱⽲⽳⽴⽵⽶⽷⽸⽹⽺⽻⽼⽽⽾⽿⾀⾁⾂⾃⾄⾅⾆⾇⾈⾉⾊⾋⾌⾍⾎⾏⾐⾑⾒⾓⾔⾕⾖⾗⾘⾙⾚⾛⾜⾝⾞⾟⾠⾡⾢⾣⾤⾥⾦⾧⾨⾩⾪⾫⾬⾭⾮⾯⾰⾱⾲⾳⾴⾵⾶⾷⾸⾹⾺⾻⾼⾽⾾⾿⿀⿁⿂⿃⿄⿅⿆⿇⿈⿉⿊⿋⿌⿍⿎⿏⿐⿑⿒⿓⿔⿕⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻〇〾いよりコサ㇀㇁㇂㇃㇄㇅㇆㇇㇈㇉㇊㇋㇌㇍㇎㇏㇐㇑㇒㇓㇔㇕㇖㇗㇘㇙㇚㇛㇜㇝㇞㇟㇠㇡㇢㇣㔾一丨丶丿乀乁乙乚乛亅人冂冖几凵凸凹匚卐卩厂囗尸己巳弓阝\ue817車龜龜丹女年卑既者艹辶華龜？𛂦𠁧𠁾𠂆𠃉𠃊𠃋𠃌𠃍𠃎𠃑𠃛𠄌𠄎𠆢𠘧𠘨𠙴𠤬𠥓𡰣𢎗𢎜𢎧𬼂𬼄𮍌乁凵北卑及多尢㠯衣豕'
"""

bujians = values-keys  # (16, '⿷⿺⿰⿻⿸？⿱↷⿲↔⿹⿳⿶⿵〾⿴')
logger.info((len(bujians), ''.join(bujians)))
bujians |= set(isolate)

for x in isolate:
    ids[x] = x 

bujians = sorted(list(bujians))
bujians=''.join(bujians)
logger.info(("bujians", len(bujians), bujians))
"""
('bujians', 477, 
'αℓ↔↷①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑲△⺁⺂⺃⺄⺅⺆⺇⺉⺋⺍⺎⺏⺐⺑⺒⺓⺔⺖⺗⺘⺙⺛⺜⺞⺟⺠⺡⺢⺣⺤⺥⺦⺧⺨⺩⺪⺫⺬⺭⺮⺯⺰⺱⺲⺳⺴⺵⺶⺷⺹⺺⺽⺾⺿⻀⻁⻂⻃⻄⻅⻆⻇⻈⻉⻊⻋⻌⻍⻎⻏⻐⻑⻒⻓⻔⻕⻖⻗⻘⻙⻚⻛⻜⻝⻞⻟⻠⻡⻢⻣⻤⻥⻦⻧⻨⻩⻪⻫⻬⻭⻮⻯⻰⻱⻲⻳⼀⼁⼂⼃⼄⼅⼆⼇⼈⼉⼊⼋⼌⼍⼎⼏⼐⼑⼒⼓⼔⼕⼖⼗⼘⼙⼚⼛⼜⼝⼞⼟⼠⼡⼢⼣⼤⼥⼦⼧⼨⼩⼪⼫⼬⼭⼮⼯⼰⼱⼲⼳⼴⼵⼶⼷⼸⼹⼺⼻⼼⼽⼾⼿⽀⽁⽂⽃⽄⽅⽆⽇⽈⽉⽊⽋⽌⽍⽎⽏⽐⽑⽒⽓⽔⽕⽖⽗⽘⽙⽚⽛⽜⽝⽞⽟⽠⽡⽢⽣⽤⽥⽦⽧⽨⽩⽪⽫⽬⽭⽮⽯⽰⽱⽲⽳⽴⽵⽶⽷⽸⽹⽺⽻⽼⽽⽾⽿⾀⾁⾂⾃⾄⾅⾆⾇⾈⾉⾊⾋⾌⾍⾎⾏⾐⾑⾒⾓⾔⾕⾖⾗⾘⾙⾚⾛⾜⾝⾞⾟⾠⾡⾢⾣⾤⾥⾦⾧⾨⾩⾪⾫⾬⾭⾮⾯⾰⾱⾲⾳⾴⾵⾶⾷⾸⾹⾺⾻⾼⾽⾾⾿⿀⿁⿂⿃⿄⿅⿆⿇⿈⿉⿊⿋⿌⿍⿎⿏⿐⿑⿒⿓⿔⿕⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻〇〾いよりコサ㇀㇁㇂㇃㇄㇅㇆㇇㇈㇉㇊㇋㇌㇍㇎㇏㇐㇑㇒㇓㇔㇕㇖㇗㇘㇙㇚㇛㇜㇝㇞㇟㇠㇡㇢㇣㔾一丨丶丿乀乁乙乚乛亅人冂冖几凵凸凹匚卐卩厂囗尸己巳弓阝\ue817車龜龜丹女年卑既者艹辶華龜？𛂦𠁧𠁾𠂆𠃉𠃊𠃋𠃌𠃍𠃎𠃑𠃛𠄌𠄎𠆢𠘧𠘨𠙴𠤬𠥓𡰣𢎗𢎜𢎧𬼂𬼄𮍌乁凵北卑及多尢㠯衣豕'
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
[I 220625 03:32:56 Goujian:72] (0, 10807, 2623, '泌𧵚拈彎廸翚僃閰畂㚚')
[I 220625 03:33:06 Goujian:72] (1, 2623, 803, '兑聿感奔𦘔也𤋱孰车𦉰')
[I 220625 03:33:16 Goujian:72] (2, 803, 503, '井四𠂈⺊朩冃艮亻弔龷')
[I 220625 03:33:28 Goujian:72] (3, 503, 502, '儿')
[I 220625 03:33:40 Goujian:72] (4, 502, 502, '')
"""

goujians = get_bujians(ids)
logger.info((len(goujians), goujians))
"""
503
'αℓ↔↷①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑲△⺁⺂⺃⺄⺅⺆⺇⺉⺋⺍⺎⺏⺐⺑⺒⺓⺔⺖⺗⺘⺙⺛⺜⺞⺟⺠⺡⺢⺣⺤⺥⺦⺧⺨⺩⺪⺫⺬⺭⺮⺯⺰⺱⺲⺳⺴⺵⺶⺷⺹⺺⺽⺾⺿⻀⻁⻂⻃⻄⻅⻆⻇⻈⻉⻊⻋⻌⻍⻎⻏⻐⻑⻒⻓⻔⻕⻖⻗⻘⻙⻚⻛⻜⻝⻞⻟⻠⻡⻢⻣⻤⻥⻦⻧⻨⻩⻪⻫⻬⻭⻮⻯⻰⻱⻲⻳⼀⼁⼂⼃⼄⼅⼆⼇⼈⼉⼊⼋⼌⼍⼎⼏⼐⼑⼒⼓⼔⼕⼖⼗⼘⼙⼚⼛⼜⼝⼞⼟⼠⼡⼢⼣⼤⼥⼦⼧⼨⼩⼪⼫⼬⼭⼮⼯⼰⼱⼲⼳⼴⼵⼶⼷⼸⼹⼺⼻⼼⼽⼾⼿⽀⽁⽂⽃⽄⽅⽆⽇⽈⽉⽊⽋⽌⽍⽎⽏⽐⽑⽒⽓⽔⽕⽖⽗⽘⽙⽚⽛⽜⽝⽞⽟⽠⽡⽢⽣⽤⽥⽦⽧⽨⽩⽪⽫⽬⽭⽮⽯⽰⽱⽲⽳⽴⽵⽶⽷⽸⽹⽺⽻⽼⽽⽾⽿⾀⾁⾂⾃⾄⾅⾆⾇⾈⾉⾊⾋⾌⾍⾎⾏⾐⾑⾒⾓⾔⾕⾖⾗⾘⾙⾚⾛⾜⾝⾞⾟⾠⾡⾢⾣⾤⾥⾦⾧⾨⾩⾪⾫⾬⾭⾮⾯⾰⾱⾲⾳⾴⾵⾶⾷⾸⾹⾺⾻⾼⾽⾾⾿⿀⿁⿂⿃⿄⿅⿆⿇⿈⿉⿊⿋⿌⿍⿎⿏⿐⿑⿒⿓⿔⿕⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻〇〾いよりコサ㇀㇁㇂㇃㇄㇅㇆㇇㇈㇉㇊㇋㇌㇍㇎㇏㇐㇑㇒㇓㇔㇕㇖㇗㇘㇙㇚㇛㇜㇝㇞㇟㇠㇡㇢㇣㐅㔾一丨丶丷丿乀乁乙乚乛亅二亠人全冂冖几凵凸凹匚十卐卑卜卩厂口囗土堇尸己巳弓曰末牜王訁釒阝\ue817車龜龜丹女年卑既者艹辶華龜？𛂦𠁧𠁾𠂆𠂉𠃉𠃊𠃋𠃌𠃍𠃎𠃑𠃛𠄌𠄎𠆢𠘧𠘨𠙴𠤬𠥓𠦮𡋬𡭔𡰣𢎗𢎜𢎧𢚎𤣩𤰃𬼂𬼄𭔥𮍌乁凵北卑及多尢㠯衣豕𰀁'
"""

goujians = set(goujians)
logger.info((star, ids.get(star, ''), star in goujians))

logger.info((len(bujians-goujians), len(goujians-bujians)))


logger.info((len(bujians-goujians), len(goujians-bujians)))
goujians = list(goujians)
goujians.sort()
with open("ChaiZi/GouJian.txt", 'w') as f:
    for x in goujians:
        f.write(x+'\n')

"""

"""

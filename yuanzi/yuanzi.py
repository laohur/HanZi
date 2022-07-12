from logzero import logger
from UnicodeTokenizer.UnicodeTokenizer import detect_hanzi


def merge(files):
    doc = []
    for x in files:
        a = open(x).read().splitlines()
        doc += a
    doc = [x for x in doc if x]
    Ji = set(x for x in doc if detect_hanzi(x))
    notHanzi = set(x for x in doc if not detect_hanzi(x))
    logger.warning(''.join(notHanzi))
    logger.info(len(Ji))
    return Ji


files = ["BiHua/BiHua.txt", "BuJian/BuJian.txt",         "DuTiZi/DuTiZi.txt"]
JiZi = merge(files)

files = ["BiHua/BiHua.txt",    "BuJian/BuJianIds.txt", "DuTiZi/DuTiZi.txt"]
JiZiIds = merge(files)

fresh = JiZiIds-JiZi
fresh = list(fresh)
fresh.sort()
fresh = ''.join(fresh)
logger.info((len(fresh), fresh))


def save(JiZi, path):

    JiZi = list(JiZi)
    JiZi.sort()

    with open(path, "w") as f:
        for x in JiZi:
            f.write(x+'\n')
    logger.info(len(JiZi))


path = "YuanZi/YuanZi.txt"
save(JiZi, path)
path = "YuanZi/YuanZiIds.txt"
save(JiZiIds, path)

"""
[W 220713 00:47:51 YuanZi:13] �
[I 220713 00:47:51 YuanZi:14] 1128
[W 220713 00:47:51 YuanZi:13] �
[I 220713 00:47:51 YuanZi:14] 2233
[I 220713 00:47:51 YuanZi:28] (1105, '㐌㐬㐭㒸㓞㕚㕣㕥㖖㗊㘠㚅㚔㚘㝉㝑㝴㝵㞌㞢㞷㠩㠭㡭㣈㣎㣺㥯㪅㫐㫒㫗㫺㬅㬎㯥㲎㲽㳄㳟㴆㸒㸚㹜㽞㿟䀠䂞䋰䍃䎜䏌䏍䏎䓵䖒䖝䖵䙲䙴䚻䜌䜭䡛䧹䩗䩻丗丛丞両並丼 
丽乏乕乖乞买亀亇争亐亗亙亟亢交亨享京亭亲亳亶亽今介仍仒仕付代令以任伐休伯何余佥佰侌侵保俞倉倝倠倶僉兄充兇光兊兌免兑兒兓兔兟兦全兮共关兴兵具典兹冐冒冓冗军冝冡冬凢処凶凷函分刍刕刖列利到制 
則前剡加务劦助劵動務勾匀包匈匊匋匍化匝匡匪区医匽匿區卉卋卒卓单占卣卥卦卪卬危即却卷卸厈厓厘原厤厲厸去厼厽參友双反叐叒叔取叜叟古句另叩只召可台右号司叹吂各合吉吊吋同名后向吕君否含启吴吾呂 
呆呈告呙周咎咠咢咸品員問啚善喜喬單嗇嚴囘囙囚回因困囷固圡圣圤在圭圼坐垔埶執堯墨壮壯声壳壹壽夃处备复夏夒多夢夰夲夵夶夸奄奇奈奉奐奔奚奞奠奴奻如妟妥妾委孖存孚孛孝学孨孰宁它安宋完宓宗官宛客 
宣害容宿寍寺寽寿將專尉尋尌尒尗尨就尼尾尿屈屋屏屖屚屾岡崔巟巢左巩巫差巸巽市布希帚帛帝師席帶幸幽府庶廉延廷建弁弄式弘弜弟弱彔录彗彥彦徙御復微忩念思急怱恣恭患悤惟惠惢意感戎成戔戕或戚戜戠戢 
扁执折攸敄敏敕敖敝敢散敦敫敬斦斩斬斯斲斿旁旉族既旦旧旨早旬旱旲旾昆昌昍明昏易昔昗昚星春昭是显景晶智曹曼曾最朁有朋朔杀杲林某柔柰桀條棘棥楽樂樊次欮欶此武歨歮歲歷死殸殹殿毎每氾氿沙沝沮泉波 
洛洰浦淮湯溥灭灰灷炎炏炗烏烕烝無焦焱熊熏爯爰牟牪犀狂狺猒玟玨珀珎珤甬男甹画畏畕留畜番異畱畺畾疑登發皃皆皇皕盇监監盧直相盾眉県眔眞真睪睿瞿矍矞矣知砳磊祟票祭离禿秀秃秋秝秦稟穌空竒竜竟章童 
筑算籴粉素累絭維罙署羅羌羍美羔羴習翟考者耎耑耤耶耿聑聶肖育肴胃胡能臤臧臯臱臸舀舂舄舋舍舠般芏芻苋苗苟若茲莧莫華萈萠蒦蓺蔑薛虒虗虚虛虽蜀蟲袁褱襄要訇詹誊誩豈豊豐豖豙象豦豩貇負貢貫責貴買賁 
賏賓賣賴负贡贵路躬軍軎辟辱農迶通逢連遀遂達邕那郎鍂閒間閵闌间阑陰隋隡隻雀集雈雋雍雐雔雝難雲需韯韱頃頻馮駦騳鬳龱卑既者𠀃𠀉𠀎𠀐𠁣𠁳𠂋𠂑𠂛𠂝𠂡𠂢𠂹𠃉𠃓𠃔𠃤𠄐𠄠𠄢𠄭𠅃𠅇𠆣𠆥𠇍𠈇𠈌𠌵𠌶𠒆𠓜𠔉𠔥�𠔽𠔿𠕀𠕻𠖬𠙸𠙼𠚍𠚣𠚪𠠴𠣏𠣜𠤕𠦂𠦄𠦏𠦜𠦝𠦬𠧢𠧪𠧴𠩵𠪚𠫔𠫝𠫤𠫯𠬞𠬢𠬤𠬶𠭖𠮛𠮠𠮡𠮥𠮦𠮰𠮷𠯃𠯑𠱄𠱠𠳋𠷎𡇒𡈼��𡉚𡉵𡋰𡍬𡏳𡕩𡖅𡗜𡗞𡘲𡥀𡥂𡨄𡩜𡩧𡬠𡭴𡭽𡯄𡰣𡰥𡰯𡰲𡱒𡱝𡴎𡵂𡵉𡿧𡿩𡿪𡿯𡿺𢀛𢀡𢂇𢆉𢆰𢆶𢆸𢇁𢇇�𢌬𢎨𢏝𢑑𢖻𢗰𢚩𢛳𢦑𢼄𢽠𢾰𣁋𣄼𣅀𣅊𣅽𣆪𣌢𣎾𣏂𣏃𣏋𣏏𣏟𣏰𣏼𣘐𣥖𣦵𣦼𣪊𣪠𣬉𣳾𣴎𤆌𤆍𤇾𤊅𤋱𤏷𤔌𤔔𤕦𤕫𤕰𤬦𤯔𤰇𤰈𤰔𤽄𥁕𥃦𥃭𥃲𥑟𥘈𥝢𥞤𥪖𥱡𦀺𦉪𦉫𦉬𦉰𦉼𦋹𦍎𦍒𦎧𦐇𦔻𦘔𦣻𦥔𦥯𦦉𦨉𦫳𦫸𦫺𦫽𦬅𦭝𦰩𧆞𧈧𧥢𧱏�𨊠𨊥𨥫𨾴𩠐𩰊𩰋𩵋𩾏𪞏𪟽𪠲𪢱𪢴𪺍𫀄𫂱𫇦𫊫𫔴𫠤𫠥𫠩𫡏𫡙𫢉𫥞𫧇𫩏𫩠𫪡𫯁𫲸𫲽𫵖𫶧𫹍𬌪𬎾𬎿𬐘𬐚𬗌𬙙𬛸𬟩𬯁𬺰𬺻��𬼀𬼖𬼸𭁈𭁟𭁠𭁨𭃂𭅰𭅲𭔰𭚧𭠍𭣦𭤨𭥍𭥐𭥫𭥴𭩠𭴘𭷔𭻾𭾁𮅕𮈄𮍌𮍏𮓗𮙸𮧮𮩴𮫙免𰀁𰀂𰀄𰀉𰀕𰀠𰀡𰀢�𰀪𰁜𰃦𰃮𰆊𰆘𰋙𰍧𰕎𰗣𰢴𰢵𰤲𰤷𰥍𰧭𰯲𱁈')
[I 220713 00:47:51 YuanZi:39] 1128
[I 220713 00:47:51 YuanZi:39] 2233
"""

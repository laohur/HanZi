# -*- coding: utf-8 -*-
import collections
from logzero import logger



JieGou = "〾⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻"
JieGou1 = "〾"
JieGou2 = "⿰⿱⿴⿵⿶⿷⿸⿹⿺⿻"
JieGou3 = "⿲⿳"

stars2 = '𛂦𠦮𡋬𡰣𢚎𤣩𨪐𬼂𬼄𭔥乁𰀁'
star = stars2[0]

path = "ChaiZi/ChaiZi.txt"
doc = open(path).read().splitlines()
doc = [x.split('\t') for x in doc]
ids = {k: v for k, v in doc}

values=''.join(ids.values())
freq = collections.Counter(values)
GouJianFreq = [(k, v) for k, v in freq.items()]
GouJianFreq.sort(key=lambda x: (-x[1], x[0]))
with open("ChaiZi/GouJianFreq0.tsv", 'w') as f:
    for k, v in GouJianFreq:
        f.write(f"{k}\t{v}"+'\n')


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
[I 230410 01:13:10 Goujian:60] epoch:0
[I 230410 01:13:10 Goujian:43] (2321, '⿱丶艹干肀一⿰丨亅丿勹二卜⿹丅不⿻廿内从氶王厶北⿵帀凵𡈼冂丷亚𠆢口彡吕业𢆉亠土⿴井兴𰀁乀𠄎𠃋人七⿶乂之斤丆丘⿸𠂆 
千禾𠂉乙𠃍冫山乚幺下斗台占⿺田加巨石卯乎乛头舌次孚折辛甫沙也母𠦝所於者乞爫糸龟日十旱𤔔粦壹龴𠂊コ丁丂𠀁彑丌𫝀旦此厽𠃊几父文厂⿳了亦小冖𣅀但立朩乇执𧘇享单
亻力又九八乃匕㔾子士丈寸工刃勺弋上三义么门刄反少卬今中比月午牛介夭丰𬼖壬分互方公止予弔屯勿殳心亢尹及厄五支犬戈木夫友尤火云区卆个䒑韦专车牙见长仑仓为㝉尺
玄奴白古尒尼世半四令由申且司平以丕只㠯正甘未宁布去皮召氐主左右央本可必它示亼失弗乍句仁女冬尔用瓦𭕄卡包𫥞回各老夅合羊百名圭耳并吉艮危全兆交䏌吏刑先𫶧至亥
夷多夸光列寺米朱血有安聿牟而𠕁同宅式旬共舟衣如存夹覀再考尧贞则乔会齐妄农尽矢君呈辰坐丑刂𠬶呂局豆廷岑孛男孝更妥吳系足我求余狂吾夋邑良仌肖利甬完巠見宋否谷
希里免甹呆刖矣夾言吴弟車寿志严两丽来佥府和具非戔表叔肥奉亞奄备育欣卑虎長知幷咎肴卒兩宛來忩固官咅典門到炎屈垂幸朋奇其周京昔隹昌疌放直空宗居兒侖卓委果松夌
昆東事奔武奈采㑒责耶舍妾英爯前匽耎重春叚曷韋禹屏若是畏扁風昜屋咢皆省品帝臿亭背枼皇要甚秋音酋建胥奓柴負畐待怱面咠哀契盾思耑則貞禺俞兪攸娄為贲鬼叟虒素尃原
茸栗辱員冓馬旁唐高桀奚扇兼隺倉畜𠈌容䍃𦐇差翁竝家泰党骨宾难參累崔庸曹悤崩從敖專區責戚𬀷爽竟祭𡕩𦰩章頃焉帶悉婁票連翏曼吅貪攵動巽象善喬貴尊彳菐喜勞敞尞登孱
爲幾番惠舜替單堯就賁閒矞惡焦朁童棘舛粟間畺黽葉禁賈喿辟豊愁愛塞義雋農亶意當敬睘會僉楚詹敫𡕰粲賓㬎需臺壽齊監疑盡遣夢舞寧榮爾賞巤畾慮廣暴賣麃賛質憂豪親歷駦
龍諸毚襄麗羅贊難黨嚴纍囊儿𠫓凶兄旧臼凹六允兌元克𫩠毛厘入𰆊龷𫠩叱𦍌𬎿𠮛異展𠂇㐅𦉫冉冃𠀎与皀豕豖取兔攴林舄马水夬犮民东争束妻爭金咸垔豈冥斯睪禀稟𠘨尸夂巾𣄼
任岂屮叹丵𠃌刀彐气丹开𠚪歹贝冈衤册另戋𢀖亘刅朶杀朿岁朵貝肙呙𥝢易岡录叕斉乘度咼害荅彖𠩺巢厥畫蜀廉豦歳蒦鼻靡蠡屬万手厉𫇦𰃮后匡每员卷坴孟革冒𰮤𤇾莫埶劦萬灬
熏厲雚亾亡夕缶𡿺⿷匚久甲玉弁匸壯贵淮算瞿川廾化䜌臣卩𠂋𠂎厃卪𦈢丞桼圡龙尨𤽄泉相厌秝夏堇猒𠪚厭大厸𤰔㣺爱逮丩双𰀉尗𰁜𠬝叒冝睿𠤎刁于𠔼史𰃦丫天巴厷引夨內欠孔
升无太历乌戹幼瓜号匝他出处永付打亏自关灰戌休冎因伊西匈𢦏地𠂢向艾达毕年华行弄赤那何牢别寽亨秀角含延酉亜走狄麦末贡劳奂冷即羌念析忽厓乳肯冏阿匋臽启拉青卦齿
国罗岩的波定郎肃弇客南昱剌侯州軍奐爰壴卽胃宣亮冋食約威苗奎急告臭邕貢益朔茶盍桑烏耆鬲蚩皋索海𧴪秦聂恩拿羗通畢庶欶族啇⿲梟崖戛虖彗國旨虚得麻麥勒都堂野婴徙
密華買然最彭肅属朝臯無㽞覃黑絜敢敦翕皐虛琴禽尋歯鲁絲䧹達歲雍虞道葛歆新翠翟蒿對察魯慧齒樂墨黎劉㓁摩燕盧閻頻霍磨戲嬰遂罒頁爵聶雜離獻蘭覽巳囗龱才或貟𬙙袁書
啚兀己广𠃓氏爪巛龸圥穴斥卢代𠂤伏伐守𠧗当㐫邦役夆成花步时阜尚隶丸帚泥臤斩岸罙突龹柬保敄恆㚇垚眉界封罡巷荒段弯既脊時冡𡨄艹追眞恭舀真射留朗逢鹿鹵斬執旣郭將
商乾啬梁尉隊曾發盛隋雲著嗇𣪠貇殿𦥯㐮漸蓋曇遺褱圣霸彎丬爿𠃜吋㐄夒生外寅弓电𡗗卉镸明𦣻務将奞奢冘夗乏𠂔䏍幵戎尾兵弦帛匊忝昏𣶒㸒画审柔美亲巸某胡昷芻𣬉息般𥁕
疾弱旋殹康匿規常敕雩敝閑戠須董與賏綿審興霜霝闌韱雙巂宀耂皿好兹卵薛弘𤴓𦣞作妟釆宓𫲽𪧇丙侵㼌貫臬豐叵身尖尢尣监吊死雨復寮尿风𦉰𠬤圶企邪犭宏沓函甾施律查𣥂荣
科竒屾屵推鳥習配隆欽業戢解罪微截㥯𢧵營歸顛𡿨巜辶功㐬凡卅丗晃景掌蒙蔑節憲𡭕𫢉𢆶发𬎾臾叜部尌屠庫鮮雝廴囬弍𠬢虽㐁哥矍氺𧰨寻产切㝵歨龰复犀𢛳㞷𰕎𣅽忄卞刍匆戉
术对亙巩囟㓞在𠫤兊军芒坒困戒吝医串囱兑壳坚戾季罔店贯星昬勃衍勇𣪊隻䀠草孫氣圂蚤殷能敏造虍㒼堅眷欲舂備閔感勤赖滿養敷韯瞢賴縣冀戊癸盈晋䖒扌卂叉仒片勾幻宂㐱
㐌龵広兰𡿪曳过羽圼岳受底夜制肩命庚参訇削览𫥎恒島屖隽窄罢𡨝殺宿率离虘殸牽畧閏牚散答叅毳着過雷虜奧献数頡罷數適樊蔡輦嬴舉赞蹇矛㡀学陳學玨阑倝𠁁㡭𭤨厼巿疋旡
㞢𡗜𢼄昍政往尭晏厤費晶署羲曰曲㚘兓肉屰囧兮冄㕣汞市夘乐色庄𠯑夲丣巵忍忌连灵秉囷服芬冗房卖劵並宜𠱠苦便亟香室飛屑𥁑羔宰匪虔隼衰庭埋𠳮竜寄患脩棥羕條黄基雪貳
越奠畱棠黃厨紫聖鼎剽楽銀箕蜜匱頗臱遷噩穌蕉龜蕭繇薄藏𡬠靈𠤕釒柰焱𣥖𠬛声巫㲋普氵亐丏囚尻目耒虫罕位条间芳畀彔沝黾鱼首斿眇哉拜𦚏盆奕炭狊㚅亯显畟師𡌥除𬜯唇許
袞魚屚𣳾覓莽張崇眾崑窒集路衆智猪筆森黍圍歰歮項零資㬅瑟暑亷慈僕維穀賔蒼瑩寫盤廛徵隨彌斂薦糞翼龠壘藍页𠔿吹闷冐穹芮炏昇㒸𣧄退閃宮雀移湯悶炙蟲爻㸚牜字雔𠕋讠
弥𤣩充𭻾法毒穿流荼渠進辡䖵丄𠄌亩佘𰢴彊𤴔疒𰀄虐愈鼠隱癶㳄𦥑酓𥃭𣦵𥃦迷鼓氷仝卤珀逆崙賢礻㐭禸彧亀巧鸟聊款早亇𥫗㘝边把助快孤刺洗洪烝𮅕逐軟錢歛邊𣦼𦓔量籴𢆰糹
龶札怠惢煞蓬纟网𣎆阝𦘒𫧇刕旅乑𠫔卝艸乡仍匹仕印江𦫸收巟戍宇杜沈杏忘旲姑杲近𦭝洛活姜勉枲盇茂派浪浦納席倍徒修問清悲廌聚臧磊閵饣䖝劫甸𭑈㡿赦梨歇辥亍钅𩠐𩵋𠮷
尓奭嶲訁㠩咨誩衛衞彦丮豸皃毌𠀐𠦄猋兟雁忠𧾷却䙴燮應奏𦔮𡰪𰀠卣㖾盎丐灭沃送祖𧴲峯開寬覧匀丢𫔭强𠁣敗遀𠇍倠𮥼务韭𥘈秃𩙿飠號羞户髟鬥鬯𩰲甶箴𠔉眔笠𠚣黹𠂡佳亰格
浮𭗼灷絫寒剡竹乖吞汝幽矦歪笑破鄉究勻孕𠂬带信戀㫐𠚤兇枝嵬凢侈弜𤰇㣇戶囙盖叐致處等疊𥇛亓羸㫄盃𠧪圅朕速壺藥祟弃𣏋承厚凾鳳曩炅苟計班羣耷芺莘遲𰥍淡吂㪅薰富提
𤕨𭀰𡉊㷠形㫺毁𠂭𪩲𩫏者㗊匂𤰞𦥔強𠂈𠀃丛𭁈夊𰀪𠂹飞乆杳𠃎使廾丱𠬞𢌿泣㢲卻仐𡍮𠷎歺ユ屡𬺻𤊽眼瞏堆畨𤐫㬥𣍘哲𠕻床靣𪠲𡷈𦉪已烈𡗓𠧒㕛𡉵粵巢初𠃔�𮊿黒黒羍𡘆渚㒵彼 
𦙃𫩏枚伯𣌢𡘤𢾕苔乜𠂛叩㞋𡉀𠃬𥘅夻𢑑托対礼𢦒改妙忿㚔𢼂𢏚癹苓看起斊㝡閉望產深啻減䪞落碎群屢㼲𦎧䝿篤霞齋𪉷𬼉𡏳圓𠕀𥃩㢴𧆞彥𠚏养毫皷𨸏𡧱𠄢𨾴宝叀𦥚𢙣菊�㞤㞤盒 
𡰥𡰱降屎芔𡸁𢀩㫒𣏼𣁋針叏牧卧貧𣏐辵𨐌篭爕𮍏雐点𠦪𦍋𦬅短𣐩葵䖍菆𡗢埀𥇡歴候莆膚産𬜠羡㫖𡖅奥細罓𦬠萑虗𡭽リ夐𪟽恶𬴘独𭅰𰀡𰯲𰀢𰀈')
[I 230410 01:13:10 Goujian:56] 0 -> 2321
[I 230410 01:13:10 Goujian:63] epoch:1
[I 230410 01:13:10 Goujian:43] (2442, '⿱丶艹干肀一⿰丨丁丄丅丆万三下丌⿻刀丕丗丙丛丞王厶北⿵帀凵丢两並个丫中彡串吕丿丵主⿴井兴𰀁乂乃乆乇么义丷乏斤丘乔
⿸𠂆冂乖乘乞⿹𠃍冫山乚幺乙斗台占⿺田加巨石卯乎乛头舌次乳折辛甫沙也母𠦝所於氵者乾爫糸亀十旱𤔔粦壹了亇予争二亍亏亐云互亓五亘亚此厽亡亢交亥产亨亩亦乁享京亭
亯亰亠但亲⿳口冖执𧘇单且亼𠆢亾亻仁力厂人又卜九八几介仌仍从仐仑仓子仕他丈付工仝刃千勺代小上门刄反少卬今比月午牛夭丰𬼖任分方公企弔屯勿殳心伊及厄支伏伐休不
夫友尤火会区卆䒑韦专车牙见𠂉长文为㝉尺玄奴伯古尒尼世半四令由申司平以只㠯正甘未宁布去皮召位氐左右央本何必它佘余失弗作句女冬尔用瓦佥卡包𫥞回各老夅合羊百止
名佳耳并吉艮危全兆䏌使刑先广𫶧至來夷侈夸光列寺米朱血有安聿牟而侖同宅式旬共舟衣如存夹覀再考尧贞则齐妄农尽侯君呈辰坐丑刂侵呂局豆廷岑孛男孝便妥吳系足我求狂
吾夋邑良肖利甬完巠見宋否谷孚希里免甹保俞矣夾信吴弟車寿志严丽来禾府和具非戔表叔肥奉亞奄备育欣卑虎長知幷咎肴卒兩宛忩固官倍典門到炎屈垂幸朋奇其周倝昔倠昌疌
放直空宗居兒卓委果松夌昆東事奔武奈采㑒责耶舍匕页妾英爯前匽耎重春叚曷韋禹屏若是畏扁風昜屋咢皆省品帝攵臿背枼皇要甚秋音酋建胥奓柴負畐待怱面咠哀契盾思耑則貞
禺兪攸处日娄為贲龸鬼叟虒素𡗜目尃原茸栗辱員冓馬旁唐高桀奚扇兼隺倉畜𠈌容䍃𦐇差翁訁寸竝家泰𢦏党骨宾讠难參累崔庸曹悤崩從敖專區責戚𬀷爽竟祭𡕩𦰩章頃焉帶悉婁票
連翏曼僉貪動巽象善喬穴貴尊僕喜勞敞尞欠登孱爲幾番惠舜替單堯就賁閒矞惡焦朁童棘户隹舛粟間畺黽葉禁賈喿辟豊愁愛塞義雋農亶意當敬睘會楚詹敫𡕰粲賓㬎需臺壽齊監疑
盡遣夢舞寧榮爾賞巤畾慮廣暴賣麃賛質貝易憂豪青親歷駦龍諸毚襄麗羅贊難黨嚴纍囊儿兀允元兄充兇兊克兌旧兑凹六毛兟白厘𠃊入內兮𰆊兰兵兹叱养𬎿𠮛冀展冃冄内𠂇冈𦉫冋
于冗与军冝皀冡豖取兔冥攴林舄莫巾马水夬冷犮民东束妻爭金咸垔豈斯睪禀稟凡凢𠘨尸夂木𣄼岂凶⿶土出凾刅切刍气丹戈刕刖初册勹别戋𢀖圭朶制杀刺岁朵肙削剌术呙𥝢咅岡
录叕剡斉度咼害荅彖𠩺剽巢厥畫蜀廉豦歳蒦鼻靡蠡屬功务劦手助劫厉劳𰃮后匡勃每勉员卷坴孟勒冒贝𰮤埶龹萬灬熏厲彳𰕎雚勻勾匀匂匆夕匈匊匋身弓𡿺⿷匚久匝甲玉弁匸壯匪
曰贵淮匱大算雈臼瞿卄卅升卉廿华卖南𭕄䜌卞卦卧卪卩𠂋㔾却卵多𦈢卽桼厃历圡厌乍龙缶厓尨厚泉相厤夏厨堇厭𠪚厷厸厼叀参叅爱逮叉双丩叏叐叒𰀉受𰁜叜𠬝示睿另叩可叵号
叹刁吂吅吊吋吏向尹吝吞犬巴化含引吹孔告无艹太乌戹冉幼瓜命旦永打咨自关灰因西哉地𠂢艾达毕年行纟弄哥赤那牢哲寽更秀言角延酉亜走狄𠬶麦末贡扌𭕆七奂即阝𡰯羌念析
忽肯商阿問臽启拉啬齿国罗岩的波定郎肃啻弇客昱州軍奐爰胃宣亮食約威苗奎急士臭嗇邕貢益朔茶盍桑烏耆鬲𠕁蚩皋索海𧴪秦聂恩拿父羗通畢庶欶族啇⿲梟壴崖戛虖彗國𫩠旨
虚得麻麥都堂野婴徙密華買然最彭肅属朝臯無㽞覃黑絜敢敦翕皐虛琴菐禽尋歯鲁絲䧹達歲噩𥫗巫雍虞道葛歆頁新翠翟辶眔蒿對疋察龰魯慧齒臣樂墨黎劉革㓁𠀎摩燕盧糹閻頻霍
磨戲嬰遂罒爵聶雜離虫蓺穌曾獻蘭㓞覽巳囙囚囗囟才囧困囷圂圅圍貟𠔉己𬙙袁圓書啚圣圥川圶𠃓圼氏坒爪巛斥矢立卢𠂤垚守𠧗当㐫邦役埀夆埋成花步时冏或阜尚隶執基帚泥堅
堆斩岸罙突柬敄恆㚇眉界封罡巷荒段弯既脊𤇾時死追眞恭舀真射留朗逢鹿鹵斬丸旣郭將梁尉隊發盛隋忄雲著𣪠貇殿𦥯㐮漸𣦻蓋壘曇遺褱𢇇畕霸彎丬声业夒外夗夘歹彐夜生𠫓寅
夨天夲夻奏奕镸明奞奠𦣻奢務将𣶒奭好冘壬开妙爿妟𠂔姑姜䏍幵戎尾𠃑弦帛忝昏臤㸒丽画审柔美巸某胡昷芻𣬉息般𥁕疾弱医旋殹康匿規常敕雩敝閑戠須𡈼董與綿審興霜霝闌韱
雙巂孕字季孤学孫孖𢆶學薛宀宇宏宓弘宜宝𡗗室𦣞宮宰呆釆𥘅宿寄𡨄富𫲽皿𪧇㼌亅貫寫寮臬𤣩豐对寻対𤰔尌尓尖尗尣尢尭监尻尿屎屑屖屚屠屡屢復賏屰屵屾风岳𠬤𣅀邪峯犭崇
沓崑崙函甾施律查戌𣥂荣科钅竒嵬推鳥習配隆欽業戢解豕罪微截狺㥯𢧵營歸昇顛巜巟巧㐬巵巿市带師席旲晃景掌蒙蔑節憲𫢉幻幽広庄床底店庚发庫庭臾癶𢌬部侌異廛鮮𢛳雝廴
囬廾弃弋弍弜𠬢𦣝張強强㐁彊彌矍彔彑粉形彥彦彧彼往徒𤴓之犀㞷𣅽氺忌忍忘忠快忿怠戉𣎳巩恒𦍌在𠫤恶芒戒患壳坚悲悶戾罔惢牜贯星昬衍复勇𣪊隻䀠草氣蚤殷慈能㣺敏造㒼
眷欲舂備釒朿閔感勤應柕𬜯赖滿養敷韯瞢賴縣戀戍癸盈晋戶托卂仒片把宂㐱㐌拜𫠣𡿪曳过羽肩龵虍訇提览𫥎𠮦島隽窄罢𡨝殺率离虘殸牽畧閏牚散答毳着㚘過雷虜奧献数頡罷數
適樊蔡輦嬴舉赞蹇鼠𮅕收丂改政敗陳斂斊玨阑𠁁㡭𭤨斿旡早㞢昍显晏普𢼄晶智暑費署羲曩服肉朕札朩杏杜杳枚枝枲矛㕣汞柰乐色格𠯑丣连灵秉㝵棥森芬房劵𠱠苦亟香礻飛𥁑羔
虔隼衰𠳮竜脩羕條黄雪貳越畱棠黃紫聖鼎楽銀箕蜜頗臱遷慶蕉龜蕭繇薄藏𡬠靈𠤕款歇焱歛歨歪歮歰歴𠬛毁𧰨毋毫㐅氶氷汝江沃沈丏沝法泣洗洛耒洪活派曲流浦浪罕浮冗条间芳
畀淡深龶円清黾鱼渚減首眇𦚏盆𦙍炭狊湯㚅𡿧畟𡌥除𫇦唇許袞魚𣳾覓莽眾窒集路衆猪筆黍項零資㬅瑟亷維穀賔蒼瑩盤徵隨𣦼韭秃雨㓹薦糞翼龠藍兓廌欮𣎆鬯灭灷炅炏点𰃦烈𠂊
𠔿烝闷冐穹芮煞㒸𣧄退閃雀移燮炙爕蟲爻牧雔𠕋独猋猒弥𠂡珀𭻾毒穿荼渠進辡䖵產産电甶甸畨疊𤴔疒𰀄虐愈隱癹皃㿟皷盃盇盎盒盖㳄𦥑酓看眼迷瞏鼓矦短破卤碎逆磊賢礼祟卸
禸秝𤽄究鸟聊㐄𦉪竹笑㘝笠边等箴篤篭逐コ軟飠錢邊籴𦓔量絫𰥍蓬网罓羍羡羣群羸耂耷丱旅膚茂臧乑𫝀艸卝芔乡芺匹苓苔苟印莆莘菆菊杲近萑𦭝落奻葵㝴納修𭁵薰豸聚豙藥躬
閵𩵋𥘈處虗號虽饣𭑈㡿赦梨辥𠃎𫠩衛衞𩠐衤𦫳𬗌䖒嶲計㠩誩丮貧雁𠌵𧾷𣂑䙴𡩧奋𦀺𦔮辵送卣速𠂈𰀠遀遲㖾䚻鄉針丐史夊祖𧴲開寬覧𫔭閉龟降𠓜𠇍雐屮𮥼霞靣㐭𩙿羞𥑟𦬇髟鬥��虱鳳黒黹齋戊龱龷𭗼寒㒵𦉰𢆰㕛𣦵㗊𰧭㚔㲋𠂬㝡㫐㞋㠭㞤𠚤㢲㢴㡀𤰇㣇𠔼致㪅𥇛㫄㫒㫖㫺㬥𠧪壺𠧢𣏋承𫪡㷠𰀪㸚𠽸㼲𢎘班𠚣𤕨䖍𥱡𭀰䝿𥃦𡉊𬟩𠂭䪞𪩲𩫏亙𠂎毌𠄌乀𠃌者𤰞𠦄廾
𦥔直𧮫𠀃𠀐𠫔𭁈𠂛𢆉𠂹𠃔飞𠄢哭𠃜龴冎𠬞𥃭𪟽𢌿卻𰀡𡉚𡍮𠷎歺ユ芚𬺻匍𤊽𢨋𤐫𦦉𣍘䡛𠃋𠕻𪠲𡷈𠕀𠤎已𡕒𡿩𮍌𡗓䖝𠀆𠚏𠣏𠚪𠧒𡉵𠁣粵𭅰巢𫩏𡰪𭆆𮊿𡘆𠥓𦙃𠧧𣌢𠯃𡘤𢾕乜𢑚囱𡉀𠃬
𠮷凸𠃨𢑑𠄎𢦒𡿨𢼂起𮓗望𢏚𧆞軎𡭽𦎧隡𰯲𪉷𬼉𡏳𥃩卥氾凷𨸏𡧱𡖅𡗢𨾴𫀄𠦜𦥚𢙣𢎨𧵩莧𦉼珎𬯁𢊁𠦑卨𣐩𠔽𦫸𡭕𡰥𡰱𠮠𡸁𢀡𢀩𣏼𣥖�𣁋𥸲昗昗𠫯𣏐𨐌𮍏𫧇㕚𠦪炗𣏟𦍋𦬅䂞𢇁戼𤬦鹽 
馮𬎾𫟯𥇡𦘒𠔥𨺅𠀁𬜠熊候𧖧孑奥細𦉬𦬠𭀖𭇁豩リ夐𰀢𬴘ス𠔥𠆥〾𰀈𰋙')
[I 230410 01:13:10 Goujian:56] 2321 -> 2442
[I 230410 01:13:10 Goujian:71] ('giveup 91', 'αℓ〇㐆㐧㔽㕟丝书卐枣桌臦女既𛂦𠀍𠂂𠃉𠃛𠄏𠄘𠕄𠖼𠘧𠘽𠙖𠣧𠥻𠧚𠧸𠪕𡕫𡖈𡗫𡚇𡧧𡭔𡰣𢄉𢤧𢼾𢽋𢿝𣇓𣦶𣫬𤉷𤊱�𤴐𤵶𥆞𥛓�𥸦𦉭𦏲𦥓𦥙𧇩𧯽𨈐𨙨𨤐𨳇𪚴𪚾𬺷𬻇𬻞𭀠𭁭𭂬𭔥𭙌𭣔𭨘𭭧𭴺𭺛𭾛𮙲𮠕勤即周㣇育𰀫𰀰𰆄')
"""

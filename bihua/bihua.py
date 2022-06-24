# http://yedict.com/zsdispUni.asp?xu=11
BiHua1 = "㇀㇁㇂㇃㇄㇅㇆㇇㇈㇉㇊㇋㇌㇍㇎㇏㇐㇑㇒㇓㇔㇕㇖㇗㇘㇙㇚㇛㇜㇝㇞㇟㇠㇡㇢㇣ "
# 31C0—31EF 中日韩笔画

BiHua = ''.join(chr(x) for x in range(0x31C0, 0x31EF+1))
print(BiHua)
with open("BiHua/BiHua.txt", 'w') as f:
    for x in BiHua:
        f.write(x+'\n')

# ㇀㇁㇂㇃㇄㇅㇆㇇㇈㇉㇊㇋㇌㇍㇎㇏㇐㇑㇒㇓㇔㇕㇖㇗㇘㇙㇚㇛㇜㇝㇞㇟㇠㇡㇢㇣㇤㇥㇦㇧㇨㇩㇪㇫㇬㇭㇮㇯


def read_ids(path):
    doc=[]
    with open(path,encoding="utf-8") as f:
        # U+6717	朗	⿰⿱丶⑤月[GTJV]	⿰良月[K]
        for line in f:
            if not line or not line.startswith('U+'):
                continue
            line = line.strip()
            # line="U+2EBC9\t𮯉\t⿰齒⿱人米\t⿰齒籴"
            tokens=line.split('\t')
            char=tokens[1]
            metas=[x.split('[')[0] for x in tokens[2:]     ]
            metas.sort(key=lambda x:len(x))
            # meta=metas[0]
            # for i in range(1,len(metas)):
            #     if len(metas[i]) < len(meta):
            #         meta=metas[i]
            doc.append([char,metas])
    return doc 

doc=read_ids("chaizi/ids.txt")

print(len(doc),doc[0])

ids0={}
for cols in doc:
    k,v=cols[:2]
    ids0[k]=v[0]

# ids=[ cols[:2] for cols in doc ]


YuanZi=open("yuanzi.txt").read().splitlines()
YuanZi=set( x for x in YuanZi if x )

ChaiZi=[  ]
for k,v in ids0.items():
    if k in YuanZi:
        v=k
    ChaiZi.append((k,v))
ChaiZi.sort(key=lambda x:x[0])

with open("chaizi.txt","w") as f:
    for x in ChaiZi:
        r='\t'.join(x)
        f.write(r+'\n')
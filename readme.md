# 汉字 Hanzi

一些汉字表
some database of Hanzi

## usage
as HanZi database of below

* "UnicodeTokenizer"(https://github.com/laohur/UnicodeTokenizer)
* "ZiCutter"(https://github.com/laohur/ZiCutter)
* "ZiTokenizer"(https://github.com/laohur/ZiTokenizer)


##  笔划
BiHua.txt
36个

## 部件
BuJian.txt
1091个

## 独体字
DuTiZi.txt
813个

## 元字表
为笔划、部件、独体字并集
YuanZi.txt
1719字

## 异体字
YiTiZi.txt
42514字

## 拆字表
ChaiZi.txt
94283字
拆分至下一级


## 常用字
ChangYongZi.txt
8664字

## 基字表
为元字、常用字并集
JiZi.txt
9616字

## 合字
HeZi.txt
94290字
指定基字字典，拆分至基字(默认JiZi.txt)
拆字原则：
* 首先异体字转正
* 若字在基字典中，不拆，否则拆分至基字典
Base.txt 与 JiZi.txt 互相印证

## 下一步
* 汉字属性表
* 汉字排序（暂以unicode排序，应以笔画、部件、独体字、合字以部首部件排序）


## 用途
* 活字编码
* 拆字，缩小基字典
    - 结构符+首个基字+基字
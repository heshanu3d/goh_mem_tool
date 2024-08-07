# tool for analyzing memory of goh

## how to use
```
python mem_searcher.py 76E426FAC4
```

## preview
```
D:\code\python\goh_mem_tool>python mem_searcher.py 76E426FAC4
0x76e414d000
0x122ac4
seq at addr 510633900740: 0000000007
seq at addr 510633900740: 0x00000007
find seq = 1 success, ofs: 0x122704, addr: 0x76e426f704, try_cnt: 6
请选择模式:
    i:  交互模式
    f:  快速模式
    d:  dump模式
    s:  查找模式
    q:  退出
#root> select mode and enter:  

```

### interact mode
```
select mode and enter: i
进入交互模式:
    h/help : 帮助
    rd/read: 读取指定地址
    q: 退出
#interact> help
rd 7c8f
read 7c8f
#interact> rd 7c8f
addr 0x76e4267c8f, val        0x0            0
#interact> q
```

### fast mode
```
select mode and enter: f
进入快速模式:
    n : 向后查找
    p : 向前查找
    q : 退出
seq =           1, cnt =           1, type =   237597971, info:unknown         , addr: 0x76e426f704
seq =           2, cnt =           1, type =    12020638, info:unknown         , addr: 0x76e426f7a4
seq =           3, cnt =           1, type =    35877812, info:unknown         , addr: 0x76e426f844
seq =           4, cnt =           1, type =    26787097, info:unknown         , addr: 0x76e426f8e4
seq =           5, cnt =           1, type =   116415794, info:unknown         , addr: 0x76e426f984
seq =           6, cnt =           1, type =   155230886, info:unknown         , addr: 0x76e426fa24
seq =           7, cnt =         600, type =    86760257, info:unknown         , addr: 0x76e426fac4
seq =           8, cnt =          80, type =   261692565, info:unknown         , addr: 0x76e426fb64
seq =          22, cnt =         320, type =    93779722, info:宠物岛扫荡币    , addr: 0x76e426fc04
seq =          23, cnt =         290, type =   158846155, info:祭坛扫荡币      , addr: 0x76e426fca4
seq =          24, cnt =         119, type =    50363169, info:符文扫荡币      , addr: 0x76e426fd44
seq =          25, cnt =          80, type =    58788201, info:战役扫荡币      , addr: 0x76e426fde4
seq =          26, cnt =          39, type =   123168583, info:地宫扫荡币      , addr: 0x76e426fe84
seq =          27, cnt =           3, type =   250006855, info:unknown         , addr: 0x76e426ff24
seq =          28, cnt =          85, type =     9211505, info:钻石代码        , addr: 0x76e426ffc4
```

### dump mode
```
select mode and enter: d
dumping...
    h/help : 帮助
    q: 退出
#dump> q
```

### search mode
```
select mode and enter: s
进入查找模式:
    h/help : 帮助
    seq=2:  查找seq=2的条目
    cnt=3:  查找cnt=2的条目
    type=3: 查找type=2的条目
    q: 退出
#search> help
单条件查找:
    seq=2:  查找seq=2的条目
    cnt=3:  查找cnt=2的条目
    type=3: 查找type=2的条目
多重条件查找:
    type=3 if seq=2: seq=2且type=2的条目
    cnt=2 if type>1000: cnt=2且type>1000的条目
    seq<1000 if info!=unknown: seq<1000且info已知的条目
#search> seq<1000 if info!=unknown
seq =          22, cnt =         320, type =    93779722, info:宠物岛扫荡币    , addr: 0x76e426fc04
seq =          23, cnt =         290, type =   158846155, info:祭坛扫荡币      , addr: 0x76e426fca4
seq =          24, cnt =         119, type =    50363169, info:符文扫荡币      , addr: 0x76e426fd44
seq =          25, cnt =          80, type =    58788201, info:战役扫荡币      , addr: 0x76e426fde4
seq =          26, cnt =          39, type =   123168583, info:地宫扫荡币      , addr: 0x76e426fe84
seq =          28, cnt =          85, type =     9211505, info:钻石代码        , addr: 0x76e426ffc4
seq =          29, cnt =   208275846, type =   108683766, info:金币代码        , addr: 0x76e4270064
seq =          30, cnt =        3200, type =   253523487, info:龙舟皮肤代币    , addr: 0x76e4270104
seq =          31, cnt =        6823, type =     5847011, info:魔能            , addr: 0x76e42701a4
seq =          32, cnt =          17, type =   168343128, info:洞窟钥匙1-1     , addr: 0x76e4270244
seq =          39, cnt =           5, type =   145648075, info:传说代币        , addr: 0x76e42706a4
seq =          40, cnt =         300, type =   132262301, info:竞技场代币      , addr: 0x76e4270744
seq =          43, cnt =          15, type =   137602091, info:洞窟钥匙2-1     , addr: 0x76e4270924
seq =          44, cnt =           1, type =   231518889, info:洞窟钥匙1-2     , addr: 0x76e42709c4
seq =          46, cnt =          32, type =   151744750, info:洞窟钥匙3-1     , addr: 0x76e4270b04
seq =          48, cnt =          26, type =   177694137, info:洞窟钥匙1-3     , addr: 0x76e4270c44
seq =          49, cnt =          39, type =    61267793, info:洞窟钥匙2-2     , addr: 0x76e4270ce4
seq =          50, cnt =          60, type =   189664262, info:洞窟钥匙5-1     , addr: 0x76e4270d84
seq =          55, cnt =           4, type =   264970127, info:洞窟钥匙4-1     , addr: 0x76e42710a4
search end
```
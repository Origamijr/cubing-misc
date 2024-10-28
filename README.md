# Cubing Stuff

Just some miscellaneous cubing stuff I coded in a rush. I know cubing libraries exist, but for my purpose, I thought it'd be faster to just code a cube than to use an existing library. The base code was made in 2 days and prioritized minimizing number lines, so give me some slack for messiness and bad coding practices.

## 3BLD

- Letter sequence finder for 3-style using weak swapping
- Letter sequences for breaking into twists/flips (see [write-up](tex/3bld_trace.pdf))

Example scramble and solve using just letter sequences from memorization
```
cube, s = Cube3().scramble(seed=1)
print(s)
print(repr(cube))
mem = speffz_sequence(cube, verbose=1)
print(mem)
print(repr(execute_sequence(cube, mem['edges'], mem['corners'])))
```
Output
```
D' U2 D2 R2 B U2 D2 R' U' R2 D' U2 D U' L B' D2 U' F2 R'
    ORG
    OWB
    BRG
WWO WWO YWR WYG
YOB YGB RRO GBO
WGY GWB OGB YBR
    RGY
    RYY
    BOR
unchecked ['UBR', 'UFL', 'RDF', 'FDL', 'RDB', 'UBL', 'BDL'] sequence [] twisted [] buffer C
unchecked ['UBR', 'UFL', 'RDF', 'RDB', 'UBL', 'BDL'] sequence ['L'] twisted [] buffer C
unchecked ['UBR', 'UFL', 'RDB', 'UBL', 'BDL'] sequence ['L', 'K'] twisted [] buffer C
unchecked ['UBR', 'UFL', 'RDB', 'UBL'] sequence ['L', 'K', 'S'] twisted [] buffer C
unchecked ['UFL', 'RDB', 'UBL'] sequence ['L', 'K', 'S', 'N'] twisted [] buffer C
unchecked ['UFL', 'RDB'] sequence ['L', 'K', 'S', 'N', 'D', 'R'] twisted [] buffer D
corner sequence ['L', 'K', 'S', 'N', 'D', 'R', 'I'] twisted ['DBR']
twisted sequence [['T', 'W']] parity True parity twist 0 adjusted letter I
corner sequence ['L', 'K', 'S', 'N', 'D', 'R', 'I', 'T', 'W']
unchecked ['UB', 'UR', 'UL', 'FR', 'FL', 'DR', 'DL', 'DF', 'BR', 'BL', 'DB'] sequence [] twisted [] buffer C
unchecked ['UB', 'UR', 'UL', 'FR', 'FL', 'DL', 'DF', 'BR', 'BL', 'DB'] sequence ['A', 'O'] twisted [] buffer A
unchecked ['UB', 'UR', 'UL', 'FR', 'FL', 'DL', 'BR', 'BL', 'DB'] sequence ['A', 'O', 'K'] twisted [] buffer A
unchecked ['UB', 'UL', 'FR', 'FL', 'DL', 'BR', 'BL', 'DB'] sequence ['A', 'O', 'K', 'B'] twisted [] buffer A
unchecked ['FR', 'FL', 'DL', 'BL', 'DB'] sequence ['A', 'O', 'K', 'B', 'Q', 'J', 'T'] twisted ['UL'] buffer J
unchecked ['FR', 'DL', 'BL', 'DB'] sequence ['A', 'O', 'K', 'B', 'Q', 'J', 'T', 'L'] twisted ['UL'] buffer J
unchecked ['FR', 'DL', 'BL'] sequence ['A', 'O', 'K', 'B', 'Q', 'J', 'T', 'L', 'W'] twisted ['UL'] buffer J
unchecked ['FR', 'DL'] sequence ['A', 'O', 'K', 'B', 'Q', 'J', 'T', 'L', 'W', 'H'] twisted ['UL'] buffer J
unchecked ['FR'] sequence ['A', 'O', 'K', 'B', 'Q', 'J', 'T', 'L', 'W', 'H', 'X'] twisted ['UL'] buffer J
edge sequence ['A', 'O', 'K', 'B', 'Q', 'J', 'T', 'L', 'W', 'H', 'X', 'P'] flipped ['UL']
flipped [['D', 'E']] last letter J
{'corners': 'LK SN DR IT W', 'edges': 'AO KB QJ TL WH XD EJ'}
    WWW
    WWW
    WWW
OOO GGG RRR BBB
OOO GGG RRR BBB
OOO GGG RRR BBB
    YYY
    YYY
    YYY
```
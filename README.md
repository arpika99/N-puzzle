# N-puzzle

Az A* algoritmust használva oldja meg a 8-as (n-es) kirakójátékot.

#Opciók
A programot a parancssor argumentumain keresztül tegye konfigurálhatóvá. Kapcsolók:
1. –input <FILE>: a kezdeti állapotot tartalmazó állomány neve. Ha a kapcsoló hiányzik, a standard bemenetr˝ol
olvassa be a kezdeti állapotot.
2. –solseq: a standard kimenetre írja a teljes megoldási szekvenciát
3. –pcost: a standard kimenetre írja a megoldás költségét
4. –nvisited: a standard kimenetre írja a meglátogatott csomópontok számát
5. –h <H>: a heurisztika típusa. Ha H=1, használja a „rossz helyen levő csempék száma” heurisztikát. Ha
Ha H=2, használja a Manhattan heurisztikát.
6. –rand <N> <M> egy véletlenszer ˝u, N méret ˝u állapotra oldja meg. M a véletlenszer ˝u
tologatások számát jelenti.

#Végső állapot
1 2 3
4 5 6
7 8 0

#Kezdő állapot
1 8 7
3 0 5
4 6 2

#Ha h = 1
Meglátogatott pontok száma 2597
Költség 25

#Ha h = 2
Meglátogatott pontok száma 5115
Költség 25

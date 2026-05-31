import sys

cur_pal = None
cur_cont = 0

for linea in sys.stdin:
    linea = linea.strip()
    if not linea:
        continue
    
    parts = linea.split('\t')
    if len(parts) != 2:
        continue
        
    pal, cont = parts
    try:
        cont = int(cont)
    except ValueError:
        continue

    if cur_pal == pal:
        cur_cont += cont
    else:
        if cur_pal:
            print(f"{cur_pal}\t{cur_cont}")
        cur_pal = pal
        cur_cont = cont

if cur_pal == pal:
    print(f"{cur_pal}\t{cur_cont}")

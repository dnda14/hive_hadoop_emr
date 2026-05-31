import sys

cur_pal = None
cur_ids = set()

for linea in sys.stdin:
    linea = linea.strip()
    if not linea:
        continue
    
    parts = linea.split('\t')
    if len(parts) != 2:
        continue
        
    pal, block_id = parts

    if cur_pal == pal:
        cur_ids.add(block_id)
    else:
        if cur_pal:
            ids_str = ",".join(sorted(list(cur_ids)))
            print(f"{cur_pal}\t{ids_str}")
        cur_pal = pal
        cur_ids = {block_id}

if cur_pal == pal:
    ids_str = ",".join(sorted(list(cur_ids)))
    print(f"{cur_pal}\t{ids_str}")

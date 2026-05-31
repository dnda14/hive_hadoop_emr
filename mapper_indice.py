import sys

for linea in sys.stdin:
    linea = linea.strip()
    if not linea:
        continue
    
    if linea.startswith('"') and linea.endswith('"'):
        linea = linea[1:-1] 
        parts = linea.split('","')
        
        if len(parts) >= 2:
            block_id = parts[0]
            texto = parts[1]
            
            pals = texto.split()
            unico_pals = set(pals)
            
            for word in unico_pals:
                print(f"{word}\t{block_id}")

import sys
import re

for linea in sys.stdin:
    linea = linea.lower()
    linea = re.sub(r'[^a-záéíóúñü0-9 ]', ' ', linea)
    pals = linea.split()
    for pal in pals:
        print(f"{pal}\t1")

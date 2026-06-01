import sys
import re
import os
import uuid

def clean_texto(text):
    text = text.lower()
    text = re.sub(r'[^a-záéíóúñü0-9 ]', ' ', text)
    return text

def main():
    buffer = []
    chunk_size = 2000
    
    task_id = os.environ.get('mapreduce_task_id', str(uuid.uuid4())[:8])
    counter = 1

    for linea in sys.stdin:
        clean_linea = clean_texto(linea)
        pals = clean_linea.split()
        
        for pal in pals:
            buffer.append(pal)
            
            if len(buffer) == chunk_size:
                text_block = " ".join(buffer)
                block_id = f"bloque_{task_id}_{counter}"
                
                print(f'"{block_id}","{text_block}"')
                
                buffer = []
                counter += 1

    if buffer:
        text_block = " ".join(buffer)
        block_id = f"bloque_{task_id}_{counter}_final"
        print(f'"{block_id}","{text_block}"')

if __name__ == "__main__":
    main()

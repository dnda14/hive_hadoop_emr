import boto3
import os
import sys
import threading
from boto3.s3.transfer import TransferConfig

REGION = 'us-east-1'
BUCKET = 'mi-bucket-emr-wimc-bigdata'

ARCHIVOS = [
    ('/home/dnda/Documents/hive_bigdata/datos_indice/novelas_unificadas.txt', 'input/novelas/novelas_unificadas.txt'),
    ('/home/dnda/Documents/hive_bigdata/datos_indice/textos_comentarios.txt', 'input/comentarios/textos_comentarios.txt'),
    ('/home/dnda/Downloads/wikipedia.txt/wikipedia.txt', 'input/wikipedia/wikipedia.txt'),
    ('/home/dnda/Downloads/corpus.txt', 'input/corpus/corpus.txt')
]

class ProgresoSubida(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                f"\r Progreso: {self._seen_so_far / (1024*1024*1024):.2f} GB / {self._size / (1024*1024*1024):.2f} GB  ({percentage:.2f}%)"
            )
            sys.stdout.flush()

def main():
    print(f" Iniciando subida al bucket s3://{BUCKET}...")
    s3_client = boto3.client('s3', region_name=REGION)
    
    config = TransferConfig(
        multipart_threshold=1024 * 25, 
        max_concurrency=10,
        multipart_chunksize=1024 * 25, 
        use_threads=True
    )
    
    archivos_subidos = 0
    errores = 0

    for ruta_local, ruta_s3 in ARCHIVOS:
        print(f"\n\n---------------------------------------------------")
        if not os.path.exists(ruta_local):
            print(f"❌ Error: No se encuentra el archivo {ruta_local}. Saltando...")
            errores += 1
            continue

        tamano_gb = os.path.getsize(ruta_local) / (1024*1024*1024)
        print(f" Archivo: {os.path.basename(ruta_local)} ({tamano_gb:.2f} GB)")
        print(f" Destino S3: s3://{BUCKET}/{ruta_s3}")
        
        try:
            s3_client.upload_file(
                ruta_local, 
                BUCKET, 
                ruta_s3,
                Config=config,
                Callback=ProgresoSubida(ruta_local)
            )
            print("\n✅ ¡Subida completada con éxito!")
            archivos_subidos += 1
        except Exception as e:
            print(f"\n❌ Ocurrió un error al subir {ruta_local}: {e}")
            errores += 1

    print("\n===================================================")
    print(f" Resumen final: {archivos_subidos} archivos subidos, {errores} errores.")

if __name__ == '__main__':
    main()

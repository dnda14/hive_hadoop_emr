import boto3
import os
import json
import glob

S3_BUCKET = 'mi-bucket-emr-wimc-bigdata'
DIRECTORIO_LOCAL = 'datos_hive'

def main():
    print("Preparando los datos de NYC Taxi Trips...\n")
    
    archivos_parquet = glob.glob(f"{DIRECTORIO_LOCAL}/*.parquet")
    
    if not archivos_parquet:
        print(f"❌ Error: No se encontraron archivos .parquet en la carpeta '{DIRECTORIO_LOCAL}'")
        return
        
    s3 = boto3.client('s3')
    
    for archivo_local in archivos_parquet:
        nombre_archivo = os.path.basename(archivo_local)
        s3_key = f'datos_taxi/{nombre_archivo}'
        
        print(f"Subiendo {nombre_archivo} a S3 (s3://{S3_BUCKET}/{s3_key})...")
        s3.upload_file(archivo_local, S3_BUCKET, s3_key)
        
    print(f"\n✅ Se subieron {len(archivos_parquet)} archivo(s) exitosamente a S3.")
    
    paths = {
        'INPUT': f's3://{S3_BUCKET}/datos_taxi/',
        'OUTPUT': f's3://{S3_BUCKET}/resultados_taxi_particionados/'
    }
    
    with open('emr_s3_taxi_paths.json', 'w') as f:
        json.dump(paths, f, indent=4)
        
    print("\n✅ Rutas S3 guardadas en 'emr_s3_taxi_paths.json'")
    print(" ¡Todo listo para lanzar el análisis en EMR!")

if __name__ == "__main__":
    main()

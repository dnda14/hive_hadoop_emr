import boto3
import json
import sys
import os
import datetime

# =================================================================
JOB_A_LANZAR = 'taxi_jobs/06_raw_filtro.q'
# =================================================================

def main():
    archivo_local = JOB_A_LANZAR
    
    if not os.path.exists(archivo_local):
        print(f"❌ Error: El archivo {archivo_local} no existe.")
        sys.exit(1)
        
    nombre_archivo = os.path.basename(archivo_local)

    try:
        with open('emr_cluster_info.json', 'r') as f:
            cluster_info = json.load(f)
    except FileNotFoundError:
        print("❌ Error: No se encontró emr_cluster_info.json. ¿Está el clúster encendido?")
        sys.exit(1)

    try:
        with open('emr_s3_taxi_paths.json', 'r') as f:
            paths = json.load(f)
    except FileNotFoundError:
        print("❌ Error: No se encontró emr_s3_taxi_paths.json. Ejecuta taxi_preparar_datos.py primero.")
        sys.exit(1)

    cluster_id = cluster_info['cluster_id']
    s3_bucket = cluster_info['s3_bucket']
    s3_input = paths['INPUT']
    s3_output = paths['OUTPUT']
    
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    s3_script_uri = f"s3://{s3_bucket}/scripts/{nombre_archivo}"
    
    s3 = boto3.client('s3')
    print(f"📤 Subiendo {archivo_local} a S3...")
    s3.upload_file(archivo_local, s3_bucket, f'scripts/{nombre_archivo}')

    emr = boto3.client('emr', region_name='us-east-1')
    
    step = {
        'Name': f'Analisis Taxi - {nombre_archivo}',
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                'hive-script',
                '--run-hive-script',
                '--args',
                '-f', s3_script_uri,
                '-d', f'INPUT={s3_input}',
                '-d', f'OUTPUT={s3_output}',
                '-d', f'FECHA={fecha_actual}'
            ]
        }
    }

    print(f"\n Lanzando Step en el clúster {cluster_id}...")
    response = emr.add_job_flow_steps(
        JobFlowId=cluster_id,
        Steps=[step]
    )

    step_id = response['StepIds'][0]
    print(f"✅ Step '{nombre_archivo}' enviado con éxito. ID: {step_id}")

if __name__ == "__main__":
    main()

import boto3
import json
import sys

def main():
    try:
        with open('emr_cluster_info.json', 'r') as f:
            info = json.load(f)
    except FileNotFoundError:
        print("❌ Error: emr_cluster_info.json no existe. Debes levantar el clúster primero con levantar_emr.py")
        sys.exit(1)

    cluster_id = info['cluster_id']
    bucket = info['s3_bucket']
    region = 'us-east-1'

    emr = boto3.client('emr', region_name=region)
    s3 = boto3.client('s3', region_name=region)

    print("Subiendo script de Hive (hive_indice.q) a S3...")
    s3.upload_file('hive_indice.q', bucket, 'scripts/hive_indice.q')

    input_path = f"s3://{bucket}/input_escala/csv_75/"
    output_path = f"s3://{bucket}/output/hive_indice_75/"
    
    step = {
        'Name': 'Job 4: Hive Indice Invertido sobre CSVs',
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                'hive-script',
                '--run-hive-script',
                '--args',
                '-f', f's3://{bucket}/scripts/hive_indice.q',
                '-d', f'INPUT={input_path}',
                '-d', f'OUTPUT={output_path}'
            ]
        }
    }

    print(f"\nEnviando Job de Hive Índice Invertido al clúster {cluster_id}...")
    try:
        response = emr.add_job_flow_steps(JobFlowId=cluster_id, Steps=[step])
        step_id = response['StepIds'][0]
        print(f"✅ Job enviado exitosamente. ID del Paso: {step_id}")
    except Exception as e:
        print(f"❌ Error al enviar el Job a EMR: {e}")

if __name__ == '__main__':
    main()

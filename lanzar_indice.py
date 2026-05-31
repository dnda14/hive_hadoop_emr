import boto3
import json
import sys

def main():
    try:
        with open('emr_cluster_info.json', 'r') as f:
            info = json.load(f)
    except FileNotFoundError:
        print("❌ Error: emr_cluster_info.json no existe")
        sys.exit(1)

    cluster_id = info['cluster_id']
    bucket = info['s3_bucket']
    region = 'us-east-1'

    emr = boto3.client('emr', region_name=region)
    s3 = boto3.client('s3', region_name=region)

    print("Subiendo scripts del a S3...")
    s3.upload_file('mapper_indice.py', bucket, 'scripts/mapper_indice.py')
    s3.upload_file('reducer_indice.py', bucket, 'scripts/reducer_indice.py')
    input_path = f"s3://{bucket}/input_escala/csv_100/"
    output_path = f"s3://{bucket}/output/indice_100/"
    
    step = {
        'Name': 'Job 2: Índice Invertido sobre CSV',
        'ActionOnFailure': 'CONTINUE', 
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                'hadoop-streaming',
                '-files', f's3://{bucket}/scripts/mapper_indice.py,s3://{bucket}/scripts/reducer_indice.py',
                '-mapper', 'python3 mapper_indice.py',
                '-reducer', 'python3 reducer_indice.py',
                '-input', input_path,
                '-output', output_path
            ]
        }
    }

    print(f"\n Enviando Job  al clúster {cluster_id}...")
    try:
        response = emr.add_job_flow_steps(
            JobFlowId=cluster_id,
            Steps=[step]
        )
        step_id = response['StepIds'][0]
        print(f"✅ Job enviado exitosamente. ID del Paso: {step_id}")
    except Exception as e:
        print(f"❌ Error al enviar el Job a EMR: {e}")

if __name__ == '__main__':
    main()

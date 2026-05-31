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

    print("Subiendo scripts de WordCount a S3...")
    s3.upload_file('mapper_wordcount.py', bucket, 'scripts/mapper_wordcount.py')
    s3.upload_file('reducer_wordcount.py', bucket, 'scripts/reducer_wordcount.py')
    input_path = f"s3://{bucket}/input_escala/crudos_100/"
    output_path = f"s3://{bucket}/output/wordcount_100/"
    
    step = {
        'Name': 'Job 1: WordCount sobre Archivos Crudos',
        'ActionOnFailure': 'CONTINUE', 
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                'hadoop-streaming',
                '-D', 'mapreduce.input.fileinputformat.input.dir.recursive=true',
                '-files', f's3://{bucket}/scripts/mapper_wordcount.py,s3://{bucket}/scripts/reducer_wordcount.py',
                '-mapper', 'python3 mapper_wordcount.py',
                '-reducer', 'python3 reducer_wordcount.py',
                '-input', input_path,
                '-output', output_path
            ]
        }
    }

    print(f"\n🚀 Enviando Job de WordCount al clúster {cluster_id}...")
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

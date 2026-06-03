# Proyecto de Procesamiento de Big Data en AWS EMR (Hadoop y Hive)

Este repositorio contiene los scripts, automatizaciones y configuraciones necesarias para desplegar, ejecutar y analizar trabajos de Big Data utilizando un clúster de Amazon EMR. 

El proyecto está estructurado alrededor de dos casos de uso principales:

---

## Infraestructura del Clúster

Todos los experimentos y procesamientos descritos en este repositorio fueron ejecutados sobre un clúster de AWS EMR compuesto por 5 máquinas en total:
*   **1 Nodo Master:** Instancia `m4.large` (8 GB de RAM, 2 vCPUs) que actúa como orquestador y NameNode.
*   **4 Nodos Core (Workers):** Instancias `m4.large` (8 GB de RAM, 2 vCPUs cada una) encargadas de almacenar los datos en HDFS y ejecutar las tareas de procesamiento.

---

## 1. Comparativa de Rendimiento y Desarrollo: Hadoop vs. Hive

La primera parte del proyecto tiene un enfoque educativo e investigativo. Su objetivo es contrastar el paradigma clásico de programación imperativa de **Hadoop MapReduce** (utilizando scripts en Python) frente a la abstracción declarativa (basada en SQL) que proporciona **Apache Hive**.

Para realizar esta comparativa, se implementaron dos algoritmos clásicos de procesamiento de textos sobre conjuntos de datos no estructurados (libros y artículos de Wikipedia):

### A. WordCount (Conteo de Palabras)
Calcula la frecuencia de aparición de cada palabra en un gran corpus de texto.
*   **Enfoque Hadoop MapReduce:** Implementado con `mapper_wordcount.py` y `reducer_wordcount.py`. Se lanza a EMR mediante `lanzar_wordcount.py`.
*   **Enfoque Hive:** Resuelto mediante consultas HQL en `hive_wordcount.q` y orquestado con `lanzar_hive_wordcount.py`.

### B. Inverted Index (Índice Invertido)
Crea un diccionario que mapea cada palabra a los documentos y líneas donde aparece, fundamental para motores de búsqueda.
*   **Enfoque Hadoop MapReduce:** Implementado con `mapper_indice.py` y `reducer_indice.py`. Se ejecuta usando `lanzar_indice.py`.
*   **Enfoque Hive:** Resuelto con consultas HQL en `hive_indice.q` (`indice_invertido.q`) y lanzado mediante `lanzar_hive_indice.py`.


## 2. Análisis de Viajes en Taxi (NYC Taxi) y Benchmarking Avanzado

El segundo caso de uso es un escenario analítico más complejo y pesado, diseñado para procesar datos estructurados de gran volumen utilizando las capacidades avanzadas de Hive. Este apartado se centra en los registros de viajes de los Taxis de Nueva York.

Este bloque busca probar estrategias de optimización y recolección de métricas sobre conjuntos de datos masivos.

*   **Benchmarking de Particionamiento:** El objetivo principal es medir empíricamente la diferencia de rendimiento al realizar consultas analíticas complejas sobre una tabla "plana" (que requiere escaneos completos, *Full Table Scans*) frente a una **tabla con particionamiento dinámico multinivel** (por año, mes y día).
*   **Scripts HiveQL:** Toda la lógica reside en el directorio `taxi_jobs/` y archivos como `taxi_analisis.q`.
*   **Automatización:** Los scripts `taxi_preparar_datos.py` y `taxi_lanzar_analisis.py` se encargan de subir el dataset gigantesco, crear las bases de datos en Hive, particionar los datos y ejecutar las baterías de pruebas analíticas.
*   **Resultados:** Los hallazgos y tiempos comparativos de esta sección están documentados en detalle dentro de `benchmark_report.md`.

---

## Componentes

Para dar soporte a ambos casos de uso, el repositorio incluye herramientas desarrolladas en Python (utilizando `boto3`) que automatizan la interacción con la nube de AWS, evitando tener que usar la consola web:

*   **`levantar_emr.py`**: Automatiza la creación, configuración y arranque del clúster de AWS EMR definiendo el hardware, almacenamiento y las aplicaciones (Hadoop, Hive, Tez).
*   **`subir_todos_s3.py` / `subir_s3_emr.py` / `subir_wikipedia_s3.py`**: Diferentes scripts para subir eficientemente los datasets locales (novelas, wikipedia, csvs de taxis) al almacenamiento en Amazon S3, utilizando en algunos casos cargas multiparte asíncronas.
*   **`lanzar_job_hadoop.py` / `lanzar_job_hive.py` / `ejecutar_paso_hive.py`**: Utilidades para programáticamente enviar "Steps" (Trabajos) al clúster de EMR en ejecución y monitorear su estado.
*   **`ver_resultados.py` / `ver_metricas.py`**: Permiten descargar y visualizar fácilmente los resultados y los logs generados desde S3 a la consola local.

## Requisitos
- Python 3.x con las librerías `boto3` instaladas.

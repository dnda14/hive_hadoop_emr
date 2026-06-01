INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}/01_total_viajes/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 'Total Viajes', COUNT(*) FROM taxi_particion;

INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}/02_promedio_distancia/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 'Promedio Distancia (millas)', AVG(trip_distance) FROM taxi_particion;

INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}/03_horas_trafico/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT hour(from_unixtime(CAST(tpep_pickup_datetime / 1000000 AS BIGINT))) as hora_del_dia, COUNT(*) as cantidad_viajes 
FROM taxi_particion 
GROUP BY hour(from_unixtime(CAST(tpep_pickup_datetime / 1000000 AS BIGINT))) 
ORDER BY cantidad_viajes DESC 
LIMIT 5;

INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}/04_metodos_pago/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT payment_type, COUNT(*) as cantidad 
FROM taxi_particion 
GROUP BY payment_type 
ORDER BY cantidad DESC;

INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}/05_top_costosos/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT from_unixtime(CAST(tpep_pickup_datetime / 1000000 AS BIGINT)) as fecha_viaje, trip_distance, total_amount, payment_type 
FROM taxi_particion 
ORDER BY total_amount DESC 
LIMIT 10;

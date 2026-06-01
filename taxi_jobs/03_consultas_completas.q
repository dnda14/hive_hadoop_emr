-- Total viajes
INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}/total_viajes/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 'Total Viajes', 
COUNT(*) 
FROM taxi_particion;

-- Promedio distancia
INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}/promedio_distancia/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 'Promedio Distancia', 
AVG(trip_distance) 
FROM taxi_particion;

-- Horas de mas carreras
INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}/horas_trafico/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT hour(from_unixtime(CAST(tpep_pickup_datetime / 1000000 AS BIGINT))) as hora_del_dia, 
COUNT(*) as cantidad_viajes 
FROM taxi_particion 
GROUP BY hour(from_unixtime(CAST(tpep_pickup_datetime / 1000000 AS BIGINT))) 
ORDER BY cantidad_viajes DESC 
LIMIT 5;

-- Métodos de pago 
INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}/metodos_pago/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT payment_type, 
COUNT(*) as cantidad 
FROM taxi_particion 
GROUP BY payment_type 
ORDER BY cantidad DESC;

-- Top 10 viajes 
INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}/top_costosos/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT from_unixtime(CAST(tpep_pickup_datetime / 1000000 AS BIGINT)) as fecha_viaje, 
trip_distance, 
total_amount, 
payment_type 
FROM taxi_particion 
ORDER BY total_amount DESC 
LIMIT 10;

-- Consulta viajes en un dia
INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}/consulta_fecha/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 'Viajes el 2026-01-01', COUNT(*) 
FROM taxi_particion 
WHERE anio = '2026' and mes ='1' and ia= '1';

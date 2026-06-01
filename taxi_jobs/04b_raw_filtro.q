INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}_RAW/06_consulta_fecha/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 'Viajes ', COUNT(*) 
FROM taxi_trips_raw 
WHERE to_date(from_unixtime(CAST(tpep_pickup_datetime / 1000000 AS BIGINT))) = '2026-01-01';

INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}_RAW/07_recaudacion_fecha/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 'Recaudacion ', SUM(total_amount) 
FROM taxi_trips_raw 
WHERE to_date(from_unixtime(CAST(tpep_pickup_datetime / 1000000 AS BIGINT))) = '2026-01-15';

INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}_RAW/08_pasajeros_fin_mes/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 'Promedio Pasajeros ', AVG(passenger_count) 
FROM taxi_trips_raw 
WHERE to_date(from_unixtime(CAST(tpep_pickup_datetime / 1000000 AS BIGINT))) = '2026-01-31';

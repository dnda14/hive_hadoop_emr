INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}_RAW/09_recaudacion_mes/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 'Recaudacion enero 2025', SUM(total_amount) 
FROM taxi_trips_raw 
WHERE year(from_unixtime(CAST(tpep_pickup_datetime / 1000000 AS BIGINT))) = 2025 
  AND month(from_unixtime(CAST(tpep_pickup_datetime / 1000000 AS BIGINT))) = 1;

INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}_RAW/10_viajes_san_valentin/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 'Viajes en 14 feb', COUNT(*) 
FROM taxi_trips_raw 
WHERE year(from_unixtime(CAST(tpep_pickup_datetime / 1000000 AS BIGINT))) = 2026 
  AND month(from_unixtime(CAST(tpep_pickup_datetime / 1000000 AS BIGINT))) = 2 
  AND day(from_unixtime(CAST(tpep_pickup_datetime / 1000000 AS BIGINT))) = 14;

INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}_RAW/11_pasajeros_febrero/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 'Promedio pasajeros feb 2025', AVG(passenger_count) 
FROM taxi_trips_raw 
WHERE year(from_unixtime(CAST(tpep_pickup_datetime / 1000000 AS BIGINT))) = 2025 
  AND month(from_unixtime(CAST(tpep_pickup_datetime / 1000000 AS BIGINT))) = 2;

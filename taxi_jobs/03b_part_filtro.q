INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}/06_consulta_fecha/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 'Viajes ', COUNT(*) 
FROM taxi_particion 
WHERE pickup_date = '2026-01-01';

INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}/07_recaudacion_fecha/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 'Recaudacion', SUM(total_amount) 
FROM taxi_particion 
WHERE pickup_date = '2026-01-15';

INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}/08_pasajeros_fin_mes/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 'Promedio Pasajeros, AVG(passenger_count) 
FROM taxi_particion 
WHERE pickup_date = '2026-01-31';

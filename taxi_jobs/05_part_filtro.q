INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}/09_recaudacion_mes/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 'Recaudacion enero 2025', SUM(total_amount) 
FROM taxi_particion 
WHERE anio = '2025' AND mes = '1';

INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}/10_viajes_san_valentin/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 'Viajes el 14', COUNT(*) 
FROM taxi_particion 
WHERE anio = '2026' AND mes = '2' AND dia = '14';

INSERT OVERWRITE DIRECTORY '${OUTPUT}/reporte_${FECHA}/11_pasajeros_febrero/'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 'Promedio Pasajeros feb 2025', AVG(passenger_count) 
FROM taxi_particion 
WHERE anio = '2025' AND mes = '2';

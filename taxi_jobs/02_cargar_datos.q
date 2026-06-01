SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

INSERT OVERWRITE TABLE taxi_particion PARTITION (anio, mes, dia)
SELECT 
    *,
    year(from_unixtime(CAST(tpep_pickup_datetime / 1000000 AS BIGINT))) as anio,
    month(from_unixtime(CAST(tpep_pickup_datetime / 1000000 AS BIGINT))) as mes,
    day(from_unixtime(CAST(tpep_pickup_datetime / 1000000 AS BIGINT))) as dia
FROM taxi_raw
WHERE tpep_pickup_datetime IS NOT NULL;

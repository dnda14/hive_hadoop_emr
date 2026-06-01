DROP TABLE IF EXISTS taxi_raw;
CREATE EXTERNAL TABLE taxi_raw (
    VendorID INT, 
    tpep_pickup_datetime BIGINT, 
    tpep_dropoff_datetime BIGINT,
    passenger_count INT, 
    trip_distance DOUBLE, 
    RatecodeID INT, 
    store_and_fwd_flag STRING,
    PULocationID INT, 
    DOLocationID INT, 
    payment_type INT, 
    fare_amount DOUBLE,
    extra DOUBLE, 
    mta_tax DOUBLE, 
    tip_amount DOUBLE, 
    tolls_amount DOUBLE,
    improvement_surcharge DOUBLE, 
    total_amount DOUBLE, 
    congestion_surcharge DOUBLE,
    Airport_fee DOUBLE
)
STORED AS PARQUET
LOCATION '${INPUT}';

DROP TABLE IF EXISTS taxi_particion;
CREATE EXTERNAL TABLE taxi_particion (
    VendorID INT, 
    tpep_pickup_datetime BIGINT, 
    tpep_dropoff_datetime BIGINT,
    passenger_count INT, 
    trip_distance DOUBLE, 
    RatecodeID INT, 
    store_and_fwd_flag STRING,
    PULocationID INT, 
    DOLocationID INT, 
    payment_type INT, 
    fare_amount DOUBLE,
    extra DOUBLE, 
    mta_tax DOUBLE, 
    tip_amount DOUBLE, 
    tolls_amount DOUBLE,
    improvement_surcharge DOUBLE, 
    total_amount DOUBLE, 
    congestion_surcharge DOUBLE,
    Airport_fee DOUBLE
)
PARTITIONED BY (anio STRING, mes STRING, dia STRING)
STORED AS PARQUET
LOCATION '${OUTPUT}';

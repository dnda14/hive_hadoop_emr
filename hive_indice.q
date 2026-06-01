set hive.tez.container.size=4096;
set hive.tez.java.opts=-Xmx3200m;

set hive.groupby.skewindata=true;

DROP TABLE IF EXISTS docs;
CREATE EXTERNAL TABLE docs (
    block_id STRING,
    text_block STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
   "separatorChar" = ",",
   "quoteChar"     = "\""
)
STORED AS TEXTFILE
LOCATION '${INPUT}';

CREATE TABLE par_p_b AS
SELECT DISTINCT
    block_id,
    lower(pal) as pal
FROM docs
LATERAL VIEW explode(split(text_block, ' ')) w AS pal;


DROP TABLE IF EXISTS indice_in;
CREATE EXTERNAL TABLE indice_in (
    pal STRING,
    block_ids STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
LOCATION '${OUTPUT}';

INSERT OVERWRITE TABLE indice_in
SELECT 
    pal, 
    concat_ws(',', collect_set(block_id)) as block_ids
FROM par_p_b
GROUP BY pal;

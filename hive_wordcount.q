set hive.tez.container.size=4096;
set hive.tez.java.opts=-Xmx3200m;

DROP TABLE IF EXISTS docs;
CREATE EXTERNAL TABLE docs (
    line STRING
)
STORED AS TEXTFILE
LOCATION '${INPUT}';

DROP TABLE IF EXISTS cont_pal;

CREATE EXTERNAL TABLE cont_pal (
    word STRING,
    count BIGINT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
LOCATION '${OUTPUT}';

INSERT OVERWRITE TABLE cont_pal
SELECT 
    pal, 
    COUNT(1) as count
FROM (
    SELECT explode(split(lower(regexp_replace(line, '[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ0-9 ]', ' ')), ' ')) as pal
    FROM docs
) w
WHERE pal != ''
GROUP BY pal;

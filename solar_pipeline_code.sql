CREATE OR REPLACE TABLE raw_nasa_data.solar_analysis_final AS 

SELECT 
  -- Creates a Clean Category for charts (turns X8.7 class storm into just "X")
  LEFT (flares.class_type, 1) AS flare_category,

  flares.class_type AS flare_specific_class,
  flares.begin_time AS flare_time,
  storms.storm_start_time AS storm_time,
  storms.storm_severity, 

  -- Golden Metric
  TIMESTAMP_DIFF(storms.storm_start_time, flares.begin_time, HOUR) AS hours_to_arrive
FROM raw_nasa_data.solar_flares AS flares
INNER JOIN raw_nasa_data.clean_storms AS storms
ON
  storms.storm_start_time > flares.begin_time
  AND
  storms.storm_start_time <= TIMESTAMP_ADD(flares.begin_time, INTERVAL 5 DAY);
 

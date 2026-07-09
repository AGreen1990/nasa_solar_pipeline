-----------------------
--Starting SILVER LAYER
-----------------------


SELECT 
  JSON_VALUE(raw_payload.activityID) as cme_id,
  JSON_VALUE(raw_payload.startTime) as start_time,
  -- pulls not from specifc scientific model-note root event aka raw_payload
  JSON_VALUE(analysis.note) as event_note,

-- Visual model data
  JSON_VALUE(analysis.speed) AS model_speed,
  JSON_VALUE(analysis.type) AS model_type,

-- Impact data (will NULL if not simulation was run)
  JSON_VALUE(impact.location) AS impact_location,
  JSON_VALUE(impact.arrivalTime) AS arrival_time
FROM
  `space-weather-monitor-501822.nasa_bronze.raw_cme`
-- Extract the array from JSON, then flatten into rows
LEFT JOIN
--Flattens Array 1(The Analyses)
  UNNEST(JSON_QUERY_ARRAY(raw_payload.cmeAnalyses)) as analysis

-- Flattens Array 2 (The simiulations hiding inside the Analyses)
LEFT JOIN
  UNNEST(JSON_QUERY_ARRAY(analysis.enlilList)) AS enlil_model

-- Flattens Array 3- Hit Impact List
LEFT JOIN
  UNNEST(JSON_QUERY_ARRAY(enlil_model.impactList)) AS impact;
 

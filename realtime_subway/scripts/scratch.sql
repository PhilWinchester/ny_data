-- Get all stations along the 1 line
SELECT * FROM realtime_subway_stations WHERE station_lines LIKE '%1%';
SELECT station_id, station_parent_id, northbound_desc, southbound_desc FROM realtime_subway_stations WHERE station_lines LIKE '%1%';

-- Get all end of line stops. Data quality is still messy from import scripts
SELECT 
    * 
FROM realtime_subway_stations 
WHERE station_parent_id IS NOT NULL
    AND northbound_desc = '' 
    AND southbound_desc = '';

-- Hacky way to determine number of times import script has been run
SELECT COUNT(DISTINCT DATE_TRUNC('minute', datetime_created)) AS "script runs" FROM realtime_subway_trains;

-- Get trains on a specific route
SELECT train_id, import_id FROM realtime_subway_trains WHERE train_route = 'C';

-- Get trains with the most "data" on them (ie buggy imports)
SELECT train_id, COUNT(*) FROM realtime_subway_trains GROUP BY 1 ORDER BY 2 DESC;

-- Inspect all data on a train
SELECT 
    train_id
    , train_route
    , route_start
    , trains.datetime_created AS import_date
    , train_direction
    , import_id
    , station_name
FROM realtime_subway_trains AS trains
    JOIN realtime_subway_stations AS stations ON trains.current_stop_id = stations.station_id
WHERE train_id = '090400'
ORDER BY import_date DESC;

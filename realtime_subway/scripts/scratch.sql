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
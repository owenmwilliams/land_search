SELECT * 
INTO TABLE countyLandvalue
FROM county_landdata_csv clc 
WHERE clc.yr::int = 2018;

SELECT *
INTO TABLE countyDataset
FROM county_population_csv cpc 
WHERE CAST(date_part('year', cpc.date_code) AS varchar) = '2018';

SELECT * 
INTO TABLE countyLatlong
FROM county_latlong_csv clc;

SELECT *
INTO TABLE placeAirports
FROM major_airports_csv mac;

SELECT * 
INTO TABLE placeRecreation
FROM national_recreation_csv nrc 
WHERE nrc.unit_type::varchar <> 'National Parkway'
AND nrc.unit_type::varchar <> 'Parkway';
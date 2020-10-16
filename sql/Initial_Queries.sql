 -- Select on a join population and land value
SELECT clc.yr, clc.county, clc.state, clc.land_value_asis_all, clc.land_share_all, cpc.population FROM county_landdata_csv clc 
JOIN county_population_csv cpc 
	ON clc.county = cpc.county 
	AND clc.yr = CAST(date_part('year', cpc.date_code) AS varchar)
	AND clc.state = trim(cpc.state)
	WHERE clc.yr = '2018'
	AND cpc.population < 50000
	AND clc.land_value_asis_all < 40000
	AND clc.land_share_all < '0.15'
	ORDER BY population ;

 -- Clean up landdata data types *** WORK IN PROGRESS ***

ALTER TABLE county_landdata_csv ADD COLUMN ID serial PRIMARY KEY;

ALTER TABLE county_landdata_csv 
ALTER COLUMN land_value_std_all TYPE int
USING land_value_std_all::integer,
ALTER COLUMN land_value_asis_all TYPE int
USING land_value_asis_all::integer,
ALTER COLUMN prop_value_std_all TYPE int
USING prop_value_std_all::integer,
ALTER COLUMN prop_value_asis_all TYPE int
USING prop_value_asis_all::integer;

 -- Clean up county population: Dropping duplicate data & updating data types *** WORK IN PROGRESS ***

SELECT * FROM county_population_csv cpc 
WHERE base_remove IS NOT NULL;

DELETE FROM county_population_csv 
WHERE base_remove IS NOT NULL;

ALTER TABLE county_population_csv DROP COLUMN base_remove;

ALTER TABLE county_population_csv ADD COLUMN ID serial PRIMARY KEY;

ALTER TABLE county_population_csv 
	ALTER COLUMN date_code TYPE date
	USING date_code::date;

ALTER TABLE county_population_csv 
	ALTER COLUMN population TYPE int
	USING population::integer;
	
ALTER TABLE county_population_csv 
	ALTER COLUMN state TYPE varchar(40);
	
 -- Cull airports list and add geometry column

CREATE EXTENSION postgis;

CREATE TABLE major_airports AS 
	SELECT x, y, loc_id, objectid, state_name, county, city, commercial_ops
	FROM airports_csv
	WHERE commercial_ops > 7000;

ALTER TABLE major_airports 
	ADD COLUMN geom geometry(Geometry,4326);

ALTER TABLE major_airports 
	RENAME COLUMN x TO long;
ALTER TABLE major_airports 
	RENAME COLUMN y TO lat;

UPDATE major_airports 
	SET geom=ST_SetSRID(ST_Point(major_airports.lat::double precision, major_airports.long::double precision),4326)::geometry;

SELECT * FROM major_airports ;

 -- Add geometry column to county lat long
 
SELECT * FROM county_latlong_csv clc ;
SELECT COLUMN_NAME FROM information_schema.COLUMNS
	WHERE table_name = 'county_latlong_csv';

UPDATE county_latlong_csv 
	SET geom=ST_SetSRID(ST_Point(county_latlong_csv.intptlat::double precision, county_latlong_csv.intptlong::double PRECISION),4326)::geometry;

SELECT * FROM county_latlong_csv clc ;

 -- Cleanup airports column names

SELECT column_name FROM information_schema.COLUMNS
	WHERE table_name = 'airports_csv';

SELECT "﻿X" FROM airports_csv ac ;
ALTER TABLE airports_csv RENAME COLUMN "﻿X" TO "x";


ALTER TABLE county_latlong_csv 
  ADD COLUMN geom 
 geometry(Geometry,4326);

 -- Find nearest neighbor airport

with cte as (
      SELECT A.geom, B.geom, A."NAME", A.state, B.loc_id, B.commercial_ops,
             ST_Distance(A.geom, B.geom) as dist -- check this value first
      FROM county_latlong_csv as A
      CROSS JOIN major_airports as B
      WHERE ST_Distance(A.geom, B.geom) < 1.5 -- 10 miles
      AND A.state = 'New Mexico'
)
SELECT *
FROM  cte;

 -- Cleanup county lat long column names

SELECT intptlat, "INTPTLONG                                                      " FROM county_latlong_csv clc ;

ALTER TABLE airports_csv 
	ALTER COLUMN commercial_ops TYPE int
	USING commercial_ops::integer;
	
 -- Getting counties lat long

SELECT l.usps, lu.Description FROM county_latlong_csv l
	JOIN state_abb_csv lu
	ON l.usps = lu.code;

ALTER TABLE county_latlong_csv ADD COLUMN state varchar(40);

UPDATE county_latlong_csv l
	SET state = lu.Description
	FROM state_abb_csv lu
	WHERE l.usps = lu.code;


SELECT COLUMN_NAME FROM information_schema.COLUMNS
WHERE table_name = 'county_latlong_csv';
SELECT * FROM county_latlong_csv clc ;
SELECT "INTPTLONG                                                      " FROM county_latlong_csv clc ;
ALTER TABLE county_latlong_csv RENAME COLUMN "INTPTLONG                                                      " TO "intptlong";

 -- Import and clean national parks data
 
SELECT * FROM national_recreation_csv nrc ;
SELECT * FROM "GNIS_ID_loc" gil WHERE "﻿FEATURE_ID" = '2877';

SELECT "﻿X" FROM national_recreation_csv nrc ;
ALTER TABLE national_recreation_csv RENAME COLUMN "﻿X" TO "x";

SELECT gil."﻿FEATURE_ID", gil.feature_name, nrc.unit_name, nrc.gnis_id, gil.prim_lat_dec, gil.prim_long_dec
	FROM "GNIS_ID_loc" gil 
	JOIN national_recreation_csv nrc 
	ON gil."﻿FEATURE_ID" = nrc.gnis_id ;

SELECT table_name, COLUMN_NAME, data_type FROM information_schema.COLUMNS 
WHERE table_name = 'county_latlong_csv'; 

ALTER TABLE national_recreation_csv ADD COLUMN lat varchar(100);
ALTER TABLE national_recreation_csv ADD COLUMN long varchar(100);
UPDATE national_recreation_csv l
	SET lat = lu.prim_lat_dec
	FROM "GNIS_ID_loc" lu
	WHERE l.gnis_id = lu."﻿FEATURE_ID" ;
UPDATE national_recreation_csv l
	SET long = lu.prim_long_dec
	FROM "GNIS_ID_loc" lu
	WHERE l.gnis_id = lu."﻿FEATURE_ID" ;

SELECT count(gnis_id) FROM national_recreation_csv nrc 
WHERE nrc.long IS NOT NULL;

 -- Add geo columns to national recreation
 
ALTER TABLE national_recreation_csv 
  ADD COLUMN geom 
 geometry(Geometry,4326);

UPDATE national_recreation_csv 
	SET geom=ST_SetSRID(ST_Point(national_recreation_csv.lat::double precision, national_recreation_csv.long::double PRECISION),4326)::geometry;

SELECT * FROM national_recreation_csv nrc ;

 -- Query on land cost, population, and land share

SELECT clc.yr, clc.county, clc.state, clc2.intptlat, clc2.intptlong, clc.land_value_asis_all, clc.land_share_all, cpc.population FROM county_landdata_csv clc 
	JOIN county_population_csv cpc 
		ON clc.county = cpc.county 
		AND clc.yr = CAST(date_part('year', cpc.date_code) AS varchar)
		AND clc.state = trim(cpc.state)
	JOIN county_latlong_csv clc2 
		ON clc.county = clc2."NAME"
		AND clc.state = clc2.state
	WHERE clc.yr = '2018'
		AND cpc.population < 50000
		AND clc.land_value_asis_all < 100000
		AND clc.land_share_all < '0.15'
	ORDER BY land_value_asis_all ;
	
 -- Query ON above + nearby airports

WITH 	cte AS (
			SELECT A.county, A.state, B.loc_id, B.commercial_ops,
             	ST_Distance(A.geom, B.geom) as dist -- check this value first
			FROM county_latlong_csv as A
			CROSS JOIN major_airports_csv as B
			WHERE ST_Distance(A.geom, B.geom) < 1.0 -- 100 miles
			), sort AS (
			SELECT *, row_number() OVER (PARTITION BY state, county ORDER BY dist) as rn
			FROM cte
			)	
SELECT clc.county, clc.state, sort.loc_id, sort.dist, sort.commercial_ops, clc.land_value_asis_all, clc.land_share_all, cpc.population
	FROM county_landdata_csv clc
	JOIN sort
		ON sort.county = clc.county 
		AND sort.state = clc.state
	JOIN county_population_csv cpc
		ON clc.county = cpc.county 
		AND clc.yr = CAST(date_part('year', cpc.date_code) AS varchar)
		AND clc.state = trim(cpc.state)
	WHERE clc.yr = '2018'
		AND cpc.population < 200000
		AND clc.land_value_asis_all < 200000
		AND clc.land_share_all < '0.25'
		AND clc.state = 'New Mexico'
		AND sort.rn = 1
	ORDER BY county, state;

SELECT * FROM county_landdata_csv clc 
	WHERE clc.state = 'New Mexico'
	AND clc.yr = '2018';

 -- Query ON above + nearby recreation

SELECT * FROM national_recreation_csv nrc ;

WITH 	cte AS (
			SELECT A.county, A.state, B.loc_id, B.commercial_ops,
             	ST_Distance(A.geom, B.geom) as dist -- check this value first
			FROM county_latlong_csv AS A
			CROSS JOIN major_airports_csv AS B
			WHERE ST_Distance(A.geom, B.geom) < 1.0 -- 100 miles
			), sort AS (
			SELECT *, row_number() OVER (PARTITION BY state, county ORDER BY dist) as rn
			FROM cte
			), clp AS (
			SELECT A.county, A.state, B.gnis_id, B.unit_name, B.lat, B.long,
				ST_Distance(A.geom, B.geom) AS dist 
			FROM county_latlong_csv AS A
			CROSS JOIN national_recreation_csv AS B
			WHERE ST_Distance(A.geom, B.geom) < 1.5
			), sortp AS (
			SELECT *, row_number() OVER (PARTITION BY state, county ORDER BY dist) AS rn 
			FROM clp
			)
SELECT clc.county, clc.state, sort.loc_id, sort.dist, sort.commercial_ops, sortp.unit_name, sortp.dist, clc.land_value_asis_all, clc.land_share_all, cpc.population
	FROM county_landdata_csv clc
	JOIN sort
		ON sort.county = clc.county 
		AND sort.state = clc.state
	JOIN sortp
		ON sortp.county = clc.county 
		AND sortp.state = clc.state 
	JOIN county_population_csv cpc
		ON clc.county = cpc.county 
		AND clc.yr = CAST(date_part('year', cpc.date_code) AS varchar)
		AND clc.state = trim(cpc.state)
	WHERE clc.yr = '2018'
		AND cpc.population < 200000
		AND clc.land_value_asis_all < 50000
		AND clc.land_share_all < '0.25'
		AND clc.state = 'Texas'
		AND sort.rn = 1
		AND sortp.rn < 3
	ORDER BY county, state;

SELECT * FROM county_landdata_csv clc 
	WHERE clc.state = 'New Mexico'
	AND clc.yr = '2018';


 -- Playground

SELECT table_name, COLUMN_NAME FROM information_schema.COLUMNS
	WHERE table_name LIKE '%_csv';

SELECT * FROM national_recreation_csv nrc ;

ALTER TABLE national_recreation_csv RENAME COLUMN "X" TO ;

DROP TABLE "GNIS_ID_loc" ;
			
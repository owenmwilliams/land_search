-- Clean up airports_bulk

SELECT * FROM airports_bulk ab ;

ALTER TABLE airports_bulk 
	DROP COLUMN rec_type, 
	DROP COLUMN site_num, 
	DROP COLUMN eff_date, 
	DROP COLUMN field_office_code, 
	DROP COLUMN state_post_office_code, 
	DROP COLUMN county_post_office_code, 
	DROP COLUMN owner_type, 
	DROP COLUMN fac_use, 
	DROP COLUMN owner_name, 
	DROP COLUMN owner_address, 
	DROP COLUMN owner_city_state_zip, 
	DROP COLUMN owner_phone, 
	DROP COLUMN manager_name, 
	DROP COLUMN manager_address, 
	DROP COLUMN manager_city_state_zip,
	DROP COLUMN manager_phone, 
	DROP COLUMN ref_point_lat, 
	DROP COLUMN ref_point_lat_secs, 
	DROP COLUMN ref_point_lon, 
	DROP COLUMN ref_point_lon_secs, 
	DROP COLUMN ref_point_method, 
	DROP COLUMN elevation_method, 
	DROP COLUMN mag_var, 
	DROP COLUMN mag_var_year, 
	DROP COLUMN pattern_altitude, 
	DROP COLUMN sectional_chart, 
	DROP COLUMN dist_city_to_airport, 
	DROP COLUMN dir_city_to_airport, 
	DROP COLUMN land_area_covered, 
	DROP COLUMN boundary_artcc_id,
	DROP COLUMN boundary_artcc_comp_id, 
	DROP COLUMN boundary_artcc_name, 
	DROP COLUMN responsible_artcc_id, 
	DROP COLUMN responsible_artcc_comp_id, 
	DROP COLUMN responsible_artcc_name, 
	DROP COLUMN fss_on_fac,
	DROP COLUMN fss_id, 
	DROP COLUMN fss_name, 
	DROP COLUMN local_phone_airport_to_fss, 
	DROP COLUMN toll_free_phone_airport_to_fss, 
	DROP COLUMN alt_fss_id, 
	DROP COLUMN alt_fss_name, 
	DROP COLUMN toll_free_phone_airport_to_alt_, 
	DROP COLUMN notam_wx_fac_id, 
	DROP COLUMN notam_dservice, 
	DROP COLUMN status_code, 
	DROP COLUMN arff_cert_type_date, 
	DROP COLUMN npias_fed_cod, 
	DROP COLUMN airspace_analysis, 
	DROP COLUMN intl_customs_entry, 
	DROP COLUMN intl_customs_landing, 
	DROP COLUMN mil_joint_use_civ, 
	DROP COLUMN mil_landing_rights, 
	DROP COLUMN inspection_method, 
	DROP COLUMN agency_inspection, 
	DROP COLUMN last_inspection, 
	DROP COLUMN last_info_request,
	DROP COLUMN fuel_types, 
	DROP COLUMN repair_service, 
	DROP COLUMN power_plant_repair, 
	DROP COLUMN bottled_oxygen, 
	DROP COLUMN bulk_oxygen, 
	DROP COLUMN lighting_sched, 
	DROP COLUMN beacon_light_schedule, 
	DROP COLUMN atc_tower,
	DROP COLUMN unicom, 
	DROP COLUMN ctaf, 
	DROP COLUMN seg_circle_marker, 
	DROP COLUMN beacon_color, 
	DROP COLUMN landing_fee, 
	DROP COLUMN medical_fac, 
	DROP COLUMN based_single_eng, 
	DROP COLUMN based_multi_eng, 
	DROP COLUMN based_jet_eng, 
	DROP COLUMN based_helicopter,
	DROP COLUMN based_gliders, 
	DROP COLUMN based_military, 
	DROP COLUMN based_ultralight, 
	DROP COLUMN annual_ops_date, 
	DROP COLUMN position_src, 
	DROP COLUMN position_src_date, 
	DROP COLUMN elevation_src, 
	DROP COLUMN elevation_src_date, 
	DROP COLUMN contract_fuel, 
	DROP COLUMN transient_storage, 
	DROP COLUMN other_services, 
	DROP COLUMN wind_indicator, 
	DROP COLUMN icao_identifier, 
	DROP COLUMN min_op_net, 
	DROP COLUMN filler, 
	DROP COLUMN geom;

SELECT table_name, COLUMN_NAME, data_type FROM information_schema.COLUMNS
	WHERE table_name = 'airports_bulk';

ALTER TABLE airports_bulk 
	ALTER COLUMN commuter_ops TYPE int
		USING commuter_ops::integer,
	ALTER COLUMN air_taxi_ops TYPE int
		USING air_taxi_ops::integer,
	ALTER COLUMN ga_local_ops TYPE int
		USING ga_local_ops::integer,		
	ALTER COLUMN ga_itinerant_ops TYPE int
		USING ga_itinerant_ops::integer,
	ALTER COLUMN commercial_ops TYPE int
		USING commercial_ops::integer;
	
ALTER TABLE airports_bulk 
	ADD PRIMARY KEY (objectid);

ALTER TABLE airports_bulk 
	RENAME COLUMN "x" TO "long";
ALTER TABLE airports_bulk 
	RENAME COLUMN "y" TO "lat";

SELECT * FROM airports_bulk ab ;
	

-- Clean up county_landdata_csv

SELECT * FROM county_landdata_csv clc ;

ALTER TABLE county_landdata_csv ADD COLUMN ID serial PRIMARY KEY;

SELECT COLUMN_NAME, data_type FROM information_schema.COLUMNS
	WHERE table_name = 'county_landdata_csv';

ALTER TABLE county_landdata_csv 
	ALTER COLUMN land_value_std_all TYPE int
		USING land_value_std_all::integer,
	ALTER COLUMN land_value_asis_all TYPE int
		USING land_value_asis_all::integer,
	ALTER COLUMN prop_value_std_all TYPE int
		USING prop_value_std_all::integer,
	ALTER COLUMN prop_value_asis_all TYPE int
		USING prop_value_asis_all::integer;
	
ALTER TABLE county_landdata_csv 
	ALTER COLUMN land_value_std_ws TYPE int
		USING land_value_std_ws::integer,
	ALTER COLUMN land_value_asis_ws TYPE int
		USING land_value_asis_ws::integer,
	ALTER COLUMN prop_value_std_ws TYPE int
		USING prop_value_std_ws::integer,
	ALTER COLUMN prop_value_asis_ws TYPE int
		USING prop_value_asis_ws::integer;
	
ALTER TABLE county_landdata_csv 
	ALTER COLUMN land_share_all TYPE decimal
		USING land_share_all::double PRECISION,
	ALTER COLUMN land_share_ws TYPE decimal
		USING land_share_ws::double PRECISION,
	ALTER COLUMN lot_size_ws TYPE int
		USING lot_size_ws::integer,
	ALTER COLUMN sqft_ws TYPE int
		USING sqft_ws::integer;
	
SELECT * FROM county_landdata_csv clc ;


 -- Clean up county_latlong_csv
 
SELECT * FROM county_latlong_csv clc ;

ALTER TABLE county_latlong_csv 
	DROP COLUMN aland,
	DROP COLUMN awater;

ALTER TABLE county_latlong_csv 
	ADD COLUMN geom geometry(Geometry,4326);

UPDATE county_latlong_csv 
	SET geom=ST_SetSRID(ST_Point(county_latlong_csv.intptlat::double precision, county_latlong_csv.intptlong::double PRECISION),4326)::geometry;

SELECT COLUMN_NAME, data_type FROM information_schema.COLUMNS
	WHERE table_name = 'county_latlong_csv';

ALTER TABLE county_latlong_csv 
	ALTER COLUMN aland_sqmi TYPE REAL
		USING aland_sqmi::REAL;
	
ALTER TABLE county_latlong_csv 
	ALTER COLUMN awater_sqmi TYPE REAL
		USING awater_sqmi::REAL;
	
ALTER TABLE county_latlong_csv 
	RENAME COLUMN intptlat TO lat;

ALTER TABLE county_latlong_csv 
	RENAME COLUMN intptlong TO long;

ALTER TABLE county_latlong_csv 
	ALTER COLUMN lat TYPE decimal
		USING lat::double PRECISION;
	
ALTER TABLE county_latlong_csv 
	ALTER COLUMN long TYPE decimal
		USING long::double PRECISION;
	
ALTER TABLE county_latlong_csv 
	ADD PRIMARY KEY (geoid);

SELECT * FROM county_latlong_csv clc ;
 

 -- Clean up county_population_csv

SELECT * FROM county_population_csv cpc ;

SELECT * FROM county_population_csv cpc 
	WHERE base_remove IS NOT NULL;

DELETE FROM county_population_csv 
	WHERE base_remove IS NOT NULL;

ALTER TABLE county_population_csv 
	DROP COLUMN base_remove;

ALTER TABLE county_population_csv 
	ADD COLUMN ID serial PRIMARY KEY;

SELECT COLUMN_NAME, data_type FROM information_schema.COLUMNS
	WHERE table_name = 'county_population_csv';

ALTER TABLE county_population_csv 
	ALTER COLUMN date_code TYPE date
	USING date_code::date;

ALTER TABLE county_population_csv 
	ALTER COLUMN population TYPE int
	USING population::integer;
	
ALTER TABLE county_population_csv 
	ALTER COLUMN state TYPE varchar(40);

SELECT * FROM county_population_csv cpc ;
	

 -- Create major_airports_csv from airports_bulk

CREATE EXTENSION postgis;

CREATE TABLE major_airports AS 
	SELECT x, y, loc_id, objectid, state_name, county, city, commercial_ops
	FROM airports_csv
	WHERE commercial_ops > 7000;

ALTER TABLE major_airports 
	ADD COLUMN geom geometry(Geometry,4326);

UPDATE major_airports 
	SET geom=ST_SetSRID(ST_Point(major_airports.lat::double precision, major_airports.long::double precision),4326)::geometry;

ALTER TABLE major_airports 
	RENAME COLUMN x TO long;

ALTER TABLE major_airports 
	RENAME COLUMN y TO lat;

ALTER TABLE major_airports_csv 
	ALTER COLUMN lat TYPE decimal
		USING lat::double PRECISION;
	
ALTER TABLE major_airports_csv 
	ALTER COLUMN long TYPE decimal
		USING long::double PRECISION;
	
ALTER TABLE major_airports_csv 
	ADD PRIMARY KEY (objectid);

SELECT * FROM major_airports_csv;


 -- Clean up national_recreation_csv
 
SELECT * FROM national_recreation_csv nrc ;

SELECT "﻿X" FROM national_recreation_csv nrc ;
ALTER TABLE national_recreation_csv RENAME COLUMN "﻿X" TO "x";

SELECT table_name, COLUMN_NAME, data_type FROM information_schema.COLUMNS 
WHERE table_name = 'national_recreation_csv'; 

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

ALTER TABLE national_recreation_csv 
	DROP COLUMN x,
	DROP COLUMN y;

ALTER TABLE national_recreation_csv 
	ALTER COLUMN lat TYPE decimal
		USING lat::double PRECISION;
	
ALTER TABLE national_recreation_csv
	ALTER COLUMN long TYPE decimal
		USING long::double PRECISION;
	
ALTER TABLE national_recreation_csv 
	ADD PRIMARY KEY (objectid);
 
ALTER TABLE national_recreation_csv 
  ADD COLUMN geom 
 geometry(Geometry,4326);

UPDATE national_recreation_csv 
	SET geom=ST_SetSRID(ST_Point(national_recreation_csv.lat::double precision, national_recreation_csv.long::double PRECISION),4326)::geometry;

SELECT * FROM national_recreation_csv nrc ;


 -- Double check data types & pkey

SELECT table_name, COLUMN_NAME, constraint_name FROM information_schema.key_column_usage kcu 
	WHERE table_name LIKE '%_csv';

SELECT table_name, COLUMN_NAME, data_type FROM information_schema.COLUMNS
	WHERE table_name LIKE '%_csv';
	
SELECT * FROM "GNIS_ID_lu" gil LIMIT 1000;

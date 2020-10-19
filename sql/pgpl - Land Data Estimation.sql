 -- Find number OF DISTINCT VALUES IN county TABLES
 
SELECT count(*) FROM 
 	(SELECT DISTINCT state, county FROM county_landdata_csv clc)
 	AS disticount;
 	
SELECT count(*) FROM 
 	(SELECT DISTINCT state, county FROM county_latlong_csv clc)
 	AS disticount;
 	
SELECT count(*) FROM 
 	(SELECT DISTINCT state, county FROM county_population_csv cpc)
 	AS disticount;
 	

 -- Find missing values in population and location
 
SELECT DISTINCT cpc.state, cpc.county FROM county_population_csv cpc
	LEFT JOIN county_latlong_csv clc 
		ON trim(cpc.state) = clc.state
		AND cpc.county = clc.county
	WHERE clc.lat IS NULL 
	ORDER BY state ASC;


 -- Find missing values in land data from population
 
SELECT DISTINCT cpc.state, cpc.county FROM county_population_csv cpc
	LEFT JOIN county_landdata_csv clc 
		ON trim(cpc.state) = clc.state
		AND cpc.county = clc.county
	WHERE clc.land_share_all IS NULL 
	ORDER BY state ASC;
	

 -- Query location, population, and existing land_value from core data set

SELECT clc.state, clc.county, clc.geom, cld.land_value_asis_all, cpc.population FROM county_population_csv cpc
	FULL OUTER JOIN county_latlong_csv clc
		ON trim(cpc.state) = clc.state 
		AND cpc.county = clc.county
		AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018'
	FULL OUTER JOIN county_landdata_csv cld
		ON trim(cpc.state) = cld.state 
		AND cpc.county =  cld.county 
		AND cld.yr = CAST(date_part('year', cpc.date_code) AS varchar)
	WHERE clc.state = 'Alabama'
	ORDER BY clc.state;
	

 -- ADD a COLUMN TO count_landdata_csv AND populate WITH either base OR str(estimate) [including tag column]

ALTER TABLE county_population_csv 
	DROP COLUMN land_value_estimate;

ALTER TABLE county_population_csv 
	ADD COLUMN land_value_estimate varchar(30);

ALTER TABLE county_population_csv 
	ADD COLUMN est_base varchar(10);

ALTER TABLE county_population_csv 
	ADD COLUMN comps varchar(500);

UPDATE county_population_csv cpc
	SET land_value_estimate = land_value_asis_all::varchar
	FROM county_landdata_csv clc
	WHERE trim(cpc.state) = clc.state 
	AND cpc.county = clc.county 
	AND clc.yr = CAST(date_part('year', cpc.date_code) AS varchar)
	AND clc.yr = '2018'
	AND clc.land_value_asis_all IS NOT NULL;

UPDATE county_population_csv 
	SET est_base = 'base'
	WHERE land_value_estimate IS NOT NULL;

UPDATE county_population_csv 
	SET est_base = 'est'
	WHERE land_value_estimate IS NULL;

UPDATE county_population_csv cpc
	SET land_value_estimate = 'estimate'
	WHERE land_value_estimate IS NULL;

UPDATE county_population_csv 
	SET comps = 'no comp'
	WHERE est_base = 'base';

SELECT * FROM county_population_csv cpc WHERE CAST(date_part('year', cpc.date_code) AS varchar) = '2018' ORDER BY state, county;

 -- Define calculation function for land value estimate based on nearest neighbor and pop comps

WITH comp_select AS (			
	SELECT A.state AS est_st, A.county AS est_cty, C.land_value_asis_all AS est_lv, E.population AS est_pop, 
			B.state AS comp_st, B.county AS comp_cty, D.land_value_asis_all AS comp_lv, f.population AS comp_pop,
			ST_Distance(A.geom, B.geom) AS dist
		FROM county_latlong_csv AS A	
		INNER JOIN county_latlong_csv AS B
			ON ST_Distance(A.geom, B.geom) < 3
			OR A.state = B.state 
		INNER JOIN county_landdata_csv AS D
			ON B.state = D.state 
			AND B.county = D.county
			AND D.yr = '2018'
		INNER JOIN county_population_csv AS E
			ON A.state = trim(E.state)
			AND A.county = E.county
			AND CAST(date_part('year', E.date_code) AS varchar) = '2018'
		INNER JOIN county_population_csv AS F
			ON B.state = trim(F.state)
			AND B.county = F.county
			AND CAST(date_part('year', F.date_code) AS varchar) = '2018'
			AND abs(E.population - F. population) < E.population*0.2
		FULL OUTER JOIN county_landdata_csv AS C
			ON A.state = C.state 
			AND A.county = C.county 
			AND C.yr = '2018'
			WHERE C.land_value_asis_all IS NULL
	),
interim_table AS (
	SELECT est_st, est_cty, avg(dist), count(comp_cty) AS comp_count, avg(comp_lv) 
		FROM comp_select
			GROUP BY est_st, est_cty
	)
SELECT * FROM interim_table WHERE comp_count > 5
	;


 -- Count est vs. base in pop

SELECT count(est_base) FROM county_population_csv cpc WHERE est_base = 'base';
SELECT count(est_base) FROM county_population_csv cpc WHERE est_base = 'est';
SELECT * FROM county_population_csv cpc ;

 -- Update land_value_estimate by calling value estimation function


SELECT state, county, land_value_estimate, est_base, comps FROM county_population_csv cpc
 WHERE trim(cpc.state) = 'Georgia'
 AND cpc.county = 'Seminole County'
 AND CAST (date_part('year', cpc.date_code) AS varchar) = '2018';

SELECT * FROM est_LandValue(3.0::decimal, 0.2::decimal, 5::int) AS est;

SELECT est_value::int FROM est_LandValue(20::decimal, 1::decimal, 2::int)
	WHERE est_state = 'Georgia'
	AND est_county = 'Seminole County';

UPDATE county_population_csv cpc
	SET land_value_estimate = est.est_value::int, est_base = '(20,1,2)'
	FROM est_LandValue(20::decimal, 1::decimal, 2::int) AS est	
	WHERE trim(cpc.state) = est.est_state 
	AND cpc.county = est.est_county 
	AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018'
	AND cpc.est_base = 'est'
	AND cpc.county = 'Seminole County'
	AND trim(cpc.state) = 'Georgia';

UPDATE county_population_csv cpc
	SET land_value_estimate = 'test', est_base = 'test', comps = 'test'
	LIMIT 1;
	

UPDATE county_population_csv cpc
	SET land_value_estimate = 'estimate', est_base = 'est'
	WHERE trim(cpc.state) = 'Georgia'
	AND cpc.county = 'Seminole County'
	AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018';

 -- Playground to optimize query in above value estimation
 
SELECT A.state, A.county, C.land_value_asis_all, E.population, B.state, B.county, D.land_value_asis_all, f.population,
			ST_Distance(A.geom, B.geom) AS dist
		FROM county_latlong_csv AS A	
		INNER JOIN county_latlong_csv AS B
			ON ST_Distance(A.geom, B.geom) < 10.0
			AND A.state = 'Georgia'
			AND A.county = 'Seminole County'
		INNER JOIN county_landdata_csv AS D
			ON B.state = D.state 
			AND B.county = D.county
			AND D.yr = '2018'
		INNER JOIN county_population_csv AS E
			ON A.state = trim(E.state)
			AND A.county = E.county
			AND CAST(date_part('year', E.date_code) AS varchar) = '2018'
		INNER JOIN county_population_csv AS F
			ON B.state = trim(F.state)
			AND B.county = F.county
			AND CAST(date_part('year', F.date_code) AS varchar) = '2018'
			AND abs(E.population - F. population) < E.population*5
		FULL OUTER JOIN county_landdata_csv AS C
			ON A.state = C.state 
			AND A.county = C.county 
			AND C.yr = '2018'
			WHERE C.land_value_asis_all IS NULL			
		;


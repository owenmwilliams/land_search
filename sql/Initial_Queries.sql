 -- Query on land cost, population, and land share

SELECT clc.yr, clc.county, clc.state, clc2.lat, clc2.long, clc.land_value_asis_all, clc.land_share_all, cpc.population 
	FROM county_landdata_csv clc 
	JOIN county_population_csv cpc 
		ON clc.county = cpc.county 
		AND clc.yr = CAST(date_part('year', cpc.date_code) AS varchar)
		AND clc.state = trim(cpc.state)
	JOIN county_latlong_csv clc2 
		ON clc.county = clc2.county
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


 -- Query ON above + nearby recreation

WITH	cte AS (
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

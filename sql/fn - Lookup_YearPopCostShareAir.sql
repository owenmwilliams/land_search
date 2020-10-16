 -- Query on land cost, population, land share, and nearby airports

 
CREATE OR REPLACE FUNCTION lookup_YrCostPopShareAir (
	REF refcursor, a varchar(100), b int, c int, d decimal, e decimal
	)
	RETURNS refcursor AS $$
	BEGIN 
		OPEN REF FOR 
			WITH cte AS (
				SELECT one.county, one.state, two.loc_id, two.commercial_ops, ST_Distance(one.geom, two.geom) as dist
					FROM county_latlong_csv as one
					CROSS JOIN major_airports_csv as two
					WHERE ST_Distance(one.geom, two.geom) < e
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
				WHERE clc.yr = a
					AND cpc.population < b
					AND clc.land_value_asis_all < c
					AND clc.land_share_all < d
					AND sort.rn = 1
				ORDER BY county, state;
		RETURN REF;
	END;
	$$ LANGUAGE plpgsql;
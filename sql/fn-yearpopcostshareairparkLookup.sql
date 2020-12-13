 -- Query on land cost, population, land share, nearby airports, and nearby parks

 
CREATE OR REPLACE FUNCTION lookup_YrCostPopShareAirPark (
	REF refcursor, a varchar(100), b int, c int, d decimal, e decimal, f decimal, g int
	)
	RETURNS refcursor AS $$
	BEGIN 
		OPEN REF FOR 
			WITH cte AS (
				SELECT one.county, one.state, two.loc_id, two.commercial_ops, ST_Distance(one.geom, two.geom) as dist
					FROM countylatlong as one
					CROSS JOIN placeairports as two
					WHERE ST_Distance(one.geom, two.geom) < e
			), sort AS (
				SELECT *, row_number() OVER (PARTITION BY state, county ORDER BY dist) as rn
					FROM cte
			), clp AS (
				SELECT three.county, three.state, four.gnis_id, four.unit_name, four.lat, four.long, ST_Distance(three.geom, four.geom) AS dist 
					FROM countylatlong AS three
					CROSS JOIN placerecreation AS four
					WHERE ST_Distance(three.geom, four.geom) < f
			), sortp AS (
				SELECT distinct(county), count(*) AS num_parks, state
					FROM clp
					WHERE county IS NOT NULL
					GROUP BY county, state
			)
			SELECT clc.state, clc.county, sort.loc_id, sort.dist, sort.commercial_ops, sortp.num_parks, clc.land_value_asis_all, clc.land_share_all, cpc.population
				FROM countylandvalue clc
				JOIN sort
					ON sort.county = clc.county 
					AND sort.state = clc.state
				JOIN sortp 
					ON sortp.county = clc.county 
					AND sortp.state = clc.state 
				JOIN countydataset cpc
					ON clc.county = cpc.county 
					AND clc.yr = CAST(date_part('year', cpc.date_code) AS varchar)
					AND clc.state = trim(cpc.state)
				WHERE clc.yr = a
					AND cpc.population < b
					AND clc.land_value_asis_all < c
					AND clc.land_share_all < d
					AND sort.rn = 1
					AND sortp.num_parks > g
				ORDER BY state, num_parks DESC, land_value_asis_all ASC ;
		RETURN REF;
	END;
	$$ LANGUAGE plpgsql;
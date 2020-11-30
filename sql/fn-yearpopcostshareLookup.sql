 -- Query on land cost, population, and land share

 
CREATE OR REPLACE FUNCTION lookup_YrCostPopShare (
	REF refcursor, a varchar(100), b int, c int, d decimal
	)
	RETURNS refcursor AS $$
	BEGIN 
		OPEN REF FOR 
			SELECT clc.yr, clc.county, clc.state, clc2.lat, clc2.long, clc.land_value_asis_all, clc.land_share_all, cpc.population 
				FROM county_landdata_csv clc 
				JOIN county_population_csv cpc 
					ON clc.county = cpc.county 
					AND clc.yr = CAST(date_part('year', cpc.date_code) AS varchar)
					AND clc.state = trim(cpc.state)
				JOIN county_latlong_csv clc2 
					ON clc.county = clc2.county
					AND clc.state = clc2.state
				WHERE clc.yr = a
					AND cpc.population < b
					AND clc.land_value_asis_all < c
					AND clc.land_share_all < d
				ORDER BY land_value_asis_all;
		RETURN REF;
	END;
	$$ LANGUAGE plpgsql;
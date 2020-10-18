 -- SET up estimator AS a FUNCTION on distance, population range, and number of comps

 DROP FUNCTION est_landvalue(numeric,numeric,integer);
 
CREATE OR REPLACE FUNCTION est_LandValue (
	x decimal, y decimal, z int
	)
	RETURNS TABLE (
		est_state varchar(40), est_county varchar(100), est_dist decimal, est_count int, est_value decimal
	)
	LANGUAGE plpgsql
	AS $$
	BEGIN 
		RETURN QUERY 
			WITH comp_select AS (			
			SELECT A.state AS est_st, A.county AS est_cty, C.land_value_asis_all AS est_lv, E.population AS est_pop, 
				B.state AS comp_st, B.county AS comp_cty, D.land_value_asis_all AS comp_lv, F.population AS comp_pop,
				ST_Distance(A.geom, B.geom) AS dist
			FROM county_latlong_csv AS A	
			INNER JOIN county_latlong_csv AS B
				ON ST_Distance(A.geom, B.geom) < x
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
				AND abs(E.population - F. population) < E.population*y
			FULL OUTER JOIN county_landdata_csv AS C
				ON A.state = C.state 
				AND A.county = C.county 
				AND C.yr = '2018'
				WHERE C.land_value_asis_all IS NULL
			),
			interim_table AS (
				SELECT est_st::varchar, est_cty::varchar, avg(dist)::decimal, count(comp_cty)::int AS comp_count, avg(comp_lv)::decimal AS comp_avg
					FROM comp_select
						GROUP BY est_st, est_cty
				)
			SELECT * FROM interim_table WHERE comp_count > z;		
	END;
	$$
 -- SET up estimator AS a FUNCTION on distance, population range, and number of comps

-- DROP FUNCTION est_landvalue(numeric,numeric,integer);
 
CREATE OR REPLACE FUNCTION est_LandValue (
	x decimal, y decimal, g varchar, h varchar
	)
--	RETURNS TABLE (
--		est_state varchar(40), est_county varchar(100), est_dist decimal, est_count int, est_value decimal
--	)
	RETURNS TABLE (
		est_st varchar(40), est_cty varchar(100), est_lv int, est_pop int
		, comp_st varchar(40), comp_cty varchar(100), comp_lv int, comp_pop int
		, dist decimal
	)	
	LANGUAGE plpgsql
	AS $$
	BEGIN 
		RETURN QUERY 
			WITH comp_select AS (			
			SELECT A.state AS est_st, A.county AS est_cty, C.land_value_asis_all::int AS est_lv, E.population AS est_pop, 
				B.state AS comp_st, B.county AS comp_cty, D.land_value_asis_all::int AS comp_lv, F.population AS comp_pop,
				ST_Distance(A.geom, B.geom)::decimal AS dist
			FROM county_latlong_csv AS A	
			INNER JOIN county_latlong_csv AS B
				ON ST_Distance(A.geom, B.geom) < x
				AND A.state = g
				AND A.county = h
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
			)
			SELECT * FROM comp_select;
	END;
	$$
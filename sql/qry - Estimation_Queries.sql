 -- Return one county, state for estimation function

SELECT county, state
	FROM county_population_csv cpc 
		WHERE land_value_estimate = 'estimate' 
		AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018'
	LIMIT 1;
	
 -- RETURN list OF comp cty, state

CREATE TABLE testtable AS SELECT * FROM est_LandValue(10, 3, 5, 'Georgia', 'Seminole County');

 -- UPDATE pop TABLE WITH restults FROM list *****COME BACK TO HERE*****

SELECT * FROM testtable;
SELECT * FROM county_population_csv cpc WHERE trim(cpc.state) = 'Georgia' AND cpc.county = 'Seminole County';

UPDATE county_population_csv cpc
	SET comps = concat(comp_st, ', ', comp_cty, '; ')
	FROM testtable	
	WHERE trim(cpc.state) = testtable.est_st
	AND cpc.county = testtable.est_cty
	AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018';
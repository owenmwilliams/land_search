 -- Return one county, state for estimation function

SELECT county, state
	FROM county_population_csv cpc 
		WHERE land_value_estimate = 'estimate' 
		AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018'
	LIMIT 1;
	

 -- RETURN list OF comp cty, state

DROP TABLE IF EXISTS testtable;

CREATE TABLE testtable AS SELECT * FROM est_LandValue(10, 3, 5, 'Georgia', 'Seminole County');
SELECT * FROM est_LandValue(10, 3, 5, 'Georgia', 'Seminole County');

SELECT * FROM testtable;

 -- UPDATE pop TABLE comps COLUMN WITH restults FROM list *****COME BACK TO HERE - UPDATE QUERY NO LONGER WORKING***** 

SELECT concat(comp_st::TEXT, ', ', comp_cty::TEXT) FROM testtable;

WITH concat_list AS (
		SELECT CONCAT(comp_st::varchar, ', ', comp_cty::varchar) FROM testtable
		)
	UPDATE county_population_csv cpc
		SET comps = subquery.concat
		FROM (SELECT STRING_AGG(concat_list::varchar, '; ') FROM concat_list) AS subquery
		WHERE trim(cpc.state) = 'Georgia'
		AND cpc.county = 'Seminole County'
		AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018';
	

SELECT comps FROM county_population_csv cpc 
	WHERE trim(cpc.state) = 'Georgia'
		AND cpc.county = 'Seminole County'
		AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018'; 
	
 -- UPDATE pop TABLE est_base COLUMN WITH query constraints FROM est query
	
UPDATE county_population_csv cpc
	SET est_base = '(10, 3, 5)'
		WHERE trim(cpc.state) = 'Georgia'
		AND cpc.county = 'Seminole County'
		AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018';
		
	
 -- UPDATE pop TABLE land_value_estimate COLUMN WITH comps FROM est query

UPDATE county_population_csv cpc
	SET land_value_estimate = subquery.lv_avg::int
	FROM (SELECT avg(comp_lv) AS lv_avg FROM testtable t WHERE t.est_st = 'Georgia' AND t.est_cty = 'Seminole County') AS subquery
		WHERE trim(cpc.state) = 'Georgia'
		AND cpc.county = 'Seminole County'
		AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018';
		
	
 -- Checking population table for correct updates
	
SELECT * FROM county_population_csv cpc WHERE trim(cpc.state) = 'Georgia'
		AND cpc.county = 'Seminole County'
		AND CAST(date_part('year', cpc.date_code) AS varchar) = '2018';
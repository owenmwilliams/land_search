 -- Create a view of 2019 population data by county
CREATE MATERIALIZED VIEW public.county_pop_2019 AS 
	SELECT DISTINCT state, county, name, pop FROM census_table
	WHERE race = 0
	AND sex = 0
	AND age_group = 0
	AND hisp = 0
	AND date_code = 12
	ORDER BY name;
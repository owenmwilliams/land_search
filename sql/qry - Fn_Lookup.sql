-- BEGIN;
-- SELECT lookup_YrCostPopShare('mycur', 2018::varchar, 100000::integer, 30000::integer, 0.2::decimal);
-- FETCH ALL IN "mycur";
-- COMMIT;

-- BEGIN;
-- SELECT lookup_YrCostPopShareAir('mycur', 2018::varchar, 100000::integer, 30000::integer, 0.2::decimal, 1.5::decimal);
-- FETCH ALL IN "mycur";
-- COMMIT;

-- BEGIN;
-- SELECT lookup_YrCostPopShareAirPark('mycur', 2018::varchar, 100000::integer, 20000::integer, 0.2::decimal, 1.5::decimal, 2.5::decimal, 5::integer);
-- FETCH ALL IN "mycur";
-- COMMIT;
 
 BEGIN;
 SELECT est_LandValue('mycur', 3.0, 0.2, 5);
 FETCH ALL IN "mycur";
 COMMIT;
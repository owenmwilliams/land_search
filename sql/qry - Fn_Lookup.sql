-- BEGIN;
-- SELECT lookup_YrCostPopShare('mycur', 2018::varchar, 100000::integer, 30000::integer, 0.2::decimal);
-- FETCH ALL IN "mycur";
-- COMMIT;

-- BEGIN;
-- SELECT lookup_YrCostPopShareAir('mycur', 2018::varchar, 100000::integer, 30000::integer, 0.2::decimal, 1.5::decimal);
-- FETCH ALL IN "mycur";
-- COMMIT;

 BEGIN;
 SELECT lookup_YrCostPopShareAirPark('mycur', 2018::varchar, 100000::integer, 30000::integer, 0.2::decimal, 1.5::decimal, 2.0::decimal, 4::integer);
 FETCH ALL IN "mycur";
 COMMIT;
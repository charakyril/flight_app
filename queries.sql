-- Query 1: Find airline with the highest number of travelers whose age is less than X and greater than Y.
-- Use the year_of_birth bounds: year_low = current_year - max(X,Y); year_high = current_year - min(X,Y)
SELECT a.name AS airline_name,
       COUNT(p.id) AS traveler_count
FROM passengers p, flights_has_passengers fhp, flights f, routes r, airlines a
WHERE p.id = fhp.passengers_id
  AND fhp.flights_id = f.id
  AND f.routes_id = r.id
  AND r.airlines_id = a.id
  AND p.year_of_birth > 1988  -- replace with year_low
  AND p.year_of_birth < 2002  -- replace with year_high
GROUP BY a.id, a.name
ORDER BY traveler_count DESC;

-- Query 2: Find total visitors per airport served by airline X between dates A and B.
SELECT air.name AS airport_name,
       COUNT(fhp.passengers_id) AS visitor_count
FROM airlines a, routes r, airports air, flights f, flights_has_passengers fhp
WHERE a.id = r.airlines_id
  AND r.destination_id = air.id
  AND f.routes_id = r.id
  AND fhp.flights_id = f.id
  AND a.name = 'Aegean Airlines'  -- replace with airline name
  AND f.date BETWEEN '2026-01-01' AND '2026-12-31'  -- replace with dates
GROUP BY air.id, air.name
ORDER BY visitor_count DESC;

-- Query 3: Find alternative flights for travel from city A to city B on date X for active airlines.
SELECT f.id AS flight_id,
       al.name AS airline_name,
       arr.name AS destination_airport,
       airpl.model AS airplane_model
FROM flights f, routes r, airlines al, airports arr, airports dep, airplanes airpl
WHERE f.routes_id = r.id
  AND r.airlines_id = al.id
  AND r.destination_id = arr.id
  AND r.source_id = dep.id
  AND f.airplanes_id = airpl.id
  AND dep.city = 'Athens'        -- replace with source city
  AND arr.city = 'Paris'         -- replace with destination city
  AND f.date = '2026-06-15'     -- replace with travel date
  AND al.active = 'Y';

-- Query 4: Find the N airlines with the highest number of flights.
SELECT a.name AS airline_name,
       a.code AS airline_code,
       COUNT(aa.airplanes_id) AS airplane_count,
       COUNT(f.id) AS flight_count
FROM airlines a, routes r, flights f, airlines_has_airplanes aa
WHERE a.id = r.airlines_id
  AND f.routes_id = r.id
  AND aa.airlines_id = a.id
  AND a.active = 'Y'
GROUP BY a.id, a.name, a.code
ORDER BY flight_count DESC;

-- Query 5: Update passenger tier categories for a specific airline.
-- First run the SELECT to confirm counts, then use the application to update the tier column.
SELECT p.id AS passenger_id,
       p.name,
       p.surname,
       COUNT(*) AS flight_count
FROM passengers p, flights_has_passengers fhp, flights f, routes r, airlines a
WHERE p.id = fhp.passengers_id
  AND fhp.flights_id = f.id
  AND f.routes_id = r.id
  AND r.airlines_id = a.id
  AND a.name = 'Aegean Airlines'  -- replace with airline name
GROUP BY p.id, p.name, p.surname
ORDER BY flight_count DESC;

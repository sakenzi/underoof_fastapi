# underoof_fastapi

UPDATE locations
SET geom = ST_SetSRID(ST_MakePoint(CAST(longitude AS DOUBLE PRECISION), CAST(latitude AS DOUBLE PRECISION)), 4326)
WHERE geom IS NULL;


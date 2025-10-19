# underoof_fastapi

UPDATE locations
SET geom = ST_SetSRID(ST_MakePoint(CAST(longitude AS DOUBLE PRECISION), CAST(latitude AS DOUBLE PRECISION)), 4326)
WHERE geom IS NULL;

ipconfig getifaddr en0


1. CREATE EXTENSION postgis;

2. python address.py

3. INSERT INTO public.roles(
	role_name)
	VALUES ('Арендодатель'),('Арендатор');

4. INSERT INTO public.type_advertisements(
	type_name)
	VALUES ('По часам'),('Посуточно'),('Помесячно');

5. sudo journalctl -u fastapi.service -f
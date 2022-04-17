ALTER TABLE address ADD COLUMN IF NOT EXISTS latitude float8;
ALTER TABLE address ADD COLUMN IF NOT EXISTS longitude float8;
DROP FUNCTION IF EXISTS filter_addresses();
CREATE OR REPLACE FUNCTION filter_addresses()
RETURNS TABLE (
		address character varying(50),
		address_id int
)
LANGUAGE plpgsql
AS $$
DECLARE 
BEGIN
return query
	SELECT A.address, A.address_id FROM address A
		WHERE A.city_id > 400 AND A.city_id < 600 AND A.address LIKE '%11%';
END;
$$
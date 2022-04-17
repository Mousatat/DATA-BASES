
DROP FUNCTION IF EXISTS customer_pagination;
CREATE OR REPLACE FUNCTION customer_pagination(from_ integer, to_ integer)
  RETURNS TABLE(customer_id INTEGER, first_name character varying(45), last_name character varying(45), address_id SMALLINT) AS
$$

BEGIN

    IF from_ < 0 OR from_ > 600 OR to_ < 0 OR to_ > 600 THEN 
        RAISE EXCEPTION 'Each input must be between 0 and 600!';
    ELSE
    
        RETURN QUERY
        
        SELECT C.customer_id, C.first_name, C.last_name, C.address_id
        FROM customer C
        WHERE C.address_id >= from_ AND C.address_id <= to_;
    END IF;
END; $$

LANGUAGE plpgsql;
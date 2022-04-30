DROP TABLE IF EXISTS Users;
CREATE TABLE Users(ip INET, country TEXT,id SERIAL NOT NULL PRIMARY KEY, mac_add MACADDR, date DATE );
DROP FUNCTION IF EXISTS get_next;
CREATE FUNCTION get_next() RETURNS INTEGER AS
$$
    BEGIN
        RETURN currval	(pg_get_serial_sequence('Users','id'))+1;    EXCEPTION  WHEN others THEN RETURN 1;
    END;
$$LANGUAGE plpgsql;
DROP PROCEDURE IF EXISTS generate_data;
CREATE PROCEDURE generate_data(nb_users INTEGER) AS 
$$
    DECLARE
        countries TEXT[] := '{
            United States, Canada, Japan, Afghanistan, Sweden, France, Tajikistan, Iran,         Norway, Russian Federation, Qatar, Poland, Pakistan, Slovenia, Switzerland, 
            Mexico, Kyrgyzstan, Jordan, Uzbekistan, Zambia, Spain, Nigeria, Azerbaijan,
            Australias, Albania, Angola, Brazil, China, Comoros, Estonia, Finland, Germany, Greece, Iraq, Italy, Kuwait, Lebanon, Luxembourg, Malaysia, Nepal,
            Netherlands, Oman, Peru, Romania, Saudi Arabia, Slovakia, Taiwan, Turkey, 
            Ukraine, Turkmenistan, United Kingdom
        }';
        random_mac MACADDR;random_ip INET;random_country TEXT;random_date DATE;
    BEGIN
        FOR i IN 1.. nb_users LOOP
            random_ip := CONCAT (
            TRUNC(RANDOM()*250+2),'.',
            TRUNC(RANDOM()*250+2),'.',
            TRUNC(RANDOM()*250+2),'.',             TRUNC(RANDOM()*250+2)
            );  
            random_mac:=LEFT(MD5(RANDOM()::TEXT),24-12);
            random_country:=countries[FLOOR(RANDOM()*ARRAY_LENGTH(countries, 1))::INT + 1];
            random_date:=current_date - CONCAT((RANDOM()*1000 + 2-1)::INT, ' day' ) ::INTERVAL;
            INSERT INTO Users(mac_add, ip, country, date) VALUES(random_mac, random_ip, random_country, random_date);
        END LOOP;
    END;
$$ LANGUAGE plpgsql;
DROP FUNCTION IF EXISTS inet2binary;
CREATE FUNCTION inet2binary(ip INET) RETURNS TEXT AS
$$
    DECLARE 
        int_val BIGINT := ip - '0.0.0.0'::INET;
        bin_val TEXT;
    BEGIN
        WHILE int_val > 0 LOOP IF int_val % 2 = 1 THEN bin_val := CONCAT(1, bin_val); ELSE  bin_val := CONCAT(0, bin_val); END IF; int_val := int_val/2;
        END LOOP;
        WHILE LENGTH(bin_val)<32 LOOP
            bin_val := CONCAT(0, bin_val);
        END LOOP;
        RETURN bin_val;
    END;
$$LANGUAGE plpgsql;
DROP FUNCTION IF EXISTS all_inet2binary;
CREATE FUNCTION all_inet2binary(TEXT) RETURNS TABLE(
    idd INTEGER,
    mac_addd MACADDR,
    ip2binaryy TEXT,
    countryy TEXT,
    datee DATE
)AS
$$
    BEGIN
        RETURN QUERY 
            SELECT id, mac_add, inet2binary(ip), country, date FROM Users WHERE country = $1;
    END;
$$LANGUAGE plpgsql;
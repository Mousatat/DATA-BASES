DROP TABLE IF EXISTS Customers CASCADE;
DROP TABLE IF EXISTS Products CASCADE;
DROP TABLE IF EXISTS Purchases CASCADE;
DROP TABLE IF EXISTS Purchases_products_list CASCADE;
DROP TABLE IF EXISTS Sales CASCADE;
CREATE TABLE Purchases(
customer_id INTEGER NOT NULL,
id SERIAL NOT NULL PRIMARY KEY,  
FOREIGN KEY (customer_id) REFERENCES Customers(id)
);
CREATE TABLE Products(
details TEXT,
price NUMERIC NOT NULL,
id SERIAL NOT NULL PRIMARY KEY,
name TEXT NOT NULL,
type TEXT
);
CREATE TABLE Customers(
address TEXT NOT NULL,
name TEXT NOT NULL,  
id SERIAL NOT NULL PRIMARY KEY,
review TEXT NOT NULL
);
CREATE TABLE Purchases_products_list
product_id INTEGER NOT NULL,
FOREIGN KEY (purchase_id) REFERENCES Purchases(id),
FOREIGN KEY (product_id) REFERENCES Products(id),
id SERIAL NOT NULL PRIMARY KEY,
purchase_id INTEGER NOT NULL
);
CREATE TABLE Sales(
id SERIAL NOT NULL PRIMARY KEY,
type TEXT NOT NULL,
discount NUMERIC NOT NULL
);
DROP INDEX IF EXISTS idx1;
DROP INDEX IF EXISTS idx2;
CREATE OR REPLACE FUNCTION query1()
RETURNS SETOF TEXT AS
$$
BEGIN
return QUERY
EXPLAIN ANALYZE SELECT DISTINCT Pr.name AS product_name, S.discount AS discount FROM Purchases_products_list AS PP, Products AS Pr, Sales AS S, Purchases AS Pu
WHERE PP.purchase_id = Pu.id AND Pr.type = S.type AND PP.product_id = Pr.id AND Pu.customer_id = 3;
END
$$ LANGUAGE plpgsql;
CREATE OR REPLACE FUNCTION query2()
RETURNS SETOF TEXT AS
$$
BEGIN
return QUERY
EXPLAIN ANALYZE SELECT Pu.customer_id, SUM(S.discount * Pr.price) FROM Purchases_products_list AS PP, Products AS Pr, Sales AS S, Purchases AS Pu
WHERE PP.product_id = Pr.id AND PP.purchase_id = Pu.id AND Pr.type = S.type GROUP BY Pu.customer_id;
END
$$ LANGUAGE plpgsql;
SELECT * FROM query1();
SELECT * FROM query2();
CREATE INDEX idx1 ON Products USING HASH (type);
CREATE INDEX idx2 ON Sales USING HASH (type);
SELECT * FROM query1();
SELECT * FROM query2();
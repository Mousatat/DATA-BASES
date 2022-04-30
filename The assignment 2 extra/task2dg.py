from enum import unique
import psycopg2
from faker import Faker
con = psycopg2.connect(user='postgres', password='1234', host='127.0.0.1', port='5432', database='task2')
cur = con.cursor()
fake = Faker()
numberOfTypes = 50
types = []
for i in range(numberOfTypes):
    types.append(fake.word())
numberOfCustomers = 1000
for i in range(1, numberOfCustomers + 1):
    name, address, review = fake.name(), fake.address(), fake.text()
    cur.execute(
        f'''
        INSERT INTO Customers (name, address, review) VALUES ('{name}', '{address}', '{review}');
        '''
    )
    con.commit()
print(f"{numberOfCustomers} customers is added")
numberOfProducts = 1000
for i in range(1, numberOfProducts + 1):
    name, details, price, type = fake.text(max_nb_chars=50), fake.text(), fake.random_int(min=1, max=100), fake.random_element(elements=types)
    cur.execute(
        f'''
        INSERT INTO Products (name, details, price, type) VALUES ('{name}', '{details}', '{price}', '{type}');
        '''
    )
    con.commit()
print(f"{numberOfProducts} products is added")
numberOfPurchases = 1000
for i in range(1, numberOfPurchases + 1):
    customer_id = fake.random_int(min=1, max=numberOfCustomers)
    cur.execute(
        f'''
        INSERT INTO Purchases (customer_id) VALUES ({customer_id});
        '''
    )
    con.commit()
print(f"{numberOfPurchases} purchases is added")
numberOfSales = 18
for type in fake.random_elements(elements = types, length = numberOfSales, unique = True):
    discount = fake.random_int(min = 1, max = 100) / 100
    cur.execute(
        f'''
        INSERT INTO Sales (type, discount) VALUES ('{type}', {discount});
        '''
    )
    con.commit()
print(f"{numberOfSales} sales discount is added")
nbPurPro = 10000
for i in range(1, nbPurPro + 1):
    product_id = fake.random_int(min=1, max=numberOfProducts)
    purchase_id = fake.random_int(min=1, max=numberOfPurchases)
    cur.execute(
        f'''
        INSERT INTO Purchases_products_list (product_id, purchase_id) VALUES ({product_id}, {purchase_id});
        '''
    )
    con.commit()
print(f"{nbPurPro} purchase_product is added")
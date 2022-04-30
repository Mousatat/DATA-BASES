import psycopg2, datetime
from faker import Faker
con = psycopg2.connect(user='postgres', database='customers', password='1234', host='127.0.0.1', port='5432')
cur = con.cursor()
start = datetime.datetime.now()
# cur.execute(
#     '''
#     DROP TABLE IF EXISTS Customer;
#     '''
# )
# con.commit()
# cur.execute(
#     '''
#     CREATE TABLE Customer(
#         id SERIAL NOT NULL PRIMARY KEY, 
#         name TEXT NOT NULL,
#         address TEXT NOT NULL,
#         review TEXT  
#     );  
#     '''
# )
# con.commit()
# fake = Faker()
# numberOfCustomers = 1000000
# print( f"{numberOfCustomers} customers have to be added ...")
# for i in range(1, numberOfCustomers + 1):
#     if i % (numberOfCustomers/10) == 0:
#         print(f"{i} customers have been added...")
#     name, address, review = fake.name(), fake.address(), fake.text()
#     cur.execute(
#         f'''
#         INSERT INTO Customer (name, address, review) VALUES ('{name}', '{address}', '{review}');
#         '''
#     )
#     con.commit()
# print(f"All {numberOfCustomers} customers have been added!\n")
q1 = "EXPLAIN ANALYZE SELECT * FROM Customer WHERE review LIKE '%John%';"
q2 = "EXPLAIN ANALYZE SELECT * FROM Customer WHERE address = 'John';"
q3 = "EXPLAIN ANALYZE SELECT * FROM Customer WHERE address BETWEEN 'J' AND 'Q';"
q4 = "EXPLAIN ANALYZE SELECT * FROM Customer WHERE name LIKE '%Smith%';"
def query1():
    cur.execute( q1 )
    print( cur.fetchall()[0] )
def query2():
    cur.execute( q2 )
    print( cur.fetchall()[0] )
def query3():
    cur.execute( q3 )
    print( cur.fetchall()[0] )
def query4():
    cur.execute( q4 )
    print( cur.fetchall()[0] )
def checkHASH():
    cur.execute(
        '''
        CREATE INDEX hash1 ON Customer USING HASH (address);
        '''
    )
    con.commit()
    query2()
    cur.execute(
        '''
        DROP INDEX IF EXISTS hash1;
        '''
    )
    con.commit()
def checkBTREE():
    cur.execute(
        '''
        CREATE INDEX btree1 ON Customer USING BTREE (address);
        '''
    )
    con.commit()
    query3()
    cur.execute(
        '''
        DROP INDEX IF EXISTS btree1;
        '''
    )
    con.commit()
def checkGIN():
    cur.execute(
        '''
        CREATE EXTENSION IF NOT EXISTS pg_trgm;
        '''
    )
    con.commit()
    cur.execute(
        '''
        CREATE INDEX gin1 ON Customer USING GIN ( review gin_trgm_ops );
        '''
    )
    con.commit()
    query1()
    cur.execute(
        '''
        DROP INDEX IF EXISTS gin1;
        '''
    )
    con.commit()
def checkGIST():
    cur.execute(
        '''
        CREATE EXTENSION IF NOT EXISTS pg_trgm;
        '''
    )
    con.commit()
    cur.execute(
        '''
        CREATE INDEX gist1 ON Customer USING GIST ( name gist_trgm_ops );
        '''
    )
    con.commit()
    query4()

    cur.execute(
        '''
        DROP INDEX IF EXISTS gist1;
        '''
    )
    con.commit()
print('-')
print("\nThe query below is going to be run before and after GIN index creation:")
print('\t', q1)
print('Before GIN: ')
query1()
print('\nAfter GIN (takes some time for GIN to be created. Please wait): ')
checkGIN()
print('-')
print("\nThe query below is going to be run before and after GIST index creation:")
print('\t', q4)
print('Before GIST: ')
query4()
print('\nAfter GIST (takes some time for GIN to be created. Please wait): ')
checkGIST()
print('-')
print("\nThe query below is going to be run before and after HASH index creation:")
print('\t', q2)
print('Before HASH: ')
query2()
print('\nAfter HASH (takes some time for HASH to be created. Please wait): ')
checkHASH()
print('-')
print("\nThe query below is going to be run before and after BTREE index creation:")
print('\t', q3)
print('Before BTREE: ')
query3()
print('\nAfter BTREE (takes some time for BTREE to be created. Please wait): ')
checkBTREE()
print('-')
end = datetime.datetime.now()
amount = end - start
print(f"\nElapsed time of Python script: {amount.microseconds} ms")

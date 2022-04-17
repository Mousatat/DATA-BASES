from geopy.geocoders import Nominatim
import psycopg2

geolocator = Nominatim(user_agent="Mozilla/5.0")



conn = psycopg2.connect(database="vdrental", user="postgres",
                       password="8Rametago8", host="127.0.0.1", port="5432")

cur = conn.cursor()


cur.callproc('filter_addresses', ())

rows = cur.fetchall()

for row in rows:
    print(row[1]," - ",row[0])
    lat = 0
    long = 0

    try:
        location = geolocator.geocode(row[0])
        #print(location.address)
        lat = location.latitude
        long = location.longitude
    except:
        lat = 0
        long = 0
    
    print(lat, long)

    update_sql = "UPDATE address SET latitude = %s, longitude = %s WHERE address_id = %s"
    val = (lat, long, row[1])

    cur.execute(update_sql, val)
    conn.commit()
  

sql = '''SELECT * FROM filter_addresses(), address
WHERE address.address_id = filter_addresses.address_id'''

cur.execute(sql)

ans = cur.fetchall()

for i in ans:
    print(i)

cur.close()
conn.close()

print("FINISHED!")
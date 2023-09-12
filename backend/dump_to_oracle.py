import datetime
import cx_Oracle
import logging
import csv
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

db_conf = {}
with open('db.json', 'r') as f:
    db_conf.update(json.loads(f.read()))

db_conn = cx_Oracle.connect(db_conf['username'], db_conf['password'], f"{db_conf['host']}:{db_conf['port']}/{db_conf['db']}")
db_cursor=db_conn.cursor()


def create_table():
    sql = "CREATE TABLE CITY_ATTRIBUTES (ID INT NOT NULL , CITY VARCHAR2(40), COUNTRY VARCHAR2(40) , LONGITUDE FLOAT , LATITUDE FLOAT , CONSTRAINT TABLE1_PK PRIMARY KEY (ID) ENABLE )"
    db_cursor.execute(sql)
    print(f"CITY_ATTRIBUTES created...")
    attrs = ['humidity', 'pressure', 'temperature', 'weather_description', 'wind_direction', 'wind_speed']
    for attr in attrs:
        sql = f"CREATE TABLE {attr} (TIME_POINT DATE, VALUE {'FLOAT' if attr!='weather_description' else 'VARCHAR2(40)'}, CITY_ID INT)"
        db_cursor.execute(sql)
        print(f"{attr} created...")
    db_conn.commit()

def insert2city():
    sql_cmd = "insert into city_attributes (id, city, country, latitude, longitude) values " \
            "(:id, :city, :country,:latitude,:longitude)"
    i = 0
    lines = []
    with open('data/city_attributes.csv', 'r') as f:
        c_reader = csv.reader(f)
        next(c_reader)
        for line in c_reader:
            lines.append([i, line[0].strip(), line[1].strip(), float(line[2].strip()), float(line[3].strip())])
            i += 1
    # print(lines)
    db_cursor.executemany(sql_cmd,lines)
    db_conn.commit()
    print('city data inserted')


def insert2other():
    sql = "select id, city from city_attributes"
    db_cursor.execute(sql)
    city_data = db_cursor.fetchall()
    cities = {}
    for city in city_data:
        cities[city[1]] = city[0]

    w = 'weather_description'
    attrs = ['humidity', 'pressure', 'temperature', 'wind_direction', 'wind_speed', 'weather_description']
    # attrs = ['weather_description']
    for attr in attrs:
        sql = f"insert into {attr} (time_point, value, city_id) values (:time_point, :value, :city_id)"
        data = []
        with open(f'data/{attr}.csv', 'r') as f:
            csv_reader = csv.reader(f)
            head = next(csv_reader)
            ind2city = {}
            for i, a in enumerate(head):
                if i > 0:
                    ind2city[i] = cities[a.strip()]
            for line in csv_reader:
                line_time = line[0].strip()
                try:
                    line_time_t = datetime.datetime.strptime(line_time, '%Y-%m-%d %H:%M:%S')
                except:
                    line_time_t = datetime.datetime.strptime(line_time, '%Y/%m/%d %H:%M')
                for i in range(1, len(line)):
                    if line[i] is not None and line[i]!='':
                        value=line[i].strip()
                        if attr!='weather_description':
                            value = float(value)
                        city_id = ind2city[i]
                        data.append([line_time_t, value, city_id])
        db_cursor.executemany(sql, data)
        db_conn.commit()
        print(f'{attr} all done, total={len(data)}')


if __name__=="__main__":
    create_table()
    insert2city()
    insert2other()
    # sql = 'select * from humidity where value=93'
    # db_cursor.execute(sql)
    # print(db_cursor.fetchall())
    db_cursor.close()
    db_conn.close()
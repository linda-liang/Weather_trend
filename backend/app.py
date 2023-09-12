import logging
from flask import Flask, request, jsonify
import json
import datetime
import cx_Oracle

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

db_conf = {}
with open('db.json', 'r') as f:
    db_conf.update(json.loads(f.read()))

db_conn = cx_Oracle.connect(db_conf['username'], db_conf['password'], f"{db_conf['host']}:{db_conf['port']}/{db_conf['db']}")
db_cursor = db_conn.cursor()

attrs = ['humidity', 'pressure', 'temperature', 'weather_description', 'wind_direction', 'wind_speed']

w_desc = {
    'few clouds': 1,
    'scattered clouds': 1,
    'broken clouds': 1,
    'sky is clear': 1
}


def get_city_info(city_name=None):
    sql = "select city, country, latitude, longitude, id from city_attributes"
    if city_name is not None:
        sql += ' where city=:city'
        args = {'city': city_name}
        db_cursor.execute(sql, args)
    else:
        db_cursor.execute(sql)
    city_data = db_cursor.fetchall()
    c_list = {}
    for city in city_data:
        item = {
            'city': city[0],
            'country': city[1],
            'latitude': city[2],
            'longitude': city[3],
            'id': city[4]
        }
        c_list[city[0]] = item
    return c_list


def get_city_id2name():
    sql = "select id, city from city_attributes"
    db_cursor.execute(sql)
    city_data = db_cursor.fetchall()
    c_list = {}
    for city in city_data:
        c_list[city[0]] = city[1]
    return c_list


@app.route("/city_info", methods=["POST"])
def city_info():
    cities = get_city_info()
    c_list = []
    country_list = []
    for key, value in cities.items():
        c_list.append(value)
        if value['country'] not in country_list:
            country_list.append(value['country'])
    return jsonify(success=True, content=c_list, country_list=country_list)


@app.route("/attr_info", methods=["POST"])
def attr_info():
    global attrs
    return jsonify(success=True, content=attrs)


@app.route("/city_attr_line", methods=["POST"])
def city_attr_line():
    city = request.json.get('city')
    attr = request.json.get('attr')
    time_start = request.json.get('st')
    time_end = request.json.get('et')
    time_period = request.json.get('period')
    logging.info(f"city={city},attr={attr},st={time_start},et={time_end},period={time_period}")
    time_start = datetime.datetime.strptime(time_start, '%Y-%m-%d')
    time_end = datetime.datetime.strptime(time_end, '%Y-%m-%d')
    data = {'x': [], 'y': []}
    ori_data = {}
    c_info = get_city_info(city)
    city_id = c_info[city]['id']
    pat = "%Y-%m-%d"
    if time_period == 'week':
        pat = "%Y %W"
    elif time_period == 'month':
        pat = "%Y %m"
    sql = f"select time_point, value from {attr} where city_id=:city_id and" \
          f" to_char(time_point,'YYYY-MM-DD hh24:mi:ss') between :st and :et"
    args = {'city_id': city_id, 'st': time_start.strftime('%Y-%m-%d %H:%M:%S'),
            'et': time_end.strftime('%Y-%m-%d %H:%M:%S')}
    db_cursor.execute(sql, args)
    sql_data = db_cursor.fetchall()
    for line in sql_data:
        line_time_t = line[0]
        value = line[1]
        kk = line_time_t.strftime(pat)
        if attr == 'weather_description':
            value = w_desc.get(value, 0)
        if kk in ori_data:
            ori_data[kk][0] += value
            ori_data[kk][1] += 1
        else:
            ori_data[kk] = [value, 1]
    temp = []
    for key, value in ori_data.items():
        temp.append([key, value[0] / value[1]])
    temp.sort(key=lambda x: x[0])
    for item in temp:
        data['x'].append(item[0])
        data['y'].append(item[1])
    return jsonify(success=True, content=data)


@app.route("/compare_city", methods=["POST"])
def compare_city():
    city = request.json.get('city')
    city2 = request.json.get('city2')
    city_id = get_city_info(city)[city]['id']
    city_id2 = get_city_info(city2)[city2]['id']
    attr = request.json.get('attr')
    time_start = request.json.get('st')
    time_end = request.json.get('et')
    time_period = request.json.get('period')
    logging.info(f"city={city},attr={attr},st={time_start},et={time_end},period={time_period}")
    time_start = datetime.datetime.strptime(time_start, '%Y-%m-%d')
    time_end = datetime.datetime.strptime(time_end, '%Y-%m-%d')
    data = {'x': [], 'y1': [], 'y2': []}
    ori_data = {}
    pat = "%Y-%m-%d"
    if time_period == 'week':
        pat = "%Y %W"
    elif time_period == 'month':
        pat = "%Y %m"

    sql = f"select time_point, value, city_id from {attr} where (city_id=:city_id or city_id=:city_id2) and" \
          f" to_char(time_point,'YYYY-MM-DD hh24:mi:ss') between :st and :et"
    args = {'city_id': city_id,'city_id2': city_id2, 'st': time_start.strftime('%Y-%m-%d %H:%M:%S'),
            'et': time_end.strftime('%Y-%m-%d %H:%M:%S')}
    db_cursor.execute(sql, args)
    sql_data = db_cursor.fetchall()
    for line in sql_data:
        line_time_t = line[0]
        value = line[1]
        kk = line_time_t.strftime(pat)
        if attr == 'weather_description':
            value = w_desc.get(value, 0)
        if line[2] == city_id:
            if kk in ori_data:
                ori_data[kk][0] += value
                ori_data[kk][1] += 1
            else:
                ori_data[kk] = [value, 1, 0, 0]
        else:
            if kk in ori_data:
                ori_data[kk][2] += value
                ori_data[kk][3] += 1
            else:
                ori_data[kk] = [0, 0, value, 1]
    temp = []
    for key, value in ori_data.items():
        temp.append([key, value[0] / value[1] if value[1] != 0 else 0, value[2] / value[3] if value[3] != 0 else 0])
    temp.sort(key=lambda x: x[0])
    for item in temp:
        data['x'].append(item[0])
        data['y1'].append(item[1])
        data['y2'].append(item[2])
    return jsonify(success=True, content=data)


@app.route("/ranking", methods=["POST"])
def ranking():
    attr = request.json.get('attr')
    time_start = request.json.get('st')
    time_end = request.json.get('et')
    descending = request.json.get('descending')
    time_start = datetime.datetime.strptime(time_start, '%Y-%m-%d')
    time_end = datetime.datetime.strptime(time_end, '%Y-%m-%d')
    data = {'x': [], 'y': []}
    ori_data = {}
    city_id2name = get_city_id2name()
    if attr!='weather_description':
        sql = f"select city_id, sum(value) as sum_value, count(1) as value_count from {attr} where" \
              f" to_char(time_point,'YYYY-MM-DD hh24:mi:ss') between :st and :et group by city_id"
        args = {'st': time_start.strftime('%Y-%m-%d %H:%M:%S'),
                'et': time_end.strftime('%Y-%m-%d %H:%M:%S')}
        db_cursor.execute(sql, args)
        sql_data = db_cursor.fetchall()
        temp = []
        for line in sql_data:
            temp.append([city_id2name[line[0]], line[1] / line[2] if line[2] != 0 else 0])
        temp.sort(key=lambda x: x[1], reverse=not descending)
        for item in temp:
            data['x'].append(item[0])
            data['y'].append(item[1])
    else:
        sql = f"select city_id, value from {attr} where" \
              f" to_char(time_point,'YYYY-MM-DD hh24:mi:ss') between :st and :et"
        args = {'st': time_start.strftime('%Y-%m-%d %H:%M:%S'),
                'et': time_end.strftime('%Y-%m-%d %H:%M:%S')}
        db_cursor.execute(sql, args)
        sql_data = db_cursor.fetchall()
        for line in sql_data:
            city_name = city_id2name[line[0]]
            value = w_desc.get(line[1], 0)
            if city_name in ori_data:
                ori_data[city_name][0] += value
                ori_data[city_name][1] += 1
            else:
                ori_data[city_name] = [value, 1]
        temp = []
        for key, value in ori_data.items():
            temp.append([key, value[0] / value[1] if value[1] != 0 else 0])
        temp.sort(key=lambda x: x[1], reverse=not descending)
        for item in temp:
            data['x'].append(item[0])
            data['y'].append(item[1])
    return jsonify(success=True, content=data)


@app.route("/analyze", methods=["POST"])
def analyze():
    attr = request.json.get('attr')
    attr2 = request.json.get('attr2')
    time_start = request.json.get('st')
    time_end = request.json.get('et')
    time_start = datetime.datetime.strptime(time_start, '%Y-%m-%d')
    time_end = datetime.datetime.strptime(time_end, '%Y-%m-%d')
    ori_data = {}
    city_id2name = get_city_id2name()
    cities = get_city_info()
    for city, info in cities.items():
        ori_data[city] = {'attr': [0, 0], 'attr2': [0, 0], 'latitude': info['latitude'], 'longitude': info['longitude']}
    if attr != 'latitude' and attr != 'longitude':
        sql = f"select city_id, value from {attr} where" \
              f" to_char(time_point,'YYYY-MM-DD hh24:mi:ss') between :st and :et"
        args = {'st': time_start.strftime('%Y-%m-%d %H:%M:%S'),
                'et': time_end.strftime('%Y-%m-%d %H:%M:%S')}
        db_cursor.execute(sql, args)
        sql_data = db_cursor.fetchall()
        for line in sql_data:
            city_name = city_id2name[line[0]]
            value = line[1]
            if attr=='weather_description':
                value = w_desc.get(line[1], 0)
            if city_name in ori_data:
                ori_data[city_name]['attr'][0] += value
                ori_data[city_name]['attr'][1] += 1
    if attr2 != 'latitude' and attr2 != 'longitude':
        sql = f"select city_id, value from {attr2} where" \
              f" to_char(time_point,'YYYY-MM-DD hh24:mi:ss') between :st and :et"
        args = {'st': time_start.strftime('%Y-%m-%d %H:%M:%S'),
                'et': time_end.strftime('%Y-%m-%d %H:%M:%S')}
        db_cursor.execute(sql, args)
        sql_data = db_cursor.fetchall()
        for line in sql_data:
            city_name = city_id2name[line[0]]
            value = line[1]
            if attr == 'weather_description':
                value = w_desc.get(line[1], 0)
            if city_name in ori_data:
                ori_data[city_name]['attr2'][0] += value
                ori_data[city_name]['attr2'][1] += 1
    temp = []
    for key, value in ori_data.items():
        value['attr'] = value['attr'][0] / value['attr'][1] if value['attr'][1] != 0 else 0
        value['attr2'] = value['attr2'][0] / value['attr2'][1] if value['attr2'][1] != 0 else 0
        if attr == 'latitude' or attr == 'longitude':
            value['attr'] = value[attr]
        if attr2 == 'latitude' or attr2 == 'longitude':
            value['attr2'] = value[attr2]
        temp.append([value['attr'], value['attr2'], key])
    temp.sort(key=lambda x: x[0])
    data = {'x': [], 'y': [], 'name': []}
    for item in temp:
        data['x'].append(item[0])
        data['y'].append(item[1])
        data['name'].append(item[2])
    return jsonify(success=True, content=data)


@app.route("/get_data_count", methods=["POST"])
def get_data_count():
    global attrs
    total_count = 0
    for attr in attrs:
        sql = f"select count(count(1)) from {attr} group by time_point"
        db_cursor.execute(sql)
        total_count += db_cursor.fetchone()[0]
    logging.info(f'total_count={total_count}')
    return jsonify(success=True, content=total_count)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=15001, debug=True)

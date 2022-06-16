import json

import requests
import time
import datetime
import sqlite3 as sl
conn = sl.connect('Stabis.db', check_same_thread=False)
cursor = conn.cursor()

def db_table_select_Auto():
    cursor.execute("SELECT id, capacity FROM cars")
    row = cursor.fetchone()
    out = []
    while row is not None:
        out.append(f"""\n{{
            "id": {row[0]},
            "capacity":{{"weight_kg": {row[1]} }}
        }},
    """)
        row = cursor.fetchone()
    out.pop()
    return ''.join(out)
def db_table_select_Last_Auto():
    cursor.execute("SELECT id, capacity FROM cars")
    row = cursor.fetchone()
    out = []
    while row is not None:
        out.append(f"""\n{{
            "id": {row[0]},
            "capacity":{{"weight_kg": {row[1]} }}
        }}
    """)
        row = cursor.fetchone()
    return ''.join(out[-1])
def db_table_select_Location():
    cursor.execute("SELECT id, latitude, longitude, capacity FROM objects")
    row = cursor.fetchone()
    out = []
    while row is not None:
        out.append(f"""\n{{
          "id": {row[0]},
          "point":
          {{
              "lat": {row[1]},
              "lon": {row[2]}
        }},
        "time_window": "07:00-18:00",
        "shipment_size": {{ "weight_kg": {row[3]}}}
      }},
  """)
        row = cursor.fetchone()
    out.pop()
    return ''.join(out)
def db_table_select_Last_Location():
    cursor.execute("SELECT id, latitude, longitude, capacity FROM objects")
    row = cursor.fetchone()
    out = []
    while row is not None:
        out.append(f"""\n{{
            "id": {row[0]},
            "point":
            {{
              "lat": {row[1]},
              "lon": {row[2]}
            }},
        "time_window": "07:00-18:00",
        "shipment_size": {{ "weight_kg": {row[3]}}}
    }}
    """)
        row = cursor.fetchone()
    return ''.join(out[-1])
print(db_table_select_Last_Location())



token = None
with open("token2.txt") as f:
    token = f.read().strip()

API_KEY = f'{token}'
print(API_KEY)
API_ROOT_ENDPOINT = 'https://courier.yandex.ru/vrs/api/v1'


payload = (f'''{{
  "depot": {{
      "id": 0,
      "point": {{
          "lat": 57.156705,
          "lon": 65.447281
      }},
      "time_window": "07:00-18:00"
  }},
  "vehicles": [ {db_table_select_Auto()}
  {db_table_select_Last_Auto()}
  ],
  "options": {{
      "time_zone": 3,
      "quality": "normal",
      "routing_mode": "truck"
    }},
  "locations": [ {db_table_select_Location()}
  {db_table_select_Last_Location()}
  ]
  }}
''')

Html_file = open('playload.json', 'w')
Html_file.write(payload)
Html_file.close()
with open('playload.json', 'r') as data_file:
    data = json.load(data_file)


# Отправьте запрос и получите ID поставленной задачи.
response = requests.post(
    API_ROOT_ENDPOINT + '/add/mvrp',
    params={'apikey': API_KEY}, json=data)

poll_stop_codes = {
    requests.codes.ok,
    requests.codes.gone,
    requests.codes.internal_server_error
}

# Опрос сервера о готовности результата оптимизации маршрута с использованием полученного ранее ID.
if response.status_code == requests.codes.accepted:
    request_id = response.json()['id']
    poll_url = '{}/result/mvrp/{}'.format(API_ROOT_ENDPOINT, request_id)

    response = requests.get(poll_url)
    while response.status_code not in poll_stop_codes:
        time.sleep(1)
        response = requests.get(poll_url)

    # Вывод информации в пользовательском формате.
    if response.status_code != 200:
        print ('Error {}: {}'.format(response.text, response.status_code))
    else:
        print ('Route optimization completed')
        print ('')

        for route in response.json()['result']['routes']:
            print ('Vehicle {} route: {:.2f}km'.format(
                route['vehicle_id'], route['metrics']['total_transit_distance_m'] / 1000))

            # Вывод маршрута в текстовом формате.
            for waypoint in route['route']:
                print ('  {type} {id} at {eta}, {distance:.2f}km driving '.format(
                    type=waypoint['node']['type'],
                    id=waypoint['node']['value']['id'],
                    eta=str(datetime.timedelta(seconds=waypoint['arrival_time_s'])),
                    distance=waypoint['transit_distance_m'] / 1000))

            # Вывод маршрута в формате ссылки на Яндекс Карты.
            yamaps_url = 'https://yandex.ru/maps/?mode=routes&rtext='
            for waypoint in route['route']:
                point = waypoint['node']['value']['point']
                yamaps_url += '{}%2c{}~'.format(point['lat'], point['lon'])
                f = open('itog.txt', 'w')
                f.write(yamaps_url)

            print ('')
            print ('See route on Yandex.Maps:')
            print (yamaps_url)
            print ('https://yandex.ru/courier/mvrp-map/#/c7242fab-73bc3b4d-9ece9179-8f815b62?route=0')
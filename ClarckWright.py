import requests
import time
import datetime
import sqlite3 as sl

conn = sl.connect('Stabis.db', check_same_thread=False)
cursor = conn.cursor()

def db_table_selectAll():
    cursor.execute("SELECT id, latitude, longitude FROM objects")
    row = cursor.fetchone()
    out = []
    while row is not None:
        out.append("""\n<tr><td align="center">%s</td>""" % row[0])
        out.append("""\n<td align="center">%s</td>""" % row[1])
        out.append("""\n<td align="center">%s</td>""" % row[2])
        row = cursor.fetchone()
    return ''.join(out)

print(db_table_selectAll())

token = None
with open("token2.txt") as f:
    token = f.read().strip()

API_KEY = f'{token}'
print(API_KEY)
API_ROOT_ENDPOINT = 'https://courier.yandex.ru/vrs/api/v1'


payload = {
  "depot": {
      "id": 0,
      "point": {
          "lat": 57.156705,
          "lon": 65.447281
      },
      "time_window": "07:00-18:00"
  },
  "vehicles": [{
          "id": 1
      }
  ],
  "locations": [{
          "id": 1,
          "point": {
              "lat": 55.708272,
              "lon": 37.46826
          },
          "time_window": "07:00-18:00"
      }
  ],
  "locations": [{
          "id": 1,
          "point": {
              "lat": 57.157429,
              "lon": 65.451158
          },
          "time_window": "07:00-18:00"
      }
  ],
  "options": {
      "time_zone": 3,
      "quality": "normal"
  }
}


# Отправьте запрос и получите ID поставленной задачи.
response = requests.post(
    API_ROOT_ENDPOINT + '/add/mvrp',
    params={'apikey': API_KEY}, json=payload)

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

            print ('')
            print ('See route on Yandex.Maps:')
            print (yamaps_url)
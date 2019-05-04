from flask import render_template
from app import app
from app import influx
from app import sensors
from flask import Markup
from flask import request
from markdown import markdown

import dateutil.parser


@app.route('/login', methods=["GET", "POST"])
def login():

    return render_template('login.html')


@app.route('/add')
def add():
    return render_template('add_md.html')


@app.route('/add_2', methods=['POST'])
def post_add():
    title = request.form['title']
    date = request.form['date']
    body = request.form['body']

    with open("app/static/blog_entries/{}_{}.md".format(date, title), "w+") as file:
        file.write(body)
        file.close()

    return render_template('index.html')


@app.route('/')
def index():
    with open("app/static/Nudelsalat.md", mode="r", encoding="utf-8") as file:
        content = Markup(markdown(file.read()))
    return render_template('index.html', **locals())


@app.route('/sensors')
def table():
    temp_result = []
    hum_result = []

    for sensor in sensors:

        if sensor['temp']:
            measurement = sensor['name']
            query_result = influx.query(
                """SELECT temperature FROM temperature WHERE "name" = '{}' ORDER by time DESC LIMIT 1""".format(
                    measurement))
            raw = query_result.get_points()
            for res in raw:
                time = dateutil.parser.parse(res['time'])
                temp_result.append(
                    {
                        "temperature": round(res['temperature'], 2),
                        "time": "{}:{}.{}".format(time.hour + 1, time.minute, time.second),
                        "name": sensor['nickname']
                    }
                )

        if sensor['hum']:
            query_result_2 = influx.query(
                """SELECT humidity FROM humidity WHERE "name" = '{}' ORDER by time DESC LIMIT 1""".format(measurement))
            raw2 = query_result_2.get_points()
            for res2 in raw2:
                time = dateutil.parser.parse(res2['time'])
                hum_result.append(
                    {
                        "humidity": round(res2['humidity'], 2),
                        "time": "{}:{}.{}".format(time.hour + 1, time.minute, time.second),
                        "name": sensor['nickname']
                    }
                )

    return render_template('sensors.html', **locals())


def parse(query_result):

    parse_result = []

    for res in query_result.get_points():
        time = dateutil.parser.parse(res['time'])
        if res['mean'] is not None:
            parse_result.append(
                {
                    "data": round(res['mean'], 2),
                    "time": "{}:{}".format(time.hour + 1, time.minute),
                }
            )

    return parse_result


def query(field, measurement, tag, divisor):

    query_result = influx.query("""SELECT mean("{}") / {} FROM "{}" WHERE ("name" = '{}') AND (time > now() - 1d) 
        GROUP BY time(10m)fill(0)""".format(field, divisor, measurement, tag))

    return parse(query_result)


@app.route('/graphs')
def graphs():
    front_outer = query("temperature", "temperature", "front_window_outside", 1)
    back_outer = query("temperature", "temperature", "back_window_outside", 1)
    front_board = query("temperature", "temperature", "front_window_inside", 1)
    back_board = query("temperature", "temperature", "back_window_inside", 1)
    desk = query("temperature", "temperature", "desk", 1)
    front_radiator = query("temperature", "temperature", "front_radiator", 1)
    back_radiator = query("temperature", "temperature", "back_radiator", 1)
    back_board_hum = query("humidity", "humidity", "window_front", 1)
    front_board_hum = query("humidity", "humidity", "window_back", 1)
    desk_hum = query("humidity", "humidity", "desk", 1)
    power_computer = query("milliwatt", "power", "Computer", 1000)
    power_server = query("milliwatt", "power", "Server", 1000)
    power_small = query("milliwatt", "power", "Kleinteile", 1000)

    return render_template('graphs.html', **locals())

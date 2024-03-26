from time import sleep
from flask import Flask, json
from flask_cors import CORS
from threading import Thread
from flask_socketio import SocketIO
from config.connection.db import get_db
from core.sensor.domain.sensor import Sensor
from core.report.domain.report import Report
from functools import reduce
from random import random
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app, debug=True, cors_allowed_origins="*", async_mode="threading")
CORS(app)

db = get_db()

sensors = []
last_data = {}
data_influencers = [True]

def populate_data():
    global sensors
    global last_data
    if not sensors:
        res = db.query(Sensor).all()
        sensors = list(map(lambda sensor: sensor.__dict__, res))
    if not last_data:
        res = db.query(Report).all()
        if not res:
            last_data = {
                1: 36,
                2: 120,
                3: 120,
            }
        else:
            last_data = reduce(lambda acc, report: {**acc, report.sensor_id: float(report.data)}, res, last_data)
    
def get_offset(act, median):
    up_chance = 0.5
    half_max = median + median / 2
    half_min = median - median / 2
    if act > half_max:
        up_chance = 0.1
    elif act < half_min:
        up_chance = 0.7
    return up_chance
    
def gen_data():
    global sensors
    global last_data
    populate_data()
    return_data = []
    for sensor in sensors:
        rep = last_data.get(sensor["id"])
        median = (sensor["max"] + sensor["min"]) / 2
        offset = get_offset(rep, median)
        ind = random()
        data = float(sensor["offset"]) * random() 
        if ind < offset:
            data_to_insert = rep + data
        else:
            data_to_insert = rep - data
        last_data[sensor["id"]] = data_to_insert
        time = datetime.now()
        sensor_data = Report(data=data_to_insert, date=time, sensor_id=sensor["id"])
        # db.add(sensor_data)
        return_data.append({
            "id": sensor_data.id,
            "name": sensor["name"],
            "data": sensor_data.data,
            "date": sensor_data.date,
            "sensor_id": sensor_data.sensor_id
        })
    return return_data
        
class Gen(Thread):
    def __init__(self):
        Thread.__init__(self)
        
    def run(self):
        while True:
            # função de gerar dados e salvar aqui
            res = gen_data()
            socketio.emit("data", json.dumps(res)) #retorno da funcao, o retorno pode ser os dados gerados: {"temperatura": 32, "humildade": 5}
            sleep(1)

gen = Gen()
gen.start()

@socketio.on("alert")
def get_alert(alert):
    data_influencers.append(alert)

if __name__ == '__main__':
    app.run()


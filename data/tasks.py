from __future__ import absolute_import

from celery import shared_task
from .models import WindData

import redis
import random
import datetime
import time

@shared_task
def generate_data():
    data_store = redis.StrictRedis(host='localhost', port=6379, db=5)
    random.seed(datetime.now())

    rand_wind_speed = random(0.0, 200.0)
    rand_wind_dir = randint(0, 359)
    time.sleep(2.5)

    data_store.set('wind_speed', str(rand_wind_speed))
    data_store.set('wind_dir', str(rand_wind_dir))

@shared_task
def get_current_data():
    data_store = redis.StrictRedis(host='localhost', port=6379, db=5)

    speed = float(data_store.get('wind_speed'))
    direction = int(data_store.get('wind_dir'))

    data = (speed, direction)
    print data

    return data

@shared_task
def start_update_data_loop():
    data_store = redis.StrictRedis(host='localhost', port=6379, db=5)
    speed = float(data_store.get('wind_speed'))
    direction = int(data_store.get('wind_dir'))

    while(True):
        new_data = WindData.objects.create(wind_direction=direction, wind_speed=speed)
        new_data.save()
        time.sleep(2.5)

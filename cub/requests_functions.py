from django.shortcuts import render

# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse
import datetime
import psycopg as pg
#from django.template.loader import get_template
from django.shortcuts import render
from django.shortcuts import redirect
from django.template import Context
import json
# import time
# import random
import math
import numpy as np
from numpy import linalg as LA
from typing import Any, Sequence
from psycopg import Cursor

from cub.forms import EdgeForm
from cub.models import Edge
from cub.models import Controler
from cub.models import Position
from cub.models import Dots
from cub.models import Vision
from django.core import serializers
from threading import Thread
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from cub.my_classes import Food, Food_db
import polygons
from queue import Queue
from cub import physical_simulation

class DictRowFactory:
    def __init__(self, cursor: Cursor[Any]):
        self.fields = [c.name for c in cursor.description]

    def __call__(self, values: Sequence[Any]) -> dict[str, Any]:
        return dict(zip(self.fields, values))

def hello(request):
    form = EdgeForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("cub")
    else:
        return render(request, "cub/cub.html", {"form": form})

def start(request):
    obj_state, created = Controler.objects.get_or_create(
        name = "state",
        description = "with controller state you can start or stop bacterial",
    )
    if obj_state.value == 0:
        obj_state.value = 1
        obj_state.save()
    data = serializers.serialize('json', [ obj_state, ])
    t = Thread(target=process_bac, args=(15, ))
    t.daemon = True
    t.start()
    return HttpResponse(data)

def stop(request):
    obj_state, created = Controler.objects.get_or_create(
        name = "state",
        description = "with controller state you can start or stop bacterial",
    )
    if obj_state.value != 0:
        obj_state.value = 0
        obj_state.save()
    data = serializers.serialize('json', [ obj_state, ])
    return HttpResponse(data)

def process_bac(inter):
    bacterial_process = physical_simulation.BacterialProcess(inter)
    channel_layer = get_channel_layer()
    while bacterial_process.st == 1 or bacterial_process.st == 3:
        bacterial_process.action_signal(physical_simulation.ActionsCodes.REVERS)
        ddd = bacterial_process.process_data()
        async_to_sync(channel_layer.group_send)(
            'chat_lobby',
            {
                'type': 'chat.message',
                'message': ddd
            }
        )

def json_1(request):
    data = json_2
    return HttpResponse(data)

def json_2():
    # time.sleep(0.5)
    all_json = {}
    obj_position, created = Position.objects.get_or_create(
        name = "position",
        description = "This is position bacterium",
    )
    obj_dots, created = Dots.objects.get_or_create()
    data_json = serializers.serialize('json', [ obj_dots, ])
    data = json.loads(data_json)

    if Vision.objects.exists():
        obj_vision = Vision.objects.last()
    else:
        obj_vision, created = Vision.objects.get_or_create()
    
    list = []
    for key, value in obj_vision.__dict__.items():
        list.append(value)
    list.pop(0)
    list.pop(0)

    all_json['x'] = obj_position.x
    all_json['y'] = obj_position.y
    all_json['r'] = obj_position.r
    all_json['plot'] = list
    all_json['dots_x1'] = obj_dots.x1
    all_json['dots_x2'] = obj_dots.x2
    all_json['dots_x3'] = obj_dots.x3
    all_json['dots_x4'] = obj_dots.x4
    all_json['dots_y1'] = obj_dots.y1
    all_json['dots_y2'] = obj_dots.y2
    all_json['dots_y3'] = obj_dots.y3
    all_json['dots_y4'] = obj_dots.y4
    all_json['dots_r'] = obj_dots.r

    #data = serializers.serialize('json', [ obj_position, ])
    data = json.dumps(all_json)
    return data

def get_div_foods(request):
    result = Food_db.objects.values('top', 'left', 'div_id', 'height', 'width')
    data_all = []
    for value in result:
        data_all.append(value)
    data = json.dumps(data_all)
    return HttpResponse(data)

def add_food(request):
    data_json = request.POST['food']
    data = json.loads(data_json)
    res = {'is_new': False}
    food_obj = Food(data['y'], data['x'], data['div_id'], data['h'], data['w'])
    if food_obj.is_new:
        res['is_new'] = True
    res_json = json.dumps(res)
    obj_state, created = Controler.objects.get_or_create(
        name = "state",
        description = "with controller state you can start or stop bacterial",
    )
    if obj_state.value == 0:
        obj_state.value = 2
        obj_state.save()
    if obj_state.value == 1:
        obj_state.value = 3
        obj_state.save()
    return HttpResponse(res_json)

def del_food(request):
    f_db = Food_db.objects.last()
    data_obj = {}
    if f_db is not None:
        f = Food(f_db.top, f_db.left, f_db.div_id, f_db.height, f_db.width)
        data_obj = f.get_div()
        data_obj['isNull'] = False
        f.delete()
    else:
        data_obj['isNull'] = True
    data = json.dumps(data_obj)
    obj_state, created = Controler.objects.get_or_create(
        name = "state",
        description = "with controller state you can start or stop bacterial",
    )
    if obj_state.value == 0:
        obj_state.value = 2
        obj_state.save()
    if obj_state.value == 1:
        obj_state.value = 3
        obj_state.save()
    return HttpResponse(data)
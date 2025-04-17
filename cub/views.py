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
import time
import random
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
    t = Thread(target=insert, args=(15, ))
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

def insert(inter):
    data = {'a': inter}
    x = 400
    y = 400
    r = 0
    stxy = Edge.objects.filter(pref_parent_id="").values_list("x1", "y1", "x2", "y2")
    foods = Food_db.objects.values()
    polygon_foods = []
    points_food = []
    for food in foods:
        food_p = [(food['left'], food['top']), 
                (food['left']+food['width'], food['top']), 
                (food['left']+food['width'], food['top']+food['height']), 
                (food['left'], food['top']+food['height'])]
        polygon_foods.append(food_p)
        for point_polyg in food_p:
            points_food.append(point_polyg)
    dx = 0
    dy = 0
    dr = 0
    st = 1
    rand = 0
    pos = Position.objects.get()
    dots = Dots.objects.get()
    channel_layer = get_channel_layer()
    while st == 1 or st == 3:
        #time.sleep(0.030)
        cntr = Controler.objects.get()
        pos.x = round(x)
        pos.y = round(y)
        pos.r = round(r)
        pos.save()
        st = cntr.value
        if st == 3:
            cntr.value = 1
            cntr.save()
            foods = Food_db.objects.values()
            polygon_foods = []
            points_food = []
            for food in foods:
                food_p = [(food['left'], food['top']), 
                        (food['left']+food['width'], food['top']), 
                        (food['left']+food['width'], food['top']+food['height']), 
                        (food['left'], food['top']+food['height'])]
                polygon_foods.append(food_p)
                for point_polyg in food_p:
                    points_food.append(point_polyg)
        # st = data[0][1]
        if rand == 0:
            # dr = random.randint(-20, 20)
            dr = random.randint(-20, 20)
            dx = 0
            dy = 0
            rand = 1
        elif rand == 1:
            dr = 0
            dx = 10 * math.cos(math.radians(r))
            dy = 10 * math.sin(math.radians(r))
            rand = 0
        randdd = random.randint(1, 4)
        if randdd == 4:
            dr = 0
            dx = -math.cos(math.radians(r))
            dy = -math.sin(math.radians(r))
        x1 = x
        x2 = x + dx
        y1 = y
        y2 = y + dy
        r1 = r
        r2 = r + dr
        acrs = 0
        dr1 = [[-15, -10], [15, -10], [15, 10], [-15, 10]]
        axy1 = [[-15, -10], [15, -10], [15, 10], [-15, 10]]
        axy2 = [[-15, -10], [15, -10], [15, 10], [-15, 10]]
        for l in range(0, 4):
            axy1[l] = [dr1[l][0] * math.cos(math.radians(r1)) - dr1[l][1] * math.sin(math.radians(r1)) + 10 + x1,
                       dr1[l][0] * math.sin(math.radians(r1)) + dr1[l][1] * math.cos(math.radians(r1)) + 15 + y1]
            axy2[l] = [dr1[l][0] * math.cos(math.radians(r2)) - dr1[l][1] * math.sin(math.radians(r2)) + 10 + x2,
                       dr1[l][0] * math.sin(math.radians(r2)) + dr1[l][1] * math.cos(math.radians(r2)) + 15 + y2]
        for j in range(0, len(stxy)):
            for jj in range(0, len(axy1)):
                acrs = acrs + across(stxy[j][0], -stxy[j][1], stxy[j][2], -stxy[j][3], axy1[jj][0], -axy1[jj][1], axy2[jj][0], -axy2[jj][1])
        
        points= [(axy2[0][0], axy2[0][1]), (axy2[1][0], axy2[1][1]), (axy2[2][0], axy2[2][1]), (axy2[3][0], axy2[3][1])]
        
        num_edges_children  =  4
        num_nodes_children  =  4
        is_inside_sum = False
        tree = polygons.build_search_tree(polygon_foods, num_edges_children, num_nodes_children)
        if len(tree) > 0 and len(points) > 0:
            is_insides = polygons.points_are_inside(tree, points)
            polygon_bacterium = [[(axy2[0][0], axy2[0][1]), (axy2[1][0], axy2[1][1]), (axy2[2][0], axy2[2][1]), (axy2[3][0], axy2[3][1])]]
            tree = polygons.build_search_tree(polygon_bacterium, num_edges_children, num_nodes_children)
            is_insides_bac = polygons.points_are_inside(tree, points_food)
            is_insides = is_insides + is_insides_bac
            is_inside_sum = False
            for is_inside in is_insides:
                is_inside_sum = is_inside_sum or is_inside
                if is_inside_sum: 
                    break
        
        if acrs >= 1 or is_inside_sum:
            dx = 0
            dy = 0
            dr = 0

        dots.x1 = axy1[0][0]
        dots.y1 = axy1[0][1]
        dots.x2 = axy1[1][0]
        dots.y2 = axy1[1][1]
        dots.x3 = axy1[2][0]
        dots.y3 = axy1[2][1]
        dots.x4 = axy1[3][0]
        dots.y4 = axy1[3][1]
        dots.save()
        x = x + dx
        y = y + dy
        r = r + dr
        list_plot = eyes_s(x, y, r)
        
        all_json = {}
        all_json['x'] = x
        all_json['y'] = y
        all_json['r'] = r
        all_json['plot'] = list_plot
        all_json['dots_x1'] = axy1[0][0]
        all_json['dots_x2'] = axy1[1][0]
        all_json['dots_x3'] = axy1[2][0]
        all_json['dots_x4'] = axy1[3][0]
        all_json['dots_y1'] = axy1[0][1]
        all_json['dots_y2'] = axy1[1][1]
        all_json['dots_y3'] = axy1[2][1]
        all_json['dots_y4'] = axy1[3][1]
        all_json['dots_r'] = r

        #data = serializers.serialize('json', [ obj_position, ])
        ddd = json.dumps(all_json)
        
        
        #ddd = json_2()
        async_to_sync(channel_layer.group_send)(
            'chat_lobby',
            {
                'type': 'chat.message',
                'message': ddd
            }
        )
        
    return HttpResponse(data)

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

def distance(x1, y1, x2, y2, x3, y3):
    x1 = float(x1)
    y1 = float(y1)
    x2 = float(x2)
    y2 = float(y2)
    x3 = float(x3)
    y3 = float(y3)
    if x1 == x2:
        x1 = x1 + 0.0000000000000000000001
    if y1 == y2:
        y1 = y1 + 0.0000000000000000000001
    dx = x1 - x2
    dy = y1 - y2
    a = math.degrees(math.atan(dy / (dx + 0.0000000000000000000001)))
    k1 = math.tan(math.radians(a))
    k2 = math.tan(math.radians(a + 90))
    y0 = y1 - k1 * x1
    y01 = y3 - k2 * x3
    x = (y01 - y0) / (k1 - k2)
    y = k1 * x + y0
    s = math.sqrt((x - x3) * (x - x3) + (y - y3) * (y - y3))
    xx1 = 0
    xx2 = 0
    yy1 = 0
    yy2 = 0
    if x2 > x1:
        xx1 = x1
        xx2 = x2
    elif x1 > x2:
        xx1 = x2
        xx2 = x1
    if y2 > y1:
        yy1 = y1
        yy2 = y2
    elif y1 > y2:
        yy1 = y2
        yy2 = y1
    if (x >= xx2 or x <= xx1) and (y >= yy2 or y <= yy1):
        f = 0
        arr = [math.sqrt((x1 - x3) * (x1 - x3) + (y1 - y3) * (y1 - y3)),
               math.sqrt((x2 - x3) * (x2 - x3) + (y2 - y3) * (y2 - y3))]
        s = min(arr)
    else:
        f = 1
    s = [round(x, 13), round(y, 13), round(s, 13), f]
    return s

def across(x1, y1, x2, y2, x3, y3, x4, y4):
    ar1 = distance(x1, y1, x2, y2, x3, y3)
    ar2 = distance(x1, y1, x2, y2, x4, y4)
    dx1 = round(ar1[0] - x3, 12)
    dy1 = round(ar1[1] - y3, 12)
    dx2 = round(ar2[0] - x4, 12)
    dy2 = round(ar2[1] - y4, 12)
    if dx1 * dx2 < 0 or dy1 * dy2 < 0:
        s = 1
    else:
        s = 0
    return s

def eyes_s(x,y,r):
    # stxy = Edge.objects.filter(pref_parent_id="").values_list("x1", "y1", "x2", "y2")
    xxx = False
    stxy = Edge.objects.values_list("x1", "y1", "x2", "y2")
    n = 59
    s3 = 100
    r_l = 60
    s1 = 20
    ggg = 0
    s2 = s3 + s1
    ds1 = []
    ds2 = []
    sss = []
    scsc = []
    data_dict = {}
    for i in range(0, n+1):
        ds1.append(rotors(x + 10, y + 15, x + 25, y + 5 + s1 * i / n, r))
        ds2.append(rotors(x + 10, y + 15, x + 25 + s3, y + 5 - s3 / 2 + s2 * i / n, r))
    for i in range(0, n+1):
        rrr = []
        for j in range(0,len(stxy)):
            x1EyeLine = ds1[i][0]
            y1EyeLine = ds1[i][1]
            x2EyeLine = ds2[i][0]
            y2EyeLine = ds2[i][1]
            xy = distance_e(x1EyeLine,y1EyeLine,x2EyeLine,y2EyeLine,stxy[j][0],stxy[j][1],stxy[j][2],stxy[j][3]) # x,y точки пересечения линии датчика зрения и линии стены
            # xCrossWall = round(xy[0], 15)
            # yCrossWall = round(xy[1], 15)
            xCrossWall = xy[0]
            yCrossWall = xy[1]
            x1Wall = min(stxy[j][0],stxy[j][2])
            x2Wall = max(stxy[j][0],stxy[j][2])
            y1Wall = min(stxy[j][1],stxy[j][3])
            y2Wall = max(stxy[j][1],stxy[j][3])
            s = xy[2]
            dd = 0.0000001
            # if (xCrossWall - x1EyeLine > 0 and x2EyeLine - x1EyeLine > 0 or \
            #    xCrossWall - x1EyeLine < 0 and x2EyeLine - x1EyeLine < 0 or \
            #    yCrossWall - y1EyeLine > 0 and y2EyeLine - y1EyeLine > 0 or \
            #    yCrossWall - y1EyeLine < 0 and y2EyeLine - y1EyeLine < 0) and \
            #    x1Wall <= xCrossWall and xCrossWall <= x2Wall and \
            #    y1Wall <= yCrossWall and yCrossWall <= y2Wall:
            #     rrr.append(math.sqrt((xCrossWall - x1EyeLine) ** 2 + (yCrossWall - y1EyeLine) ** 2))
            # if xxx:
            #     www = 'i: ' +  str(i) + ', j: ' + str(j) + ', xy: ' +  str(xy)
            #     print(www)
            if x1Wall <= xCrossWall + dd and xCrossWall - dd <= x2Wall and \
               y1Wall <= yCrossWall + dd and yCrossWall - dd <= y2Wall and s > 0:
                rrr.append(s)

        if len(rrr) > 0:
            sss.append(min(rrr))
        else:
            sss.append(0)
            
        pref = 's'
        if i < 10:
            pref = 's0'
        
        if sss[i]==0:
            # print(www)
            sss[i]=0
            xxx = True
        else:
            xxx = False
            
        
        data_dict[pref + str(i)] = sss[i]
        scsc.append(sss[i])
        scsc.append(0)
    Vision.objects.create(**data_dict)
    return scsc
# поворот точки x, y вокруг x0, y0 по радиусу r
def rotors(x0, y0, x, y, r):
    dx = x - x0
    dy = y - y0
    xy = [dx * math.cos(math.radians(r)) - dy * math.sin(math.radians(r)) + x0,
          dx * math.sin(math.radians(r)) + dy * math.cos(math.radians(r)) + y0]
    return xy
# x1, y1, x2, y2 - это линия датчика зрения, x3, y3, x4, y4 - линия стены
def distance_e(x1, y1, x2, y2, x3, y3, x4, y4):
    x1 = float(x1) + 0.00000000000000001
    y1 = float(y1) + 0.00000000000000001
    x2 = float(x2) + 0.00000000000000002
    y2 = float(y2) + 0.00000000000000002
    x3 = float(x3) + 0.00000000000000001
    y3 = float(y3) + 0.00000000000000001
    x4 = float(x4) + 0.00000000000000002
    y4 = float(y4) + 0.00000000000000002
    k1 = (y2 - y1) / (x2 - x1 + 0.00000000000000001) # наклон линии датчика зрения
    k2 = (y4 - y3) / (x4 - x3 + 0.00000000000000001) # наклон линии стены
    y01 = y1 - k1 * x1 # постоянное смещение линии датчика зрения по оси y
    y02 = y3 - k2 * x3 # постоянное смещение линии стены по оси y
    x = (y01 - y02) / (k2 - k1 + 0.00000000000000001) # x точки пересечения линии датчика зрения и линии стены
    y = k1 * x + y01                                  # y точки пересечения линии датчика зрения и линии стены

    A = [x1, y1]
    B = [x2, y2]
    C = [x3, y3]
    D = [x4, y4]
    O = [x, y]
    AB = [A[0]-B[0], A[1]-B[1]] # A - B
    AO = [A[0]-O[0], A[1]-O[1]] # A - O
    nAB = math.sqrt(AB[0]**2 + AB[1]**2) # LA.norm(AB)
    dotAB_AO = AB[0]*AO[0] + AB[1]*AO[1] # np.dot(AB, AO)
    s = dotAB_AO/nAB
    xys = [x, y, s]
    return xys # расстояние от A до пересечения

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
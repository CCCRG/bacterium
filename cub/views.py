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
    if obj_state.value != 1:
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
    stxy = Edge.objects.values_list("x1", "y1", "x2", "y2")
    dx = 0
    dy = 0
    dr = 0
    st = 1
    rand = 0
    pos = Position.objects.get()
    dots = Dots.objects.get()
    while st == 1:
        time.sleep(0.070)
        cntr = Controler.objects.get()
        pos.x = round(x)
        pos.y = round(y)
        pos.r = round(r)
        pos.save()
        st = cntr.value
        # st = data[0][1]
        if rand == 0:
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
                acrs = acrs + across(stxy[j][0], -stxy[j][1], stxy[j][2], -stxy[j][3], axy1[jj][0], -axy1[jj][1],
                                     axy2[jj][0], -axy2[jj][1])
        if acrs >= 1:
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
        eyes_s(x, y, r)
        
    return HttpResponse(data)

def json_1(request):
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
    return HttpResponse(data)

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
    stxy = Edge.objects.values_list("x1", "y1", "x2", "y2")
    script1 = 'insert into eyes('
    script2 = 'values ('
    n = 59
    s3 = 100
    r_l = 60
    s1 = 20
    ggg = 0
    s2 = s3 + s1
    ds1 = []
    ds2 = []
    sss = []
    data_dict = {}
    for i in range(0, n+1):
        ds1.append(rotors(x + 10, y + 15, x + 25, y + 5 + s1 * i / n, r))
        ds2.append(rotors(x + 10, y + 15, x + 25 + s3, y + 5 - s3 / 2 + s2 * i / n, r))
    for i in range(0, n+1):
        rrr = []
        for j in range(0,len(stxy)):
            xy = distance_e(ds1[i][0],ds1[i][1],ds2[i][0],ds2[i][1],stxy[j][0],stxy[j][1],stxy[j][2],stxy[j][3])
            if xy[0] - ds1[i][0] > 0 and ds2[i][0] - ds1[i][0] > 0 or xy[0] - ds1[i][0] < 0 and ds2[i][0] - ds1[i][0] < 0 or xy[1] - ds1[i][1] > 0 and ds2[i][1] - ds1[i][1] > 0 or xy[1] - ds1[i][1] < 0 and ds2[i][1] - ds1[i][1] < 0:
                rrr.append(math.sqrt((xy[0] - ds1[i][0]) * (xy[0] - ds1[i][0]) + (xy[1] - ds1[i][1]) * (xy[1] - ds1[i][1])))

        if len(rrr) > 0:
            sss.append(min(rrr))
        else:
            sss.append(0)
            
        pref = 's'
        if i < 10:
            pref = 's0'
            
        data_dict[pref + str(i)] = sss[i]
        script1 = script1 + 's' + str(i+1) + ',' + 'c' + str(i+1) + ','
        script2 = script2 + str(sss[i]) + ','
        script2 = script2 + str(0) + ','
    script1 = script1[0:len(script1) - 1] + ') '
    script2 = script2[0:len(script2) - 1] + ')'
    script = script1 + script2 + ';'
    Vision.objects.create(**data_dict)
    return script

def rotors(x0, y0, x, y, r):
    dx = x - x0
    dy = y - y0
    xy = [dx * math.cos(math.radians(r)) - dy * math.sin(math.radians(r)) + x0,
          dx * math.sin(math.radians(r)) + dy * math.cos(math.radians(r)) + y0]
    return xy

def distance_e(x1, y1, x2, y2, x3, y3, x4, y4):
    x1 = float(x1) + 0.00000000000000001
    y1 = float(y1) + 0.00000000000000001
    x2 = float(x2) + 0.00000000000000002
    y2 = float(y2) + 0.00000000000000002
    x3 = float(x3) + 0.00000000000000001
    y3 = float(y3) + 0.00000000000000001
    x4 = float(x4) + 0.00000000000000002
    y4 = float(y4) + 0.00000000000000002
    k1 = (y2 - y1) / (x2 - x1 + 0.00000000000000001)
    k2 = (y4 - y3) / (x4 - x3 + 0.00000000000000001)
    y01 = y1 - k1 * x1
    y02 = y3 - k2 * x3
    x = (y01 - y02) / (k2 - k1 + 0.00000000000000001)
    y = k1 * x + y01
    r = math.degrees(math.atan(k1))
    xy = [x,y]
    return xy

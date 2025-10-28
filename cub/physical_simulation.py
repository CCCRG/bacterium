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
from queue import Queue

from threading import Thread
from queue import Queue
import time
from enum import Enum, IntEnum

class ActionsCodes(IntEnum):
    """Справочник действий-кодов"""
    RANDOM = 0
    TURNL = 1
    TURNR = 2
    FORVARD = 3
    REVERS = 4

# ОБЩАЯ очередь для всего приложения
# bacterial_queue = Queue()

class BacterialProcess:
    def __init__(self, inter):
        self.data = {'a': inter}
        self.x = 400
        self.y = 400
        self.r = 0
        self.stxy = Edge.objects.filter(pref_parent_id="").values_list("x1", "y1", "x2", "y2")
        self.foods = Food_db.objects.values()
        self.polygon_foods = []
        self.points_food = []
        for food in self.foods:
            food_p = [(food['left'], food['top']), 
                    (food['left']+food['width'], food['top']), 
                    (food['left']+food['width'], food['top']+food['height']), 
                    (food['left'], food['top']+food['height'])]
            self.polygon_foods.append(food_p)
            for point_polyg in food_p:
                self.points_food.append(point_polyg)
        self.dx = 0
        self.dy = 0
        self.dr = 0
        self.st = 1
        self.pos = Position.objects.get()
        self.dots = Dots.objects.get()
        self.rand = 0

    
    # def start(self):
    #     if not self.running:
    #         self.running = True
    #         self.thread = Thread(target=self._process_commands, daemon=True)
    #         self.thread.start()
    
    # def _process_commands(self):
    #     while self.running:
    #         try:
    #             # Получаем команды из ОБЩЕЙ очереди
    #             command, data = self.queue.get(timeout=1.0)
                
    #             if command == "UPDATE_PARAM":
    #                 print(f"Worker получил новое значение: {data}")
    #                 # Обрабатываем данные
    #                 self._process_data(data)
                
    #             elif command == "STOP":
    #                 break
                    
    #             self.queue.task_done()
                
    #         except:
    #             # Таймаут - продолжаем цикл
    #             continue
    
    def process_data(self):
        cntr = Controler.objects.get()
        self.pos.x = round(self.x)
        self.pos.y = round(self.y)
        self.pos.r = round(self.r)
        self.pos.save()
        self.st = cntr.value
        if self.st == 3:
            cntr.value = 1
            cntr.save()
            self.foods = Food_db.objects.values()
            self.polygon_foods = []
            self.points_food = []
            for food in self.foods:
                food_p = [(food['left'], food['top']), 
                        (food['left']+food['width'], food['top']), 
                        (food['left']+food['width'], food['top']+food['height']), 
                        (food['left'], food['top']+food['height'])]
                self.polygon_foods.append(food_p)
                for point_polyg in food_p:
                    self.points_food.append(point_polyg)
        # st = data[0][1]
            
        x1 = self.x
        x2 = self.x + self.dx
        y1 = self.y
        y2 = self.y + self.dy
        r1 = self.r
        r2 = self.r + self.dr
        acrs = 0
        dr1 = [[-15, -10], [15, -10], [15, 10], [-15, 10]]
        axy1 = [[-15, -10], [15, -10], [15, 10], [-15, 10]]
        axy2 = [[-15, -10], [15, -10], [15, 10], [-15, 10]]
        for l in range(0, 4):
            axy1[l] = [dr1[l][0] * math.cos(math.radians(r1)) - dr1[l][1] * math.sin(math.radians(r1)) + 10 + x1,
                       dr1[l][0] * math.sin(math.radians(r1)) + dr1[l][1] * math.cos(math.radians(r1)) + 15 + y1]
            axy2[l] = [dr1[l][0] * math.cos(math.radians(r2)) - dr1[l][1] * math.sin(math.radians(r2)) + 10 + x2,
                       dr1[l][0] * math.sin(math.radians(r2)) + dr1[l][1] * math.cos(math.radians(r2)) + 15 + y2]
        for j in range(0, len(self.stxy)):
            for jj in range(0, len(axy1)):
                acrs = acrs + self._across(self.stxy[j][0], -self.stxy[j][1], self.stxy[j][2], -self.stxy[j][3], axy1[jj][0], -axy1[jj][1], axy2[jj][0], -axy2[jj][1])
        
        points= [(axy2[0][0], axy2[0][1]), (axy2[1][0], axy2[1][1]), (axy2[2][0], axy2[2][1]), (axy2[3][0], axy2[3][1])]
        
        num_edges_children  =  4
        num_nodes_children  =  4
        is_inside_sum = False
        tree = polygons.build_search_tree(self.polygon_foods, num_edges_children, num_nodes_children)
        if len(tree) > 0 and len(points) > 0:
            is_insides = polygons.points_are_inside(tree, points)
            polygon_bacterium = [[(axy2[0][0], axy2[0][1]), (axy2[1][0], axy2[1][1]), (axy2[2][0], axy2[2][1]), (axy2[3][0], axy2[3][1])]]
            tree = polygons.build_search_tree(polygon_bacterium, num_edges_children, num_nodes_children)
            is_insides_bac = polygons.points_are_inside(tree, self.points_food)
            is_insides = is_insides + is_insides_bac
            is_inside_sum = False
            for is_inside in is_insides:
                is_inside_sum = is_inside_sum or is_inside
                if is_inside_sum: 
                    break
        
        if acrs >= 1 or is_inside_sum:
            self.dx = 0
            self.dy = 0
            self.dr = 0

        self.dots.x1 = axy1[0][0]
        self.dots.y1 = axy1[0][1]
        self.dots.x2 = axy1[1][0]
        self.dots.y2 = axy1[1][1]
        self.dots.x3 = axy1[2][0]
        self.dots.y3 = axy1[2][1]
        self.dots.x4 = axy1[3][0]
        self.dots.y4 = axy1[3][1]
        self.dots.save()
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.r = self.r + self.dr
        list_plot = self._eyes_s(self.x, self.y, self.r)
        
        all_json = {}
        all_json['x'] = self.x
        all_json['y'] = self.y
        all_json['r'] = self.r
        all_json['plot'] = list_plot
        all_json['dots_x1'] = axy1[0][0]
        all_json['dots_x2'] = axy1[1][0]
        all_json['dots_x3'] = axy1[2][0]
        all_json['dots_x4'] = axy1[3][0]
        all_json['dots_y1'] = axy1[0][1]
        all_json['dots_y2'] = axy1[1][1]
        all_json['dots_y3'] = axy1[2][1]
        all_json['dots_y4'] = axy1[3][1]
        all_json['dots_r'] = self.r

        #data = serializers.serialize('json', [ obj_position, ])
        ddd = json.dumps(all_json)
        return ddd
    
    def action_signal(self, act: ActionsCodes):
        ## под замену
        if act == ActionsCodes.RANDOM:
            if self.rand == 0:
                # dr = random.randint(-20, 20)
                self.dr = random.randint(-20, 20)
                self.dx = 0
                self.dy = 0
                self.rand = 1
            elif self.rand == 1:
                self.dr = 0
                self.dx = 10 * math.cos(math.radians(self.r))
                self.dy = 10 * math.sin(math.radians(self.r))
                self.rand = 0
            randdd = random.randint(1, 4)
            if randdd == 4:
                self.dr = 0
                self.dx = -math.cos(math.radians(self.r))
                self.dy = -math.sin(math.radians(self.r))
        elif act == ActionsCodes.TURNL:
                self.dr = -20
                self.dx = 0
                self.dy = 0
        elif act == ActionsCodes.TURNR:
                self.dr = 20
                self.dx = 0
                self.dy = 0
        elif act == ActionsCodes.FORVARD:
                self.dr = 0
                self.dx = 10 * math.cos(math.radians(self.r))
                self.dy = 10 * math.sin(math.radians(self.r))
        elif act == ActionsCodes.REVERS:
                self.dr = 0
                self.dx = -math.cos(math.radians(self.r))
                self.dy = -math.sin(math.radians(self.r))

    def _across(self, x1, y1, x2, y2, x3, y3, x4, y4):
        ar1 = self._distance(x1, y1, x2, y2, x3, y3)
        ar2 = self._distance(x1, y1, x2, y2, x4, y4)
        dx1 = round(ar1[0] - x3, 12)
        dy1 = round(ar1[1] - y3, 12)
        dx2 = round(ar2[0] - x4, 12)
        dy2 = round(ar2[1] - y4, 12)
        if dx1 * dx2 < 0 or dy1 * dy2 < 0:
            s = 1
        else:
            s = 0
        return s

    def _eyes_s(self, x,y,r):
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
            ds1.append(self._rotors(x + 10, y + 15, x + 25, y + 5 + s1 * i / n, r))
            ds2.append(self._rotors(x + 10, y + 15, x + 25 + s3, y + 5 - s3 / 2 + s2 * i / n, r))
        for i in range(0, n+1):
            rrr = []
            for j in range(0,len(stxy)):
                x1EyeLine = ds1[i][0]
                y1EyeLine = ds1[i][1]
                x2EyeLine = ds2[i][0]
                y2EyeLine = ds2[i][1]
                xy = self._distance_e(x1EyeLine,y1EyeLine,x2EyeLine,y2EyeLine,stxy[j][0],stxy[j][1],stxy[j][2],stxy[j][3]) # x,y точки пересечения линии датчика зрения и линии стены
                xCrossWall = xy[0]
                yCrossWall = xy[1]
                x1Wall = min(stxy[j][0],stxy[j][2])
                x2Wall = max(stxy[j][0],stxy[j][2])
                y1Wall = min(stxy[j][1],stxy[j][3])
                y2Wall = max(stxy[j][1],stxy[j][3])
                s = xy[2]
                dd = 0.0000001
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
    def _rotors(self, x0, y0, x, y, r):
        dx = x - x0
        dy = y - y0
        xy = [dx * math.cos(math.radians(r)) - dy * math.sin(math.radians(r)) + x0,
            dx * math.sin(math.radians(r)) + dy * math.cos(math.radians(r)) + y0]
        return xy
    
    def _distance(self, x1, y1, x2, y2, x3, y3):
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
    
    # x1, y1, x2, y2 - это линия датчика зрения, x3, y3, x4, y4 - линия стены
    def _distance_e(self, x1, y1, x2, y2, x3, y3, x4, y4):
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
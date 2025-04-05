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

class DictRowFactory:
    def __init__(self, cursor: Cursor[Any]):
        self.fields = [c.name for c in cursor.description]

    def __call__(self, values: Sequence[Any]) -> dict[str, Any]:
        return dict(zip(self.fields, values))

def hello(request):
    return render(request, "cub/cub.html")

def plot(request):
    #conn = pymysql.connect(host='localhost', user='root', passwd='fdlZm6vC', db='db_cub')
    conn = pg.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
    cur = conn.cursor()
    cur.execute("select s1,c1,s2,c2,s3,c3,s4,c4,s5,c5,s6,c6,s7,c7,s8,c8,s9,c9,s10,c10,s11,c11,s12,c12,s13,c13,s14,c14,s15,c15,s16,c16,s17,c17,s18,c18,s19,c19,s20,c20,s21,c21,s22,c22,s23,c23,s24,c24,s25,c25,s26,c26,s27,c27,s28,c28,s29,c29,s30,c30,s31,c31,s32,c32,s33,c33,s34,c34,s35,c35,s36,c36,s37,c37,s38,c38,s39,c39,s40,c40,s41,c41,s42,c42,s43,c43,s44,c44,s45,c45,s46,c46,s47,c47,s48,c48,s49,c49,s50,c50,s51,c51,s52,c52,s53,c53,s54,c54,s55,c55,s56,c56,s57,c57,s58,c58,s59,c59,s60,c60 from eyes where num = (SELECT MAX(num) FROM eyes)")
    conn.commit()
    data = cur.fetchall()
    cur.close()
    conn.close()
    return HttpResponse(json.dumps(data))

def start(request):
    #conn = pymysql.connect(host='localhost', user='root', passwd='fdlZm6vC', db='db_cub')
    conn = pg.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
    cur = conn.cursor()
    cur.execute("update control set value = 1 where num = 1")
    conn.commit()
    cur.execute("select * from control where num = 1")
    data = cur.fetchall()
    cur.close()
    conn.close()
    st = data[0][2]
    return HttpResponse(json.dumps(data))

def stop(request):
    #conn = pymysql.connect(host='localhost', user='root', passwd='fdlZm6vC', db='db_cub')
    conn = pg.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
    cur = conn.cursor()
    cur.execute("update control set value = 0 where num = 1")
    conn.commit()
    cur.execute("select x1, y1, x2, y2 from stena")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return HttpResponse(json.dumps(data[0]))


def points(request):
    #conn = pymysql.connect(host='localhost', user='root', passwd='fdlZm6vC', db='db_cub')
    conn = pg.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
    # cur = conn.cursor(pymysql.cursors.DictCursor)
    cur = conn.cursor(row_factory=DictRowFactory)
    cur.execute("SELECT * FROM test where num = (SELECT MAX(num) FROM test)")
    data = cur.fetchall()
    cur.close()
    #conn.close()

    cur = conn.cursor()
    cur.execute("select s1,c1,s2,c2,s3,c3,s4,c4,s5,c5,s6,c6,s7,c7,s8,c8,s9,c9,s10,c10,s11,c11,s12,c12,s13,c13,s14,c14,s15,c15,s16,c16,s17,c17,s18,c18,s19,c19,s20,c20,s21,c21,s22,c22,s23,c23,s24,c24,s25,c25,s26,c26,s27,c27,s28,c28,s29,c29,s30,c30,s31,c31,s32,c32,s33,c33,s34,c34,s35,c35,s36,c36,s37,c37,s38,c38,s39,c39,s40,c40,s41,c41,s42,c42,s43,c43,s44,c44,s45,c45,s46,c46,s47,c47,s48,c48,s49,c49,s50,c50,s51,c51,s52,c52,s53,c53,s54,c54,s55,c55,s56,c56,s57,c57,s58,c58,s59,c59,s60,c60 from eyes where num = (SELECT MAX(num) FROM eyes)")
    conn.commit()
    data2 = cur.fetchall()
    cur.close()
    conn.close()
    data[0]['plot'] = data2

    return HttpResponse(json.dumps(data))


def insert(request):
    x = 400
    y = 400
    r = 0
    #conn = pymysql.connect(host='localhost', user='root', passwd='fdlZm6vC', db='db_cub')
    conn = pg.connect(dbname="postgres", user="postgres", password="postgres", host="localhost",keepalives=1,
                        keepalives_idle=130,
                        keepalives_interval=20,
                        keepalives_count=30)
    cur = conn.cursor()
    cur.execute("select x1, y1, x2, y2 from stena")
    stxy = cur.fetchall()
    cur.close()
    conn.close()
    dx = 0
    dy = 0
    dr = 0
    st = 1
    rand = 0
    while st == 1:
        conn = pg.connect(dbname="postgres", user="postgres", password="postgres", host="localhost", keepalives=1,
                          keepalives_idle=130,
                          keepalives_interval=20,
                          keepalives_count=30)
        cur = conn.cursor()
        cur.execute("update numbers set xxx = %s where num = 299", [round(x)])
        conn.commit()
        cur.execute("update numbers_y set yyy = %s where num = 244", [round(y)])
        conn.commit()
        cur.execute("update rotors set rrr = %s where num = 1", [r])
        conn.commit()
        cur.execute("select * from control where num = 1")
        data = cur.fetchall()
        cur.close()
        conn.close()
        st = data[0][1]
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

        conn = pg.connect(dbname="postgres", user="postgres", password="postgres", host="localhost", keepalives=1,
                          keepalives_idle=130,
                          keepalives_interval=20,
                          keepalives_count=30)
        cur = conn.cursor()
        #cur.execute("update test set x1 = %e ,y1 = %e ,x2 = %e ,y2 = %e ,x3 = %e ,y3 = %e ,x4 = %e ,y4 = %e ,acrs = %e where num = 1" % ([axy1[0][0]], [axy1[0][1]], [axy1[1][0]], [axy1[1][1]], [axy1[2][0]], [axy1[2][1]], [axy1[3][0]], [axy1[3][1]], [r]))
        cur.execute(
            "update test set x1 = %e ,y1 = %e ,x2 = %e ,y2 = %e ,x3 = %e ,y3 = %e ,x4 = %e ,y4 = %e ,acrs = %e where num = 1" % (
                axy1[0][0], axy1[0][1], axy1[1][0], axy1[1][1], axy1[2][0], axy1[2][1], axy1[3][0], axy1[3][1], r))
        conn.commit()
        cur.close()
        conn.close()
        x = x + dx
        y = y + dy
        r = r + dr
        eyes_s(x, y, r)
    conn = pg.connect(dbname="postgres", user="postgres", password="postgres", host="localhost", keepalives=1,
                      keepalives_idle=130,
                      keepalives_interval=20,
                      keepalives_count=30)
    cur = conn.cursor()
    cur.execute("SELECT * FROM eyes1 where num = (SELECT MAX(num) FROM eyes1)")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return HttpResponse(json.dumps(data))


def json_1(request):
    #conn = pymysql.connect(host='localhost', user='root', passwd='fdlZm6vC', db='db_cub')
    conn = pg.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
    #cur = conn.cursor(pymysql.cursors.RealDictRow)DictCursor
    cur = conn.cursor(row_factory=DictRowFactory)
    cur.execute("select * from numbers where num = 299")
    data = cur.fetchall()
    #print(json.dumps(cur.fetchall(), indent=2))
    #data = cur.fetchone()
    #res = data['xxx']
    conn.commit()
    cur.close()
    conn.close()
    res = json.dumps(data)
    return HttpResponse(json.dumps(data))


def json_y(request):
    #conn = pymysql.connect(host='localhost', user='root', passwd='fdlZm6vC', db='db_cub')
    conn = pg.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
    #cur = conn.cursor()
    cur = conn.cursor(row_factory=DictRowFactory)
    cur.execute("select * from numbers_y where num = 244")
    data = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return HttpResponse(json.dumps(data))


def json_r(request):
    #conn = pymysql.connect(host='localhost', user='root', passwd='fdlZm6vC', db='db_cub')
    conn = pg.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
    #cur = conn.cursor()
    cur = conn.cursor(row_factory=DictRowFactory)
    cur.execute("select * from rotors where num = 1")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return HttpResponse(json.dumps(data))


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
    #conn = pymysql.connect(host='localhost', user='root', passwd='fdlZm6vC', db='db_cub')
    conn = pg.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
    cur = conn.cursor()
    cur.execute("select x1, y1, x2, y2 from stena")
    stxy = cur.fetchall()
    cur.execute("SELECT * FROM test where num = (SELECT MAX(num) FROM test)")
    bxy = cur.fetchall()
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
        script1 = script1 + 's' + str(i+1) + ',' + 'c' + str(i+1) + ','
        script2 = script2 + str(sss[i]) + ','
        script2 = script2 + str(0) + ','
    script1 = script1[0:len(script1) - 1] + ') '
    script2 = script2[0:len(script2) - 1] + ')'
    script = script1 + script2 + ';'
    print('script')
    cur.execute(script)
    conn.commit()
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

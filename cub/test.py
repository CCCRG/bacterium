
import psycopg as pg
import json
import numpy as np
from numpy import linalg as LA
import math
import numpy as np
import polygons

polygon_points  =  [ 
    [( 0.0 ,  0.0 ),  ( 1.0 , 0.0 ), ( 1.0 ,  1.0 ),  ( 0.0 , 1.0  ) ] , 
    [( 0.0 , 2.0 ) , ( 1.0 , 2.0 ), ( 1.0 , 3.0 ), ( 0.0 , 3.0 ) ] , ]

points= [( 0.5 ,  0.5 ),  ( 0.5 ,  - 0.5 )]

num_edges_children  =  5
num_nodes_children  =  5
tree = polygons.build_search_tree(polygon_points, num_edges_children, num_nodes_children)
inside = polygons.points_are_inside(tree, points)
print(inside)  # [True, False]

# x1 = 500
# y1 = 700
# x2 = 500 #3
# y2 = 600 #0.5
# x3 = 0
# y3 = 0
# x4 = 1020
# y4 = 0


# x1 = float(x1) + 0.00000000000000001
# y1 = float(y1) + 0.00000000000000001
# x2 = float(x2) + 0.00000000000000002
# y2 = float(y2) + 0.00000000000000002
# x3 = float(x3) + 0.00000000000000001
# y3 = float(y3) + 0.00000000000000001
# x4 = float(x4) + 0.00000000000000002
# y4 = float(y4) + 0.00000000000000002
# k1 = (y2 - y1) / (x2 - x1 + 0.00000000000000001) # наклон линии датчика зрения
# k2 = (y4 - y3) / (x4 - x3 + 0.00000000000000001) # наклон линии стены
# y01 = y1 - k1 * x1 # постоянное смещение линии датчика зрения по оси y
# y02 = y3 - k2 * x3 # постоянное смещение линии стены по оси y
# x = (y01 - y02) / (k2 - k1 + 0.00000000000000001) # x точки пересечения линии датчика зрения и линии стены
# y = k1 * x + y01                                  # y точки пересечения линии датчика зрения и линии стены

# A = [x1, y1]
# B = [x2, y2]
# C = [x3, y3]
# D = [x4, y4]
# O = [x, y]
# AB = [A[0]-B[0], A[1]-B[1]] # A - B
# AO = [A[0]-O[0], A[1]-O[1]] # A - O
# nAB = math.sqrt(AB[0]**2 + AB[1]**2) # LA.norm(AB)
# nAO = math.sqrt(AO[0]**2 + AO[1]**2) # LA.norm(AO)
# dotAB_AO = AB[0]*AO[0] + AB[1]*AO[1] # np.dot(AB, AO)
# res = dotAB_AO/nAB
# print(res)
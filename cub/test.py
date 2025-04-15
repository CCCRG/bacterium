
import psycopg as pg
import json
import numpy as np
from numpy import linalg as LA
import math
import numpy as np

x1 = 500
y1 = 700
x2 = 500 #3
y2 = 600 #0.5
x3 = 0
y3 = 0
x4 = 1020
y4 = 0


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

A = np.array([[x1, y1]])
B = np.array([[x2, y2]])
C = np.array([[x3, y3]])
D = np.array([[x4, y4]])
O = np.array([[x, y]])
AB = A - B
AO = A - O
nAB = LA.norm(AB)
nAO = LA.norm(AO)
AO = np.transpose(AO)
dotAB_AO = np.dot(AB, AO)
dotAB_AO = dotAB_AO[0][0]
res = dotAB_AO/nAB
print(res)
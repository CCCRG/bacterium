import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import random

# усовершенствованный метот Хебба по поиску корреляций с забыванием
# параметры
eta = 0.1          # скорость обучения
steps = 2000000     # количество шагов
w = 0            # начальный вес связи
p1 = 0.00046
p2 = 0.04
p3 = p1/p2

prevA1 = 0
prevA2 = 0
prevA3 = 0
prevB = 0
prevB1 = 0
A1 = 0
A2 = 0
A3 = 0
B = 0
B1 = 0
weights1, weights2, weights3, a_A1, a_A2, a_B, a_A12 = [], [], [], [], [], [], []
# случайная активность нейронов (0 или 1)
for t in range(steps):
    A1 = 1 if random.random() < p2 else 0
    A2 = 1 if random.random() < 0.5 else 0
    A3 = 1 if random.random() < p3 else 0
    A4 = A1*A3
    B = A2*A4
    B1 = A2
    #A1 = A4
    if t > 0:
        dA1 = (A1-prevA1)
        dA2 = (A2-prevA2)
        dA3 = (A3-prevA3)
        dB = (B-prevB)
        dB1 = (B1-prevB1)
    else:
        prevA1 = A1
        prevA2 = A2
        prevA3 = A3
        prevB = B
        prevB1 = B1
    dA1 = (A1-prevA1)
    dA2 = (A2-prevA2)
    dA3 = (A3-prevA3)
    dB = (B-prevB)
    dB1 = (B1-prevB1)
    a_A1.append(dA1)  # входной нейрон
    a_A2.append(dA2)  # входной нейрон
    a_A12.append(dB1)
    a_B.append(dB)  # входной нейрон
    prevA1 = A1
    prevA2 = A2
    prevA3 = A3
    prevB = B
    prevB1 = B1
    
    
a_count = deque(maxlen=10000)
count_p = 0
count_m = 0
count_01 = 0
for t in range(steps):
    # Усиление при совпадении = 1, ослабление при несовпадении = -1
    if a_B[t] != 0 and a_B[t] != 0:
        if (a_A1[t] == a_B[t]):
            a_count.append(1)
        elif a_A1[t] == -a_B[t]:
            a_count.append(-1)
        elif a_A1[t] == 0:
            a_count.append(0)
        count_p = sum(1 for x in a_count if x == 1)
        count_m = sum(1 for x in a_count if x == -1)
        count_01 = sum(1 for x in a_count if x == 0)
        if len(a_count) == 0:
            s =5
        w = (count_p - count_m)/len(a_count)
        weights3.append(w)
print("процент совпадений: ", count_p)
print("процент не совпадений: ", count_m)

a_count = deque(maxlen=10000)
count_p = 0
count_m = 0
count_02 = 0
for t in range(steps):
    # Усиление при совпадении = 1, ослабление при несовпадении = -1
    if a_B[t] != 0 and a_A2[t] != 0:
        if (a_A2[t] == a_B[t]):
            a_count.append(1)
        elif a_A2[t] == -a_B[t]:
            a_count.append(-1)
        elif a_A2[t] == 0:
            a_count.append(0)
        count_p = sum(1 for x in a_count if x == 1)
        count_m = sum(1 for x in a_count if x == -1)
        count_02 = sum(1 for x in a_count if x == 0)
        if len(a_count) == 0:
            s =5
        w = (count_p - count_m)/len(a_count)
        weights1.append(w)
print("процент count_01: ", count_01)
print("процент count_02: ", count_02)


# визуализация
plt.figure(figsize=(7,4))
plt.plot(weights3, label='Сила связи w_A1B')
plt.plot(weights1, label='Сила связи a_A2B')
plt.title('Рост связи при совместной активности (правило Хебба)')
plt.xlabel('Время (шаги)')
plt.ylabel('Вес w_AB')
plt.legend()
plt.show()

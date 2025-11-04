import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# усовершенствованный метот Хебба по поиску корреляций с забыванием
# параметры
eta = 0.1          # скорость обучения
steps = 1000     # количество шагов
w = 0            # начальный вес связи

weights1, weights2, weights3, a_A1, a_A2, a_B, a_A12= [], [], [], [], [], [], []
# случайная активность нейронов (0 или 1)
for t in range(steps):
    A1 = np.random.randint(0,2)
    A2 = np.random.randint(0,2)
    A3 = np.random.randint(0,2)
    B = A1*A2*A3
    B1 = A1*A2
    a_A1.append(A1)  # входной нейрон
    a_A2.append(A2)  # входной нейрон
    a_A12.append(B1)
    a_B.append(B)  # входной нейрон
    # ran = np.random.randint(0,2)
    # if ran == 0:
    #     #a_B1.append(np.random.randint(0,2))
    #     a_A1.append(1)
    # else:
    #     a_A1.append(1)

a_count = deque(maxlen=1000)

count_p = 0
count_m = 0
for t in range(steps):
    # Усиление при совпадении = 1, ослабление при несовпадении = -1
    if (a_A1[t] == a_B[t]):
        a_count.append(1)
    else:
        a_count.append(-1)
    count_p = sum(1 for x in a_count if x == 1)
    count_m = len(a_count) - count_p
    w = (count_p - count_m)/len(a_count)
    weights1.append(w)

a_count = deque(maxlen=1000)
count_p = 0
count_m = 0
for t in range(steps):
    # Усиление при совпадении = 1, ослабление при несовпадении = -1
    if (a_A2[t] == a_B[t]):
        a_count.append(1)
    else:
        a_count.append(-1)
    count_p = sum(1 for x in a_count if x == 1)
    count_m = len(a_count) - count_p
    w = (count_p - count_m)/len(a_count)
    weights2.append(w)
    
    
a_count = deque(maxlen=1000)
count_p = 0
count_m = 0
for t in range(steps):
    # Усиление при совпадении = 1, ослабление при несовпадении = -1
    if (a_A12[t] == a_B[t]):
        a_count.append(1)
    else:
        a_count.append(-1)
    count_p = sum(1 for x in a_count if x == 1)
    count_m = len(a_count) - count_p
    w = (count_p - count_m)/len(a_count)
    weights3.append(w)
print("процент совпадений: ", count_p)
print("процент не совпадений: ", count_m)

# визуализация
plt.figure(figsize=(7,4))
plt.plot(weights1, label='Сила связи w_A1B')
plt.plot(weights2, label='Сила связи w_A2B')
plt.plot(weights3, label='Сила связи w_A12B')
plt.title('Рост связи при совместной активности (правило Хебба)')
plt.xlabel('Время (шаги)')
plt.ylabel('Вес w_AB')
plt.legend()
plt.show()

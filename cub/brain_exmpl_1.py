import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# усовершенствованный метот Хебба по поиску корреляций с забыванием
# параметры
eta = 0.1          # скорость обучения
steps = 5000     # количество шагов
w = 0            # начальный вес связи

weights, a_A1, a_B1 = [], [], []
# случайная активность нейронов (0 или 1)
for t in range(int(steps/2)):
    A = np.random.randint(0,2)
    a_A1.append(A)  # входной нейрон
    ran = np.random.randint(0,2)
    if ran == 0:
        a_B1.append(np.random.randint(0,2))
    else:
        a_B1.append(A)


a_A2, a_B2 = [], []
# случайная активность нейронов (0 или 1)
for t in range(int(steps/2)):
    A = np.random.randint(0,2)
    a_A2.append(A)  # входной нейрон
    ran = np.random.randint(0,2)
    if ran == 0:
        a_B2.append(np.random.randint(0,2))
    else:
        a_B2.append(1-A)

a_A, a_B = [], []
a_A = a_A1 + a_A2
a_B = a_B1 + a_B2
a_count = deque(maxlen=1000)

count_p = 0
count_m = 0
for t in range(steps):
    # Усиление при совпадении = 1, ослабление при несовпадении = -1
    if (a_A[t] == a_B[t]):
        a_count.append(1)
    else:
        a_count.append(-1)
    count_p = sum(1 for x in a_count if x == 1)
    count_m = len(a_count) - count_p
    w = (count_p - count_m)/len(a_count)
    weights.append(w)
# for t in range(steps):
#     dw = eta * a_A[t] * a_B[t]   # правило Хебба
#     w += dw
#     weights.append(w)
print("процент совпадений: ", count_p)
print("процент не совпадений: ", count_m)

# визуализация
plt.figure(figsize=(7,4))
plt.plot(weights, label='Сила связи w_AB')
plt.title('Рост связи при совместной активности (правило Хебба)')
plt.xlabel('Время (шаги)')
plt.ylabel('Вес w_AB')
plt.legend()
plt.show()

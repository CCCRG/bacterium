import numpy as np
#from typing import TypeVar, Generic
from typing import List, Union, Any, Dict, Optional
#Matrix = TypeVar('Neuron', bound=Neuron)
from collections import deque
import matplotlib.pyplot as plt
import random
import pickle
import os
         
# -------------------------------
# 2. Класс мозга
# -------------------------------
class BrainFast:
    def __init__(self, n_neurons=10, history_len=1000):
        # основные размеры
        self.n_neurons = n_neurons
        self.history_len = history_len

        # состояния (аналог detector, dofam, control)
        self.detectors = np.zeros(n_neurons, dtype=np.int8)
        self.dofams = np.zeros(n_neurons, dtype=np.int8)
        self.controls = np.zeros(n_neurons, dtype=np.int8)

        # корреляции
        self.corr_x = np.zeros(n_neurons)
        self.corr_c = np.zeros(n_neurons)
        self.corr_d = np.zeros(n_neurons)

        # история сигналов
        self.x_hist = np.zeros((n_neurons, history_len), dtype=np.int8)
        self.y_hist = np.zeros((n_neurons, history_len), dtype=np.int8)
        self.hist_ptr = np.zeros(n_neurons, dtype=np.int32)

    # --- корреляция между X и Y ---
    def calc_iter(self):
        n = self.n_neurons
        x = self.detectors
        y = self.dofams

        # сохранить значения в историю
        idx = self.hist_ptr % self.history_len
        self.x_hist[np.arange(n), idx] = x
        self.y_hist[np.arange(n), idx] = y
        self.hist_ptr += 1

        # считаем статистику
        count_p = np.sum(self.x_hist * self.y_hist == 1, axis=1)
        count_n = np.sum(((1 - self.x_hist) * self.y_hist) == 1, axis=1)
        count_x = np.sum(self.x_hist == 1, axis=1)
        L = np.minimum(self.hist_ptr, self.history_len)

        avg_x = np.divide(count_x, L, out=np.zeros_like(count_x, dtype=float), where=L!=0)
        valid = (avg_x > 0) & (avg_x < 1)

        p = np.zeros(n)
        n_ = np.zeros(n)
        p[valid] = count_p[valid] / L[valid]
        n_[valid] = count_n[valid] / L[valid]

        norm_p = np.zeros(n)
        norm_n = np.zeros(n)
        norm_p[valid] = p[valid] / avg_x[valid]
        norm_n[valid] = n_[valid] / (1 - avg_x[valid])

        denom = norm_p + norm_n
        with np.errstate(divide='ignore', invalid='ignore'):
            corr = np.where(denom != 0, (norm_p - norm_n) / denom, 0)
            corr = np.nan_to_num(corr, nan=0.0, posinf=0.0, neginf=0.0)
        self.corr_x = corr
        self.corr_c = corr.copy()
        self.corr_d = corr.copy()

    # --- вычисление активности (контроль) ---
    def calc_control(self, p1=0.00046, p2=0.04):
        n = self.n_neurons
        p3 = p1 / p2

        # генерируем случайные бинарные состояния
        rand = np.random.rand(n, 4)
        A1 = (rand[:, 0] < p2).astype(np.int8)
        A2 = (rand[:, 1] < 0.5).astype(np.int8)
        A3 = (rand[:, 2] < p3).astype(np.int8)
        A4 = (rand[:, 3] < 0.5).astype(np.int8)
        B = A1 * A2 * A3

        # обновляем состояния
        self.detectors[:] = A1
        self.controls[:] = np.where(self.corr_c < 10, A2, A1)
        self.dofams[:] = np.where(np.random.rand(n) < 0.5, B, A4)

    # --- один шаг ---
    def step(self):
        self.calc_control()
        self.calc_iter()



if __name__ == "__main__":
    br = BrainFast(n_neurons=1)

    steps = 500000
    weights = np.zeros((steps, br.n_neurons))

    for t in range(steps):
        br.step()
        weights[t] = br.corr_x



# p1 = 0.00046
# p2 = 0.04
# p3 = p1/p2
# steps = 500000
# restart = True # True если хочешь стирать состояние мозга при перезапуске
# is_new: bool = False
# if os.path.exists('/home/vboxuser/bacterium/cub/b1/data.pkl'):
#     if restart:
#         os.remove('/home/vboxuser/bacterium/cub/b1/data.pkl')
#         is_new = True
#     else:
#         with open('/home/vboxuser/bacterium/cub/b1/data.pkl', 'rb') as f:
#             br = pickle.load(f)
# else:
#     is_new = True
# if is_new:
#     br = Brain()
    
# a_Dofam, a_Detect, a_Control = [], [], []
# weightsX, weightsC, weightsD = [], [], []

# for t in range(steps):
#     br.calc_iter()
#     weightsX.append(br.neurons[0].pins_x[0].correlation.value)
#     weightsC.append(br.neurons[0].pins_c[0].correlation.value)
#     weightsD.append(br.neurons[0].pins_d[0].correlation.value)
    
# sss = 1
# with open('/home/vboxuser/bacterium/cub/b1/data.pkl', 'wb') as f:
#     pickle.dump(br, f)

# # визуализация
# print('длина истории с d=1: ',len(br.neurons[0].pins_x[0].correlation.history))
# print('длина истории с x: ',len(br.neurons[0].pins_x[0].correlation.history_x))
# print('norm_p с x: ',br.neurons[0].pins_x[0].correlation.norm_p)
# print('norm_n с x: ',br.neurons[0].pins_x[0].correlation.norm_n)
# print('value с x: ',br.neurons[0].pins_x[0].correlation.value)
# print('norm_p с c: ',br.neurons[0].pins_c[0].correlation.norm_p)
# print('norm_n с c: ',br.neurons[0].pins_c[0].correlation.norm_n)
# print('value с c: ',br.neurons[0].pins_c[0].correlation.value)
# print('norm_p с d: ',br.neurons[0].pins_d[0].correlation.norm_p)
# print('norm_n с d: ',br.neurons[0].pins_d[0].correlation.norm_n)
# print('value с d: ',br.neurons[0].pins_d[0].correlation.value)
plt.figure(figsize=(7,4))
plt.plot(weights, label='Сила связи pinX')
# plt.plot(weightsC, label='Сила связи pinC')
# plt.plot(weightsD, label='Сила связи pinD')
plt.title('Рост связи при совместной активности (правило Хебба)')
plt.xlabel('Время (шаги)')
plt.ylabel('Вес w_AB')
plt.legend()
plt.show()



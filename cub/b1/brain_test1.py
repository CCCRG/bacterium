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
# 2. Класс детектора
# -------------------------------
class Detector:
    def __init__(self, id: int, type: str):
        self.id = id
        self.type = type
        self.curr_val = 0
        
# -------------------------------
# 2. Класс пина в нейроне
# -------------------------------
class DPin:
    def __init__(self, id: int, detectors: List[Detector], dofams: List[Detector], controls: List[Detector]):
        self.id = id
        self.type = 'Dofam'
        self.detector: Detector
        self.cursor = 0
        self.detectors = detectors
        self.dofams = dofams
        self.controls = controls
        self.correlation: Correlation = Correlation(self,self)
        self.prev_val = 0
        
    def search_link(self):
        self.detector = self.dofams[self.cursor]
        # if (self.correlation.value < abs(0.2) and 
        #     len(self.correlation.history) > 100):
        #     self.cursor += 1
        #     self.detector = self.dofams[self.cursor]
        #     self.correlation = Correlation(self, self)
        
class Pin:
    def __init__(self, id: int, type: str, detectors: List[Detector], dofams: List[Detector], controls: List[Detector], y_pin: DPin):
        self.id = id
        self.type = type
        self.detector: Detector
        self.cursor = 0
        self.detectors = detectors
        self.dofams = dofams
        self.controls = controls
        self.y_pin: DPin = y_pin
        self.correlation: Correlation = Correlation(self, y_pin)
        self.prev_val = 0
        
    def search_link(self):
        if self.type == 'Detector':
            self.detector = self.detectors[self.cursor]
        elif self.type == 'Control':
            self.detector = self.controls[self.cursor]
            
        # if (self.correlation.value < abs(0.2) and 
        # len(self.correlation.history) > 100 or
        # len(self.correlation.history) == 0 and self.correlation.value == 0):
        #     self.cursor += 1
        #     if self.type == 'Detector':
        #         self.detector = self.detectors[self.cursor]
        #         self.correlation = Correlation(self, self.y_pin)
        #     elif self.type == 'Control':
        #         self.detector = self.controls[self.cursor]
        #         self.correlation = Correlation(self, self.y_pin)
            
        
        
# -------------------------------
# 2. Класс корреляции
# -------------------------------
class Correlation:
    def __init__(self, x: Pin, y: DPin):
        self.x = x
        self.y = y
        self.maxl = 10000
        self.maxl_x = 10000
        self.history = deque(maxlen=self.maxl)
        self.history_x = deque(maxlen=self.maxl_x)
        self.value = 0
        self.is_first_iter = True
        self.norm_p = 0
        self.norm_n = 0
        self.count_p = 0
        self.count_n = 0
        self.count_x = 0        
        
    def _append_x(self, x_val):
        """Добавляет x в историю и корректирует счётчик count_x"""
        if len(self.history_x) == self.maxl_x:
            old = self.history_x[0]
            if old == 1:
                self.count_x -= 1
        self.history_x.append(x_val)
        if x_val == 1:
            self.count_x += 1

    def _append_history(self, val):
        """Добавляет значение в основную историю и корректирует счётчики"""
        if len(self.history) == self.maxl:
            old = self.history[0]
            if old == 1:
                self.count_p -= 1
            elif old == -1:
                self.count_n -= 1

        self.history.append(val)
        if val == 1:
            self.count_p += 1
        elif val == -1:
            self.count_n += 1
            
    def calc_iter(self):
        """Быстрая версия расчёта корреляции"""
        if self.is_first_iter:
            self.is_first_iter = False
            self.x.prev_val = self.x.detector.curr_val
            self.y.prev_val = self.y.detector.curr_val

        x_val = self.x.detector.curr_val
        y_val = self.y.detector.curr_val

        # Добавляем x в историю
        self._append_x(x_val)

        # Обновляем основную историю
        if x_val * y_val == 1:
            self._append_history(1)
        elif (1 - x_val) * y_val == 1:
            self._append_history(-1)
        elif y_val == 1:
            self._append_history(0)

        # Вычисляем средние и нормированные значения
        len_h = len(self.history)
        len_hx = len(self.history_x)
        if len_hx == 0 or len_h == 0:
            self.value = 0.0
            return

        avg_x = self.count_x / len_hx
        if avg_x == 0 or avg_x == 1:
            self.value = 0.0
            return

        p = self.count_p / len_h
        n = self.count_n / len_h

        self.norm_p = p / avg_x
        self.norm_n = n / (1 - avg_x)
        denom = (self.norm_p + self.norm_n)
        self.value = (self.norm_p - self.norm_n) / denom if denom != 0 else 0.0
            
# -------------------------------
# 2. Класс нейрона
# -------------------------------
class Neuron:
    def __init__(self, id: int, detectors: List[Detector], dofams: List[Detector], controls: List[Detector]):
        self.bias = 0.0
        self.pins_x: List[Pin] = []
        self.pins_d: List[Pin] = []
        self.pins_c: List[Pin] = []
        #self.correlations: List[Correlation] = []
        self.detectors = detectors
        self.dofams = dofams
        self.controls = controls
        self.add_dpin()
        self.add_pin('Detector', self.pins_d[0])
        self.add_pin('Control', self.pins_d[0])
        
    def add_dpin(self):
        pin = DPin(len(self.pins_d), self.detectors, self.dofams, self.controls)
        self.pins_d.append(pin)
            
    def add_pin(self, type: str, y_pin: DPin):
        if type == 'Detector':
            pin = Pin(len(self.pins_d),type, self.detectors, self.dofams, self.controls, y_pin)
            self.pins_x.append(pin)
        elif type == 'Control':
            pin = Pin(len(self.pins_d),type, self.detectors, self.dofams, self.controls, y_pin)
            self.pins_c.append(pin)
        
    # def add_corr(self, corr: Correlation):
    #     self.correlations.append(corr)
        
    def calc_iter(self):
        for p_d in self.pins_d:
            p_d.search_link()
        for p_x in self.pins_x:
            p_x.search_link()
        for p_c in self.pins_c:
            p_c.search_link()
        v_x = self.pins_x[0].detector.curr_val
        v_c = self.pins_c[0].detector.curr_val
        # тестовая логика среды потом удалить
        # self.pins_d[0].detector.curr_val = v_x * v_c
        for p_x in self.pins_x:
            p_x.correlation.calc_iter()
        for p_c in self.pins_c:
            p_c.correlation.calc_iter()
        for p_d in self.pins_d:
            p_d.correlation.calc_iter()
        for p_d in self.pins_d:
            p_d.prev_val = p_d.detector.curr_val
        for p_x in self.pins_x:
            p_x.prev_val = p_x.detector.curr_val
        for p_c in self.pins_c:
            p_c.prev_val = p_c.detector.curr_val
            
    def calc_control(self):
        p1 = 0.00046 # 0.00046
        p2 = 0.04 # 0.04
        p3 = p1/p2 # 0.0115
        A1 = 1 if random.random() < p2 else 0
        A2 = 1 if random.random() < 0.5 else 0
        A3 = 1 if random.random() < p3 else 0
        
        A4 = 1 if random.random() < 0.5 else 0

        B = A1*A2*A3
        
        self.pins_x[0].detector.curr_val = A1
        if self.pins_c[0].correlation.value < 10:
            self.pins_c[0].detector.curr_val = A2
        else:
            self.pins_c[0].detector.curr_val = self.pins_x[0].detector.curr_val
            
        self.pins_d[0].detector.curr_val = B if random.random() < 0.9995 else A4
        
# -------------------------------
# 2. Класс мозга
# -------------------------------
class Brain:
    def __init__(self):
        self.neurons: List[Neuron] = []
        self.detectors: List[Detector] = []
        self.dofams: List[Detector] = []
        self.controls: List[Detector] = []
        start_detector = Detector(0, 'Detector')
        self.detectors.append(start_detector)
        start_dofam = Detector(0, 'Dofam')
        self.dofams.append(start_dofam)
        start_control = Detector(0, 'Control')
        self.controls.append(start_control)
        start_neuron = Neuron(0,self.detectors, self.dofams, self.controls)
        self.add_neuron(start_neuron)

    def add_neuron(self, neuron: Neuron):
        self.neurons.append(neuron)
    
    def calc_iter(self):
        for n in self.neurons:
            n.calc_iter()
            n.calc_control()



p1 = 0.00046
p2 = 0.04
p3 = p1/p2
steps = 500000
restart = True # True если хочешь стирать состояние мозга при перезапуске
is_new: bool = False
if os.path.exists('/home/vboxuser/bacterium/cub/b1/data.pkl'):
    if restart:
        os.remove('/home/vboxuser/bacterium/cub/b1/data.pkl')
        is_new = True
    else:
        with open('/home/vboxuser/bacterium/cub/b1/data.pkl', 'rb') as f:
            br = pickle.load(f)
else:
    is_new = True
if is_new:
    br = Brain()
    
a_Dofam, a_Detect, a_Control = [], [], []
weightsX, weightsC, weightsD = [], [], []

for t in range(steps):
    br.calc_iter()
    weightsX.append(br.neurons[0].pins_x[0].correlation.value)
    weightsC.append(br.neurons[0].pins_c[0].correlation.value)
    weightsD.append(br.neurons[0].pins_d[0].correlation.value)
    
sss = 1
with open('/home/vboxuser/bacterium/cub/b1/data.pkl', 'wb') as f:
    pickle.dump(br, f)

# визуализация
print('длина истории с d=1: ',len(br.neurons[0].pins_x[0].correlation.history))
print('длина истории с x: ',len(br.neurons[0].pins_x[0].correlation.history_x))
print('norm_p с x: ',br.neurons[0].pins_x[0].correlation.norm_p)
print('norm_n с x: ',br.neurons[0].pins_x[0].correlation.norm_n)
print('value с x: ',br.neurons[0].pins_x[0].correlation.value)
print('norm_p с c: ',br.neurons[0].pins_c[0].correlation.norm_p)
print('norm_n с c: ',br.neurons[0].pins_c[0].correlation.norm_n)
print('value с c: ',br.neurons[0].pins_c[0].correlation.value)
print('norm_p с d: ',br.neurons[0].pins_d[0].correlation.norm_p)
print('norm_n с d: ',br.neurons[0].pins_d[0].correlation.norm_n)
print('value с d: ',br.neurons[0].pins_d[0].correlation.value)
plt.figure(figsize=(7,4))
plt.plot(weightsX, label='Сила связи pinX')
plt.plot(weightsC, label='Сила связи pinC')
# plt.plot(weightsD, label='Сила связи pinD')
plt.title('Рост связи при совместной активности (правило Хебба)')
plt.xlabel('Время (шаги)')
plt.ylabel('Вес w_AB')
plt.legend()
plt.show()



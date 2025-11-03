import numpy as np
#from typing import TypeVar, Generic
from typing import List, Union, Any, Dict, Optional
#Matrix = TypeVar('Neuron', bound=Neuron)
from collections import deque
import matplotlib.pyplot as plt
import random
        
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
        self.history = deque(maxlen=100)
        self.value = 0.5
        
    def calc_iter(self):
        x_val = self.x.detector.curr_val
        y_val = self.y.detector.curr_val
        if (x_val == y_val):
            self.history.append(1)
        else:
            self.history.append(-1)
        count_p = sum(1 for h in self.history if h == 1)
        count_m = len(self.history) - count_p
        self.value = (count_p - count_m)/len(self.history)
        if self.x.type == 'Control':
            bit_rand = 1 if random.random() < self.value else 0
            self.x.detector.curr_val = bit_rand
            
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
        self.pins_d[0].detector.curr_val = v_x * v_c
        for p_x in self.pins_x:
            p_x.correlation.calc_iter()
        for p_c in self.pins_c:
            p_c.correlation.calc_iter()
        for p_d in self.pins_d:
            p_d.correlation.calc_iter()
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

steps = 500
br = Brain()
a_Dofam, a_Detect, a_Control = [], [], []
weightsX, weightsC, weightsD = [], [], []
# случайная активность нейронов (0 или 1)
for t in range(steps):
    A1 = np.random.randint(0,2)
    A2 = np.random.randint(0,2)
    B = A1*A2
    a_Control.append(A1)  # выход
    a_Detect.append(A2)  # вход
    a_Dofam.append(A1*A2)  # дофамин
    # ran = np.random.randint(0,2)
    # if ran == 0:
    #     #a_B1.append(np.random.randint(0,2))
    #     a_A1.append(1)
    # else:
    #     a_A1.append(1)
for t in range(steps):
    br.detectors[0].curr_val = a_Detect[t]
    # br.dofams[0].curr_val = a_Dofam[t]
    # br.controls[0].curr_val = a_Control[t]
    br.calc_iter()
    weightsX.append(br.neurons[0].pins_x[0].correlation.value)
    weightsC.append(br.neurons[0].pins_c[0].correlation.value)
    weightsD.append(br.neurons[0].pins_d[0].correlation.value)
sss = 1
# визуализация
plt.figure(figsize=(7,4))
plt.plot(weightsX, label='Сила связи pinX')
plt.plot(weightsC, label='Сила связи pinC')
plt.plot(weightsD, label='Сила связи pinD')
plt.title('Рост связи при совместной активности (правило Хебба)')
plt.xlabel('Время (шаги)')
plt.ylabel('Вес w_AB')
plt.legend()
plt.show()
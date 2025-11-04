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
        self.maxl = 100000
        self.history = deque(maxlen=self.maxl)
        self.value = 0
        self.is_first_iter = True
        
        
    def calc_iter(self):
        if self.is_first_iter:
            self.is_first_iter = False
            self.x.prev_val = self.x.detector.curr_val
            self.y.prev_val = self.y.detector.curr_val
         
        x_val = self.x.detector.curr_val - self.x.prev_val
        y_val = self.y.detector.curr_val - self.y.prev_val
        
        if x_val != 0 and y_val != 0:
            if (x_val == y_val):
                self.history.append(1)
            elif x_val == -y_val:
                self.history.append(-1)
            elif x_val == 0:
                self.history.append(0)
            len_h = len(self.history)
            count_p = sum(1 for x in self.history if x == 1)
            count_m = sum(1 for x in self.history if x == -1)
            #self.value = len_h/self.maxl * (count_p - count_m)/len_h
            self.value = (count_p - count_m)/len_h
        
        # if self.x.type == 'Control':
            # if self.value < 10:
            #     self.x.detector.curr_val = 1 if random.random() < 0.5 else 0
            # else:
            #     self.x.detector.curr_val = self.x.detectors[0].curr_val
            # A1 = self.x.detectors[0].curr_val
            # A2 = self.x.detector.curr_val
            # A3 = 1 if random.random() < 0.5 else 0
            # A4 = A1*A2
            # self.x.dofams[0].curr_val = A4 if random.random() < 0.5 else A3
            
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
        p3 = p1/p2
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
        self.pins_d[0].detector.curr_val = B if random.random() < 1 else A4
        
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
steps = 20000
br = Brain()
a_Dofam, a_Detect, a_Control = [], [], []
weightsX, weightsC, weightsD = [], [], []
# случайная активность нейронов (0 или 1)
for t in range(steps):
    # A1 = 1 if random.random() < p2 else 0
    # A2 = 1 if random.random() < 0.5 else 0
    # A3 = 1 if random.random() < p3 else 0
    # A4 = A1*A3
    # B = A2*A4
    # B1 = A2
    # A1 = A4
    A1 = 1 if random.random() < 0.5 else 0
    A2 = 1 if random.random() < 0.5 else 0
    A3 = 1 if random.random() < 0.5 else 0
    A4 = A1*A2
    B = A4 if random.random() < 1 else A3
    # a_Control.append(A2)  # выход
    a_Detect.append(A1)  # вход
    # a_Dofam.append(B)  # дофамин
for t in range(steps):
    # br.detectors[0].curr_val = a_Detect[t]
    # br.dofams[0].curr_val = a_Dofam[t]
    # br.controls[0].curr_val = a_Control[t]
    

    
    if t == 998:
        d = 0
    br.calc_iter()
    weightsX.append(br.neurons[0].pins_x[0].correlation.value)
    weightsC.append(br.neurons[0].pins_c[0].correlation.value)
    weightsD.append(br.neurons[0].pins_d[0].correlation.value)
    
    # if self.value < 10:
    #     self.x.detector.curr_val = 1 if random.random() < 0.5 else 0
    # else:
    #     self.x.detector.curr_val = self.x.detectors[0].curr_val
    # br.neurons[0].pins_c[0].detector.curr_val = 1 if random.random() < 0.5 else 0
    # A1 = br.neurons[0].detectors[0].curr_val
    # A2 = br.neurons[0].pins_c[0].detector.curr_val
    # A3 = 1 if random.random() < 0.5 else 0
    # A4 = A1*A2
    # br.neurons[0].dofams[0].curr_val = A4 if random.random() < 0.5 else A3
sss = 1
# визуализация
print('длина истории с детектора: ',len(br.neurons[0].pins_x[0].correlation.history))
print('длина истории с контроллера: ',len(br.neurons[0].pins_c[0].correlation.history))
plt.figure(figsize=(7,4))
plt.plot(weightsX, label='Сила связи pinX')
plt.plot(weightsC, label='Сила связи pinC')
plt.plot(weightsD, label='Сила связи pinD')
plt.title('Рост связи при совместной активности (правило Хебба)')
plt.xlabel('Время (шаги)')
plt.ylabel('Вес w_AB')
plt.legend()
plt.show()
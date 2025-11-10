import numpy as np
from collections import Counter
class Bisection:
    def __init__(self):
        self.max_m = 0
        self.min = 0
        self.med = 0
        self.k = 1
        self.sec = 0
    def normalase_val(self, val):
        if val > self.max_m:
            self.max_m = val
            self.sec = self.max - self.min
        
        if self.k == 1:
            self.min = med
            self.max = med + self.sec

# Пример с бинарной последовательностью
source = [500, 100, 102, 1003, 200, 5, 123, 126, 0, 50, 300, 320, 58, 1, 10, 15, 25, 107, 3, 45, 128, 405, 10, 10, 100, 61]
result = [1 if x <= 2 else 0 for x in source]
max=0
med=0
k=-2
i = 0
bi = Bisection()
for v in source:
    bi.normalase_val(v)
    i += 1

print("max_m: ", bi.max_m)
print("med: ", bi.med)
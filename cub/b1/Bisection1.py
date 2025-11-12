import numpy as np
from collections import Counter
class Bisection:
    def __init__(self):
        self.max_m = 2000
        self.max = self.max_m
        self.min = self.max_m/2
        self.is_changed = False
        self.sec = self.max_m/2
        self.min_sec = 1
        self.is_error = False
        
    def change_sec(self):
        self.max = self.min
        self.min = self.min - self.sec
        self.is_changed = True
        
    def decrease_sec(self):
        self.sec = self.sec/2
        self.min = self.max - self.sec
        self.is_changed = False
            
    def check(self, source, result):
        i = 0
        d = False
        val = -1
        for v in source:
            res = result[i]
            i += 1
            if res == 1:
                d = True
                val = v
                break
        if d and val >= self.min and val <= self.max:
            return True
        else:
            return False
        
    def check_min_sec(self):
        if self.sec/2 <= self.min_sec:
            return True
        else:
            return False

# Пример с бинарной последовательностью
source = [500, 100, 102, 1003, 200, 5, 123, 126, 0, 50, 300, 320, 58, 1, 10, 15, 25, 107, 3, 45, 128, 405, 10, 10, 100, 61]
result = [1 if x <= 58 and x >= 50 else 0 for x in source]
max=0
med=0
i = 0
# Инициализируем
bi = Bisection()
is_while = True
while is_while:
    print("i: ", i)
    print("sec: ", bi.sec)
    print("min: ", bi.min)
    print("max: ", bi.max)
    i += 1
    ch = bi.check(source, result)
    if ch:
        if bi.check_min_sec():
            bi.is_error = False
            is_while = False
            break
        else:
            bi.decrease_sec()
    else:
        if bi.is_changed:
            bi.is_error = True
            is_while = False
            break
        else:
            bi.change_sec()
            is_while = True


print("i: ", i)
print("sec: ", bi.sec)
print("min: ", bi.min)
print("max: ", bi.max)
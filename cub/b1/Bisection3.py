import numpy as np
from collections import Counter
class Bisection:
    def __init__(self, min, max):
        self.max_m = 2000
        self.max = 0
        self.min = 0
        self.min_l = 0
        self.min_r = 0
        self.max_l = 0
        self.max_r = 0
        self.set_min_max(min, max)
        
    def set_min_max(self, min, max):
        self.max = max
        self.min = min
        self.min_l = min
        self.max_l = min + (max-min)/2
        self.min_r = self.max_l
        self.max_r = max
            
    def calc_prob(self, source, result, min, max):
        i = 0
        d = False
        sum_pos = 0
        for v in source:
            res = result[i]
            i += 1
            if res == 1:
                if v >= min and v <= max:
                    sum_pos += 1
        return sum_pos

# Пример с бинарной последовательностью
source = [500, 100, 102, 1003, 200, 5, 123, 125, 0, 50, 300, 320, 58, 1, 10, 15, 25, 107, 3, 45, 128, 405, 10, 10, 100, 61]
result = [1 if x >= 58 and x <= 126 else 0 for x in source]
max=0
med=0
i = 0
# Инициализируем
bi = Bisection(0,2000)
is_while = True
while is_while:
    print("i: ", i)
    print("max_m: ", bi.max_m)
    print("min: ", bi.min)
    print("max: ", bi.max)
    i += 1
    p0 = bi.calc_prob(source, result, bi.min, bi.max)
    p1 = bi.calc_prob(source, result, bi.min_l, bi.max_l)
    p2 = bi.calc_prob(source, result, bi.min_r, bi.max_r)
    arr_p = [p0, p1, p2]
    arr_p.sort(reverse=True)
    max_p = arr_p[0]
    if max_p == p0:
        if  p2 == max_p:
            bi.set_min_max(bi.min_r, bi.max_r)
        elif p1 == max_p:
            bi.set_min_max(bi.min_l, bi.max_l)
        else:
            break
    elif p1 >= p2:
        bi.set_min_max(bi.min_l, bi.max_l)
    else:
        bi.set_min_max(bi.min_r, bi.max_r)
    # защита от бесконечного цикла
    if i > 1000000:
        print("слишком длнииый цикл: ", i)
        break


print("i: ", i)
print("min: ", bi.min)
print("max: ", bi.max)
import numpy as np
import random
import matplotlib.pyplot as plt
k = 1
s = 5
k = k*s-s/2
output = np.array([n for n in np.arange(0, 1, 0.01)])
prob = np.array([1 / (1 + np.exp(-(k*s-s/2))) for k in output])
#res = 1 if random.random() < prob else 0

plt.figure(figsize=(7,4))
plt.plot(prob, label='Сила связи pinX')
# plt.plot(weightsC, label='Сила связи pinC')
# plt.plot(weightsD, label='Сила связи pinD')
plt.title('Рост связи при совместной активности (правило Хебба)')
plt.xlabel('Время (шаги)')
plt.ylabel('Вес w_AB')
plt.legend()
plt.show()
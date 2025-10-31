import numpy as np
import random
import matplotlib.pyplot as plt

# -------------------------------
# 1. Среда
# -------------------------------
# Простая: reward=1 если vision=1 и action=1, иначе 0
def environment(vision, action):
    return 1 if (vision == 1 and action == 1) else 0

# Генератор входов (случайное зрение)
def random_vision():
    return random.choice([0, 1])

# -------------------------------
# 2. Класс нейрона
# -------------------------------
class Neuron:
    def __init__(self, inputs_idx, n_inputs):
        self.inputs_idx = inputs_idx            # какие сенсоры он видит
        self.w = np.random.randn(len(inputs_idx)) * 0.01
        self.bias = 0.0
        self.activity = 0.0
        self.utility = 0.0
        self.age = 0

    def activate(self, x):
        s = np.dot(self.w, x[self.inputs_idx]) - self.bias
        self.activity = 1 / (1 + np.exp(-s))
        return self.activity

    def update_weights(self, x, modulator, eta=0.1, decay=0.001):
        # Reward-модулированный Хебб
        for i, idx in enumerate(self.inputs_idx):
            dw = eta * modulator * self.activity * x[idx] - decay * self.w[i] * self.activity**2
            self.w[i] += dw

        # Homeostasis
        target_activity = 0.3
        self.bias += 0.01 * (self.activity - target_activity)

    def update_utility(self, local_err, modulator):
        # полезность = reward × уменьшение ошибки
        self.utility = 0.9 * self.utility + 0.1 * (modulator * (1 - local_err))
        self.age += 1

# -------------------------------
# 3. Мозг бактерии
# -------------------------------
class BacteriumBrain:
    def __init__(self, n_inputs, max_neurons=50):
        self.n_inputs = n_inputs
        self.neurons = []
        self.max_neurons = max_neurons
        self.resources = max_neurons

    def forward(self, x):
        # вычисляем все активности
        if not self.neurons:
            return np.zeros(1)
        acts = np.array([n.activate(x) for n in self.neurons])
        return acts

    def choose_action(self, x):
        # действие определяется суммой активности + шум
        output = np.mean(self.forward(x)) if self.neurons else 0
        prob = 1 / (1 + np.exp(-output))
        return 1 if random.random() < prob else 0

    def learn(self, x, reward, prev_reward):
        # локальная ошибка = |reward - prev_reward|
        local_err = abs(reward - prev_reward)
        modulator = reward - 0.5 * local_err  # reward > 0 усиливает Hebb
        # обновляем все существующие нейроны
        for n in self.neurons:
            n.update_weights(x, modulator)
            n.update_utility(local_err, modulator)

        # рост
        if local_err > 0.4 and self.resources > 0:
            self.grow_neuron(x)

        # pruning
        self.prune_neurons()

    def grow_neuron(self, x):
        active_inputs = np.argsort(np.abs(x))[-2:]  # top-2 входа
        new_neuron = Neuron(inputs_idx=active_inputs, n_inputs=self.n_inputs)
        self.neurons.append(new_neuron)
        self.resources -= 1

    def prune_neurons(self):
        before = len(self.neurons)
        self.neurons = [n for n in self.neurons if n.utility > 0.01 or n.age < 50]
        self.resources += before - len(self.neurons)

# -------------------------------
# 4. Симуляция
# -------------------------------
brain = BacteriumBrain(n_inputs=2, max_neurons=1)
rewards, num_neurons, errors = [], [], []
prev_reward = 0

for t in range(1000):
    vision = random_vision()
    x = np.array([vision, random.random()])  # сенсор + шумовой канал
    action = brain.choose_action(x)
    reward = environment(vision, action)

    brain.learn(x, reward, prev_reward)

    # метрики
    rewards.append(reward)
    num_neurons.append(len(brain.neurons))
    errors.append(abs(reward - prev_reward))
    prev_reward = reward

# -------------------------------
# 5. Визуализация
# -------------------------------
plt.figure(figsize=(20,5))
plt.subplot(3,1,1)
plt.plot(rewards, label="Reward")
plt.legend(); plt.ylabel("Reward")

plt.subplot(3,1,2)
plt.plot(errors, label="Local error", color='orange')
plt.legend(); plt.ylabel("Error")

plt.subplot(3,1,3)
plt.plot(num_neurons, label="Num neurons", color='green')
plt.legend(); plt.ylabel("Neurons")
plt.xlabel("Time steps")
plt.tight_layout()
plt.show()
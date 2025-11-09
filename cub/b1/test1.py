import numpy as np
from collections import Counter

def calculate_entropy(sequence):
    """
    Универсальная функция для расчета энтропии
    """
    # Подсчет частот символов
    counter = Counter(sequence)
    total = len(sequence)
    
    # Расчет вероятностей и энтропии
    probabilities = [count / total for count in counter.values()]
    entropy = -sum(p * np.log2(p) for p in probabilities if p > 0)
    
    return entropy

# Пример с бинарной последовательностью
binary_seq = [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1]
entropy = calculate_entropy(binary_seq)
print(f"Энтропия: {entropy:.4f}")
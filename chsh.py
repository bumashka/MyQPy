import random
import library
from quantum_system import QuantumSystem
import math
import numpy as np
def chsh_classical():
    you, eve = lambda your_input: 0, lambda eve_input: 0
    your_input, eve_input = random.randint(0, 1), random.randint(0, 1)
    parity = 0 if you(your_input) == eve(eve_input) else 1
    res = parity == (your_input and eve_input)
    return res

def chsh_quantum():

    my_question = library.random_generator()
    eve_question = library.random_generator()

    qs = QuantumSystem([0, 0])

    qs.hadamard([0])
    qs.cnot(0, 1)

    if my_question == 0:
        qs.ry(math.pi / 2, [0])
    else:
        qs.ry(0, [0])

    if eve_question == 0:
        qs.ry(math.pi / 4, [1])
    else:
        qs.ry(3 * math.pi / 4, [1])

    p = np.power(qs.return_qs_states(), 2)
    choice = np.random.choice(len(p), p=np.real(p).flatten())

    if choice == 0:
        my_answer = eve_answer = 0
    elif choice == 1:
        my_answer, eve_answer = 0, 1
    elif choice == 2:
        my_answer, eve_answer = 1, 0
    else:
        my_answer = eve_answer = 1

    if (my_question and eve_question) == (my_answer ^ eve_answer):
        return 1

    return 0

n = 1000

classical_sum = 0
quantum_sum = 0

for idx_game in range(n):
    classical_sum = classical_sum + chsh_classical()
    quantum_sum = quantum_sum + chsh_quantum()

print(f"Вероятность выигрыша в классическом подходе: {classical_sum/n} %")
print(f"Вероятность выигрыша в квантовом подходе: {quantum_sum/n} %")


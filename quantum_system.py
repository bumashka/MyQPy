import numpy as np
from main import MyQPy


class QuantumSystem():
    def __init__(self, initial_states: list):
        qu_lib = MyQPy()
        self.system_size = len(initial_states)
        self.quantum_system = 1
        for i in range(0, self.system_size):
            if initial_states[i] == 0:
                self.quantum_system = np.kron(self.quantum_system, qu_lib.ket_0())
            else:
                self.quantum_system = np.kron(self.quantum_system, qu_lib.ket_1())

    def hadamard(self, register):
        pass

    def cnot(self, control: int, target: int):
        pass

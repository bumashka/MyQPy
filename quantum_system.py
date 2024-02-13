import numpy as np
from main import MyQPy


class QuantumSystem:
    def __init__(self, initial_states: list):
        self.qu_lib = MyQPy()
        self.system_size = len(initial_states)
        self.quantum_system = 1
        for i in range(0, self.system_size):
            if initial_states[i] == 0:
                self.quantum_system = np.kron(self.quantum_system, self.qu_lib.ket_0())
            else:
                self.quantum_system = np.kron(self.quantum_system, self.qu_lib.ket_1())

    def simple_gate(self, operation, register: int = 0, total=False):
        if total:
            system = operation
            for i in range(0, self.system_size):
                system = np.kron(system, operation)
        else:
            system = 1
            for i in range(0, self.system_size):
                if i == register:
                    system = np.kron(system, operation)
                else:
                    system = np.kron(system, self.qu_lib.i())
        self.quantum_system = system @ self.quantum_system

    def hadamard(self, register: int = 0, total=False):
        self.simple_gate(self.qu_lib.hadamard(), register, total)

    def x(self, register: int = 0, total=False):
        self.simple_gate(self.qu_lib.x(), register, total)

    def z(self, register: int = 0, total=False):
        self.simple_gate(self.qu_lib.z(), register, total)

    def cnot(self, control: int, target: int):

        controlled_proj = self.qu_lib.ket_0() @ np.transpose(self.qu_lib.ket_1())
        target_proj = (self.qu_lib.ket_1()) @ np.transpose(self.qu_lib.ket_1())

        for i in range(control, target):
            controlled_proj = np.kron(controlled_proj, self.qu_lib.i())
            target_proj = np.kron(target_proj, self.qu_lib.i())

        controlled_proj = np.kron(controlled_proj, self.qu_lib.i())
        target_proj = np.kron(target_proj, self.qu_lib.x())

        for i in range(0, control):
            controlled_proj = np.kron(self.qu_lib.i(), controlled_proj)
            target_proj = np.kron(self.qu_lib.i(), target_proj)

        for i in range(target, self.system_size):
            controlled_proj = np.kron(controlled_proj, self.qu_lib.i())
            target_proj = np.kron(target_proj, self.qu_lib.i())

        result = controlled_proj + target_proj

        self.quantum_system = result @ self.quantum_system

    def measure(self, register):
        rho = np.outer(self.quantum_system, np.conj(self.quantum_system))

        before_cubit = np.eye(2 ** register) if register > 0 else 1
        after_cubit = np.eye(2 ** (self.system_size - register))

        prob_0 = np.trace(np.kron(before_cubit, np.kron(self.qu_lib.projector_0(), after_cubit)) @ rho)

        return prob_0.round() > 0

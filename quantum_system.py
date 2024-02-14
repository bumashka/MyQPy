import numpy as np

import library


class QuantumSystem:
    def __init__(self, initial_states: list):
        self.system_size = len(initial_states)
        self.quantum_system = 1
        for i in range(0, self.system_size):
            l = type(initial_states[i])
            if type(initial_states[i]) is int and initial_states[i] == 0:
                self.quantum_system = np.kron(self.quantum_system, library.ket_0())
            elif type(initial_states[i]) is int and initial_states[i] == 1:
                self.quantum_system = np.kron(self.quantum_system, library.ket_1())
            else:
                self.quantum_system = np.kron(self.quantum_system, initial_states[i])

    def return_qs_states(self):
        return self.quantum_system

    def simple_gate(self, operation, reg_range = None):
        if reg_range is None:
            reg_range = []
        system = 1
        if reg_range:
            for i in range(0, self.system_size):
                if i in reg_range:
                    system = np.kron(system, operation)
                else:
                    system = np.kron(system, library.i())
        self.quantum_system = system @ self.quantum_system

    def hadamard(self, reg_range = None):
        self.simple_gate(library.hadamard(), reg_range)

    def x(self, reg_range = None):
        self.simple_gate(library.x(), reg_range)

    def z(self, reg_range = None):
        self.simple_gate(library.z(), reg_range)

    def ry(self, angle, reg_range = None):
        self.simple_gate(library.RY(angle), reg_range)

    def cnot(self, control: int, target: int):

        controlled_proj = library.projector_0()
        target_proj = library.projector_1()

        for i in range(control, target - 1):
            controlled_proj = np.kron(controlled_proj, library.i())
            target_proj = np.kron(target_proj, library.i())

        controlled_proj = np.kron(controlled_proj, library.i())
        target_proj = np.kron(target_proj, library.x())

        for i in range(0, control):
            controlled_proj = np.kron(library.i(), controlled_proj)
            target_proj = np.kron(library.i(), target_proj)

        for i in range(target + 1, self.system_size):
            controlled_proj = np.kron(controlled_proj, library.i())
            target_proj = np.kron(target_proj, library.i())

        result = controlled_proj + target_proj

        self.quantum_system = result @ self.quantum_system

    def measure(self, register):
        rho = np.outer(self.quantum_system, np.conj(self.quantum_system))

        before_cubit = np.eye(2 ** register) if register > 0 else 1
        after_cubit = np.eye(2 ** (self.system_size - register - 1))

        prob_0 = np.trace(np.kron(before_cubit, np.kron(library.projector_0(), after_cubit)) @ rho)

        return prob_0

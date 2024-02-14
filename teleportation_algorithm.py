from quantum_system import QuantumSystem
import library
import math

def teleportation(state):

    qc = QuantumSystem([state, 0, 0])

    qc.hadamard([1])

    qc.cnot(1, 2)

    qc.cnot(0, 1)

    qc.hadamard([1])

    res_0 = qc.measure(0)
    res_1 = qc.measure(1)

    if res_0:
        qc.x([2])
    if res_1:
        qc.z([2])

    print(f"Measure system:{[qc.measure(i) for i in range(0, 3)]}")

teleportation(library.RY(math.pi/3)@library.ket_0())
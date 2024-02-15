from quantum_system import QuantumSystem
import library
import math

def teleportation_00(state):

    qc = QuantumSystem([state, 0, 0])

    qc.hadamard([1])

    qc.cnot(0, 2)

    qc.hadamard([0])

    res_0 = qc.measure([0], False)
    res_1 = qc.measure([1], False)

    if res_0.round() > 0:
        qc.x([2])
    if res_1.round() > 0:
        qc.z([2])

    qc.measure([2])

def teleportation_10(state):

    qc = QuantumSystem([state, 0, 0])

    qc.x([1])

    qc.hadamard([1])

    qc.cnot(0, 2)

    qc.hadamard([0])

    qc.z([2])

    res_0 = qc.measure([0], False)
    res_1 = qc.measure([1], False)

    if res_0:
        qc.x([2])
    if res_1:
        qc.z([2])

    qc.measure([2])

def teleportation_01(state):

    qc = QuantumSystem([state, 0, 0])

    qc.x([2])

    qc.hadamard([1])

    qc.cnot(0, 2)

    qc.hadamard([0])

    qc.x([1])

    res_0 = qc.measure([0], False)
    res_1 = qc.measure([1], False)

    if res_0:
        qc.x([2])
    if res_1:
        qc.z([2])

    qc.measure([2])

def teleportation_11(state):

    qc = QuantumSystem([state, 0, 0])

    qc.x([2])

    qc.x([1])

    qc.hadamard([1])

    qc.cnot(0, 2)

    qc.hadamard([0])

    qc.x([1])

    qc.z([2])

    res_0 = qc.measure([0], False)
    res_1 = qc.measure([1], False)

    if res_0.round() > 0:
        qc.x([2])
    if res_1.round() > 0:
        qc.z([2])

    qc.measure([2])

teleportation_00(library.RY(math.pi/5)@library.ket_0())
teleportation_01(library.RY(math.pi/5)@library.ket_0())
teleportation_10(library.RY(math.pi/5)@library.ket_0())
teleportation_11(library.RY(math.pi/5)@library.ket_0())

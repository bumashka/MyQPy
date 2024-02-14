import numpy as np

X = np.array([
    [0, 1],
    [1, 0]
], dtype=complex)

Z = np.array([
    [1, 0],
    [0, -1]
], dtype=complex)

RY = lambda phi: np.array([
    [np.cos(phi / 2), -np.sin(phi / 2)],
    [np.sin(phi / 2), np.cos(phi / 2)]
], dtype=complex)

# self.Fi = lambda a, b: a @ self.KET_0 + b @ self.KET_1

KET_0 = np.array([[1], [0]], dtype=complex)

HADAMARD = np.array([
    [1, 1],
    [1, -1]
], dtype=complex) / np.sqrt(2)

I = np.array([
    [1, 0],
    [0, 1]
], dtype=complex)

CNOT = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
], dtype=complex)


def ket_0():
    return KET_0


def ket_1():
    return X @ KET_0


def hadamard():
    return HADAMARD


def cnot():
    return CNOT


def x():
    return X


def i():
    return I


def z():
    return Z


def projector_0():
    return KET_0 @ np.transpose(KET_0)


def projector_1():
    return ket_1() @ np.transpose(ket_1())

def measure(state):
    # pr0 = np.abs(np.transpose(state)@self.KET_0) ** 2
    pr0 = np.abs(state[0, 0]) ** 2
    sample = np.random.random() <= pr0
    return False if sample else True

def random_generator():
    qubit = ket_0()
    qubit = hadamard() @ qubit
    result = measure(qubit)
    return result

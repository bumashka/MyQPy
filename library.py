import numpy as np

X = np.array([
    [0, 1],
    [1, 0]
], dtype=complex)

Z = np.array([
    [1, 0],
    [0, -1]
], dtype=complex)

Y = np.array([
    [0, 0],
    [0, 0]
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

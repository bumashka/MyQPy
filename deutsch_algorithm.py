import library
import numpy as np


def deutsch_oracle(type):
    if type == 0:
        return np.kron(library.i(), library.i())
    elif type == 1:
        return np.kron(library.i(), library.x())
    elif type == 2:
        return library.cnot()
    else:
        return np.kron(library.x(), library.i()) @ library.cnot() @ np.kron(library.x(), library.i())


def deutsch_alg(type):
    x = library.ket_0()

    y = library.ket_1()

    xy = np.kron(library.hadamard(), library.hadamard()) @ np.kron(x, y)

    xy = deutsch_oracle(type) @ xy

    xy = np.kron(library.hadamard(), library.i()) @ xy

    # дополнительная лекция по измерениям №5
    # считаем матрицу плотности полученного состояния, через внешнее произведение
    rho = np.outer(xy, np.conj(xy))

    # trace - след матрицы, сумма элементов по диагонали
    # np.dot - скалярное произведение

    prob_0 = np.trace(np.kron(library.projector_0(), library.i()) @ rho)

    return '0' if prob_0.round() > 0 else '1'


print(f"f(x)=0   : {deutsch_alg(0)}")
print(f"f(x)=1   : {deutsch_alg(1)}")
print(f"f(x)=x   : {deutsch_alg(2)}")
print(f"f(x)=!x  : {deutsch_alg(3)}")

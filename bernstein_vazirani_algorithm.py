from quantum_system import QuantumSystem


def bernstein_vazirani_alg(number: str):
    number = list(number)
    n = len(number)

    qc = QuantumSystem([0] * n + [1])

    qc.hadamard(range(n + 1))

    for i in range(0, n):
        if number[i] == '1':
            qc.cnot(i, n)

    qc.hadamard(range(n + 1))

    for i in range(0, n):
        print(f"{i}--")
        qc.measure([i])

    print(f"a : {number}")



bernstein_vazirani_alg('101')

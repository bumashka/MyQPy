from quantum_system import QuantumSystem
def simon(n, f):
    qc = QuantumSystem([0] * 2 * n)

    qc.hadamard(range(n))

    qc.cnot(f[0][0], f[0][1])
    qc.cnot(f[1][0], f[1][1])

    qc.hadamard(range(n))

    qc.measure([0, 1, 2])

n = 3
f = [[1, n+1], [2, n+2]]
simon(n, f)
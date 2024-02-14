from quantum_system import QuantumSystem
def simon(self, n):
    qc = QuantumSystem([0] * 2 * n)

    qc.hadamard(range(n))

    qc.cnot(1, n + 1)
    qc.cnot(2, n + 2)

    print(f"Measure 2nd register:{[qc.measure(i) for i in range(n, n * 2)]}")

    qc.hadamard(range(n))

    print(f"Measure 1nd register:{[qc.measure(i) for i in range(0, n)]}")

simon(3)
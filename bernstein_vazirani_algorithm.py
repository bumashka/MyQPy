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

    message = []
    prob_list = []
    for i in range(0, n):
        prob_0 = qc.measure(i)
        prob_list.append(prob_0)
        message.append('0') if prob_0.round() > 0 else message.append('1')

    print(f"a : {number}")
    print(f"The string we got using the algorithm is: {message}")
    print(f"The system states (basis 0): {prob_list}")

bernstein_vazirani_alg('101')
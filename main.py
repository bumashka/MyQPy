import random
from quantum_system import QuantumSystem
import numpy as np


class MyQPy:

    def __init__(self):
        self.X = np.array([
            [0, 1],
            [1, 0]
        ], dtype=complex)

        self.Z = np.array([
            [1, 0],
            [0, -1]
        ], dtype=complex)

        self.Y = np.array([
            [0, 0],
            [0, 0]
        ], dtype=complex)

        self.Fi = lambda a, b: a @ self.KET_0 + b @ self.KET_1

        self.KET_0 = np.array([[1], [0]], dtype=complex)
        self.HADAMARD = np.array([
            [1, 1],
            [1, -1]
        ], dtype=complex) / np.sqrt(2)

        self.I = np.array([
            [1, 0],
            [0, 1]
        ], dtype=complex)

        self.CNOT = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ], dtype=complex)

    def ket_0(self):
        return self.KET_0

    def ket_1(self):
        return self.X @ self.KET_0

    def hadamard(self):
        return self.HADAMARD

    def cnot(self):
        return self.CNOT

    def x(self):
        return self.X

    def i(self):
        return self.I

    def z(self):
        return self.Z

    def projector_0(self):
        return self.KET_0 @ np.transpose(self.KET_0)

    def projector_1(self):
        return self.ket_1() @ np.transpose(self.ket_1())

    def measure(self, state):
        # pr0 = np.abs(np.transpose(state)@self.KET_0) ** 2
        pr0 = np.abs(state[0, 0]) ** 2
        # print("Measure\npr0: " + str(pr0))
        sample = np.random.random() <= pr0
        # print("sample: " + str(sample))
        return False if sample else True

    def random_generator(self):
        qubit = self.KET_0.copy()
        qubit = self.HADAMARD @ qubit
        result = self.measure(qubit)
        # print("random_generator returned " + str(result))
        return result

    def send_single_bit_with_bb84(self):
        my_bit = self.random_generator()
        my_basis = self.random_generator()

        eva_basis = self.random_generator()

        qubit = self.prepare_qubit(my_bit, self.KET_0.copy(), my_basis)

        received_qubit = qubit.copy()

        if eva_basis:
            received_qubit = self.HADAMARD @ qubit

        result = self.measure(received_qubit)

        print("((my_bit, my_basis),(eva_bit, eva_basis)): (("
              + str(int(my_bit)) + ", " + str(int(my_basis)) + "),("
              + str(int(result)) + ", " + str(int(eva_basis)) + "))")

        return {"result": str(int(result)),
                "my_basis": my_basis,
                "eva_basis": eva_basis
                }

    def bb84(self, number_of_bits):
        key = ""
        while number_of_bits > 0:
            result = self.send_single_bit_with_bb84()
            if result["my_basis"] == result["eva_basis"]:
                key = ''.join([key, result["result"]])
                number_of_bits -= 1
        return key

    def quantum_strategy(self):
        shared_system = np.kron(self.KET_0, self.KET_0)
        your_qubit = np.kron(self.KET_0 @ np.transpose(self.KET_0), self.I) @ shared_system
        eve_qubit = np.kron(self.X @ self.KET_0 @ np.transpose(self.X @ self.KET_0), self.I) @ shared_system
        shared_system.register_state = qt.bell_state()
        your_angles = [90 * np.pi / 180, 0]
        eve_angles = [45 * np.pi / 180, 135 * np.pi / 180]

        def you(your_input: int):
            your_qubit.ry(your_angles[your_input])
            return your_qubit.measure()

        def eve(eve_input: int):
            eve_qubit.ry(eve_angles[eve_input])
            return eve_qubit.measure()

        return you, eve

    def turn_qubit(self, angle):
        pass

    def teleportation(self):

        # создаем схему
        qc = QuantumSystem([0, 0, 0])
        #qc = np.kron(self.Fi(a, b), np.kron(self.KET_0, self.KET_0))

        # Шаг 1
        # qc.h(qr[1])
        qc.hadamard(1)
        # Шаг 2
        # qc.cx(qr[1], qr[2])
        qc.cnot(1, 2)
        # qc = self.build_up_CNOT(1, 2) @ qc

        # Шаг 3
        # qc.cx(qr[0], qr[1])
        #qc = self.build_up_CNOT(0, 1) @ qc
        qc.cnot(0, 1)
        # Шаг 4
        # qc.h(qr[0])
        # qc = (np.kron(self.HADAMARD, np.kron(self.I, self.I))) @ qc
        qc.hadamard(1)

        # Шаг 5 - измеряются 2 кубита Алисы, чтобы передать результат Бобу
        res_0 = qc.measure(0)
        res_1 = qc.measure(1)

        # Шаг 6 - применяются гейт X и гейт Z в завиимости от того, какое из измерений дает результат 1.
        if res_0:
            qc.x(2)
        if res_1:
            qc.z(2)
        # qc.x(qr[2]).c_if(crx, 1)
        # qc.z(qr[2]).c_if(crz, 1)
        # qc.draw()

    def prepare_qubit(self, bit, qubit, basis):
        if bit:
            qubit = self.X @ qubit
        if basis:
            qubit = self.HADAMARD @ qubit
        return qubit

    def bit_from_qubit(self):
        bit = self.random_generator()
        qubit = self.prepare_qubit(bit, self.KET_0.copy(), False)
        result = self.measure(qubit)
        print("We prepared bit: " + str(bit))
        print("Eve got: " + str(result))
        return result

    def preform_qrng(self):
        for i in range(0, 10):
            print(i)
            self.random_generator()

    def preform_bb84(self):
        key = int(self.bb84(96), base=2)
        print("We got the key: " + hex(key))
        message = int(
            "110110000011110111011100100101101101100000111101110111000000110111011000001111011101110010111011", base=2)
        print("We will use the key to send message: " + hex(message))
        encrypted_message = message ^ key
        print("Encrypted message: " + hex(encrypted_message))
        decrypted_message = encrypted_message ^ key
        print("Eva decrypted and got message: " + hex(decrypted_message))

    def chsh(self):
        sum = 0
        n_games = 1000
        for idx_game in range(n_games):
            you, eve = lambda your_input: 0, lambda eve_input: 0
            your_input, eve_input = random.randint(0, 1), random.randint(0, 1)
            parity = 0 if you(your_input) == eve(eve_input) else 1
            res = parity == (your_input and eve_input)
            sum = sum + res
        return sum / n_games

    def deutsch_oracle(self, type):
        if type == 0:
            return np.kron(self.I, self.I)
        elif type == 1:
            return np.kron(self.I, self.X)
        elif type == 2:
            return self.CNOT
        else:
            return np.kron(self.X, self.I) @ self.CNOT @ np.kron(self.X, self.I)

    def deutsch_alg(self, type):
        x = self.KET_0

        y = self.X @ self.KET_0

        xy = np.kron(self.HADAMARD, self.HADAMARD) @ np.kron(x, y)

        xy = self.deutsch_oracle(type) @ xy

        xy = np.kron(self.HADAMARD, self.I) @ xy

        # дополнительная лекция по измерениям №5
        # считаем матрицу плотности полученного состояния, через внешнее произведение
        rho = np.outer(xy, np.conj(xy))

        # trace - след матрицы, сумма элементов по диагонали
        # np.dot - скалярное произведение

        prob_0 = np.trace(np.kron(self.KET_0 @ np.transpose(self.KET_0), self.I) @ rho)

        return '[0>' if prob_0.round() > 0 else '[1>'

    def perform_deutsch_alg(self):
        print(f"f(x)=0   : {self.deutsch_alg(0)}")
        print(f"f(x)=1   : {self.deutsch_alg(1)}")
        print(f"f(x)=x   : {self.deutsch_alg(2)}")
        print(f"f(x)=!x  : {self.deutsch_alg(3)}")

    def bernstein_vazirani_alg(self, number: str):
        number = list(number)
        n = len(number)

        system = self.KET_0
        hadamard_system = self.HADAMARD

        for i in range(0, n - 1):
            system = np.kron(system, self.KET_0)
            hadamard_system = np.kron(hadamard_system, self.HADAMARD)

        system = np.kron(system, self.X @ self.KET_0)
        result_system = np.kron(hadamard_system, self.HADAMARD) @ system

        oracle = np.eye(2 ** (n + 1))
        for i in range(0, n):
            if number[i] == '1':
                oracle = oracle @ self.build_up_CNOT(i, n)
        result_system = oracle @ result_system

        result_system = np.kron(hadamard_system, self.HADAMARD) @ result_system

        # дополнительная лекция по измерениям №5
        # считаем матрицу плотности полученного состояния, через внешнее произведение
        rho = np.outer(result_system, np.conj(result_system))

        # trace - след матрицы, сумма элементов по диагонали
        # np.dot - скалярное произведение
        message = []
        for i in range(0, n):
            before_cubit = np.eye(2 ** (i)) if i > 0 else 1
            after_cubit = np.eye(2 ** (n - i))
            projector = np.kron(before_cubit, np.kron(self.KET_0 @ np.transpose(self.KET_0), after_cubit))
            prob_0 = np.trace(projector @ rho)
            message.append('0') if prob_0.round() > 0 else message.append('1')

        print(f"The string we got is: {number}")
        print(f"The string we got using the algorithm is: {message}")

    def build_up_CNOT(self, control: int, target: int, reverse=False):

        controlled_proj = self.KET_0 @ np.transpose(self.KET_0)
        target_proj = (self.X @ self.KET_0) @ np.transpose(self.X @ self.KET_0)

        for i in range(control, target - 1):
            controlled_proj = np.kron(controlled_proj, self.I)
            target_proj = np.kron(target_proj, self.I)

        controlled_proj = np.kron(controlled_proj, self.I)
        target_proj = np.kron(target_proj, self.X)

        for i in range(0, control):
            controlled_proj = np.kron(self.I, controlled_proj)
            target_proj = np.kron(self.I, target_proj)

        result = controlled_proj + target_proj
        return result

    def simon(self):
        # Работаем в пространстве размерности n = 3
        # Создаём необходимые регистры
        qc = QuantumSystem([0,0,0])

        # Шаг 2. Применяем гейт Адамара ко всем кубитам первого регистра
        qc.h(range(n))

        # Шаг 3. Применяем U_f
        qc.cx(qr1[0], qr2[0])

        # Шаг 4. Производим измерение второго регистра
        qc.measure(qr2, cr1)

        # Шаг 5. Ещё раз применяем гейт адамара к каждому из кубитов
        qc.h(range(n))

        # Шаг 6. Производим измерение первого регистра
        qc.measure(qr1, cr1)

        # Рисуем схему
        qc.draw()


if __name__ == '__main__':
    my_q_py = MyQPy()
    my_q_py.teleportation()

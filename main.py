import random

import library
from quantum_system import QuantumSystem
import numpy as np

class MyQPy:

    def measure(self, state):
        # pr0 = np.abs(np.transpose(state)@self.KET_0) ** 2
        pr0 = np.abs(state[0, 0]) ** 2
        # print("Measure\npr0: " + str(pr0))
        sample = np.random.random() <= pr0
        # print("sample: " + str(sample))
        return False if sample else True

    def random_generator(self):
        qubit = library.ket_0()
        qubit = library.hadamard() @ qubit
        result = self.measure(qubit)
        # print("random_generator returned " + str(result))
        return result

    def send_single_bit_with_bb84(self):
        my_bit = self.random_generator()
        my_basis = self.random_generator()

        eva_basis = self.random_generator()

        qubit = self.prepare_qubit(my_bit, library.ket_0(), my_basis)

        received_qubit = qubit.copy()

        if eva_basis:
            received_qubit = library.hadamard() @ qubit

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
        shared_system = np.kron(library.ket_0(), library.ket_0())
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
        qc.hadamard([1])
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
        qc.hadamard([1])

        # Шаг 5 - измеряются 2 кубита Алисы, чтобы передать результат Бобу
        res_0 = qc.measure(0)
        res_1 = qc.measure(1)

        # Шаг 6 - применяются гейт X и гейт Z в завиимости от того, какое из измерений дает результат 1.
        if res_0:
            qc.x([2])
        if res_1:
            qc.z([2])

        print(f"Measure system:{[int(qc.measure(i)) for i in range(0, 3)]}")
        # qc.x(qr[2]).c_if(crx, 1)
        # qc.z(qr[2]).c_if(crz, 1)
        # qc.draw()

    def prepare_qubit(self, bit, qubit, basis):
        if bit:
            qubit = library.x() @ qubit
        if basis:
            qubit = library.hadamard() @ qubit
        return qubit

    def bit_from_qubit(self):
        bit = self.random_generator()
        qubit = self.prepare_qubit(bit, library.ket_0(), False)
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
            return np.kron(library.i(), library.i())
        elif type == 1:
            return np.kron(library.i(), library.x())
        elif type == 2:
            return self.CNOT
        else:
            return np.kron(library.x(), library.i()) @ self.CNOT @ np.kron(self.X, library.i())

    def deutsch_alg(self, type):
        x = library.ket_0()

        y = library.ket_1()

        xy = np.kron(library.hadamard(), library.hadamard()) @ np.kron(x, y)

        xy = self.deutsch_oracle(type) @ xy

        xy = np.kron(library.hadamard(), library.i()) @ xy

        # дополнительная лекция по измерениям №5
        # считаем матрицу плотности полученного состояния, через внешнее произведение
        rho = np.outer(xy, np.conj(xy))

        # trace - след матрицы, сумма элементов по диагонали
        # np.dot - скалярное произведение

        prob_0 = np.trace(np.kron(library.projector_0(), library.i()) @ rho)

        return '[0>' if prob_0.round() > 0 else '[1>'

    def perform_deutsch_alg(self):
        print(f"f(x)=0   : {self.deutsch_alg(0)}")
        print(f"f(x)=1   : {self.deutsch_alg(1)}")
        print(f"f(x)=x   : {self.deutsch_alg(2)}")
        print(f"f(x)=!x  : {self.deutsch_alg(3)}")

    def bernstein_vazirani_alg(self, number: str):
        number = list(number)
        n = len(number)

        system = library.ket_0()
        hadamard_system = library.hadamard()

        for i in range(0, n - 1):
            system = np.kron(system, library.ket_0())
            hadamard_system = np.kron(hadamard_system, library.hadamard())

        system = np.kron(system, library.ket_1())
        result_system = np.kron(hadamard_system, library.hadamard()) @ system

        oracle = np.eye(2 ** (n + 1))
        for i in range(0, n):
            if number[i] == '1':
                oracle = oracle @ self.build_up_CNOT(i, n)
        result_system = oracle @ result_system

        result_system = np.kron(hadamard_system, library.hadamard()) @ result_system

        # дополнительная лекция по измерениям №5
        # считаем матрицу плотности полученного состояния, через внешнее произведение
        rho = np.outer(result_system, np.conj(result_system))

        # trace - след матрицы, сумма элементов по диагонали
        # np.dot - скалярное произведение
        message = []
        for i in range(0, n):
            before_cubit = np.eye(2 ** (i)) if i > 0 else 1
            after_cubit = np.eye(2 ** (n - i))
            projector = np.kron(before_cubit, np.kron(library.projector_0(), after_cubit))
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

    def simon(self, n):
        # Работаем в пространстве размерности n = 3
        # Создаём необходимые регистры
        qc = QuantumSystem([0]*2*n)

        # Шаг 2. Применяем гейт Адамара ко всем кубитам первого регистра
        qc.hadamard(range(n))

        # Шаг 3. Применяем U_f
        qc.cnot(0, n)

        # Шаг 4. Производим измерение второго регистра
        print(f"Measure 2nd register:{ [int(qc.measure(i)) for i in range(n, n*2)]}")
        # qc.measure(n)

        # Шаг 5. Ещё раз применяем гейт адамара к каждому из кубитов
        qc.hadamard(range(n))

        # Шаг 6. Производим измерение первого регистра
        # qc.measure(qr1, cr1)
        print(f"Measure 1nd register:{[int(qc.measure(i)) for i in range(0, n)]}")

        # Рисуем схему
        # qc.draw()

if __name__ == '__main__':
    my_q_py = MyQPy()
    my_q_py.simon(3)

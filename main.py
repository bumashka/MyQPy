import numpy as np


class MyQPy:

    def __init__(self):
        self.KET_0 = np.array([[1], [0]], dtype=complex)
        self.HADAMART = np.array([
            [1, 1],
            [1, -1]
        ], dtype=complex) / np.sqrt(2)

        self.X = np.array([
            [0, 1],
            [1, 0]
        ], dtype=complex) / np.sqrt(2)

    def measure(self, state):
        # pr0 = np.abs(np.transpose(state)@self.KET_0) ** 2
        pr0 = np.abs(state[0, 0]) ** 2
        print("Measure\npr0: " + str(pr0))
        sample = np.random.random() <= pr0
        print("sample: " + str(sample))
        return False if sample else True

    def random_generator(self):
        qubit = self.KET_0.copy()
        qubit = self.HADAMART @ qubit
        result = self.measure(qubit)
        print("random_generator returned " + str(result))
        return result

    def send_single_bit_with_bb84(self):
        my_bit = self.random_generator()
        my_basis = self.random_generator()

        eva_basis = self.random_generator()

        qubit = self.prepare_qubit(my_bit, self.KET_0.copy(), my_basis)

        received_qubit = qubit.copy()

        if eva_basis:
            received_qubit = self.HADAMART @ qubit

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
        while number_of_bits>0:
            result = self.send_single_bit_with_bb84()
            if result["my_basis"] == result["eva_basis"]:
                key = ''.join([key, result["result"]])
                number_of_bits -= 1
        print(key)

    def prepare_qubit(self, bit, qubit, basis):
        if bit:
            qubit = self.X @ qubit
        if basis:
            qubit = self.HADAMART @ qubit
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


if __name__ == '__main__':
    my_q_py = MyQPy()
    my_q_py.bb84(10)

import math
import library
import numpy as np

if __name__ == '__main__':
    print("Hello, quantum computer!")
    def preform_qrng():
        for i in range(0, 10):
            print(f"{i}: {library.random_generator()}")

    preform_qrng()





import library

def prepare_qubit(bit, qubit, basis):
    if bit:
        qubit = library.x() @ qubit
    if basis:
        qubit = library.hadamard() @ qubit
    return qubit


def send_single_bit_with_bb84():
    my_bit = library.random_generator()
    my_basis = library.random_generator()

    eva_basis = library.random_generator()

    qubit = prepare_qubit(my_bit, library.ket_0(), my_basis)

    received_qubit = qubit.copy()

    if eva_basis:
        received_qubit = library.hadamard() @ qubit

    result = library.measure(received_qubit)

    return {"result": str(int(result)),
            "my_basis": my_basis,
            "eva_basis": eva_basis
            }


def bb84(number_of_bits):
    key_string = ""
    while number_of_bits > 0:
        result = send_single_bit_with_bb84()
        if result["my_basis"] == result["eva_basis"]:
            key_string = ''.join([key_string, result["result"]])
            number_of_bits -= 1
    return key_string


key = int(bb84(96), base=2)
print("We got the key: " + hex(key))
message = int(
    "110110000011110111011100100101101101100000111101110111000000110111011000001111011101110010111011", base=2)
print("We will use the key to send message: " + hex(message))
encrypted_message = message ^ key
print("Encrypted message: " + hex(encrypted_message))
decrypted_message = encrypted_message ^ key
print("Eva decrypted and got message: " + hex(decrypted_message))

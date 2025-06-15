import itertools
import random
from itertools import permutations, combinations
import numpy as np
import sys

# Define the finite field modulus
mod = 5

# Construct the symmetric group S4
G = list(permutations((1, 2, 3, 4)))  # This generates all 24 permutations of (1,2,3,4)

# Multiplicative inverses in F5 (field with 5 elements)
# For non-zero elements: inverse[x] * x ≡ 1 mod 5
multiplicative_inverse = {
    1: 1,
    2: 3,
    3: 2,
    4: 4
}

# Predefined idempotents e[0] through e[4] (based on the structure of F5[S4])
# These should be assigned appropriately as 24-element vectors over F5.
# Example placeholders (REPLACE with actual values if not already defined):
e = [
    (4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4 , 4) ,
    (4 , 1 , 1 , 4 , 4 , 1 , 1 , 4 , 4 , 1 , 1 , 4 , 4 , 1 , 1 , 4 , 4 , 1 , 1 , 4 , 4 , 1 , 1 , 4) ,
    (1 , 0 , 0 , 2 , 2 , 0 , 0 , 1 , 2 , 0 , 0 , 2 , 2 , 0 , 0 , 2 , 1 , 0 , 0 , 2 , 2 , 0 , 0 , 1) ,
    (1 , 3 , 3 , 0 , 0 , 3 , 3 , 3 , 0 , 2 , 2 , 0 , 0 , 2 , 3 , 0 , 3 , 2 , 2 , 0 , 0 , 3 , 2 , 3) ,
    (1 , 2 , 2 , 0 , 0 , 2 , 2 , 3 , 0 , 3 , 3 , 0 , 0 , 3 , 2 , 0 , 3 , 3 , 3 , 0 , 0 , 2 , 3 , 3) ,
]


def mul(a, b):
    A = np.array(a) - 1
    B = np.array(b) - 1
    C = tuple(B[A] + 1)
    return C

def add(a, b):
    res = [(a[i] + b[i]) % 5 for i in range(len(a))]
    return tuple(res)

def mul_scalar_vector(scalar, vector):
    res = [(scalar * x) % 5 for x in vector]
    return tuple(res)

def mul_inF_5_S_4(a, b):
    res = [0] * len(a)
    for i in range(len(G)):
        for j in range(len(G)):
            if a[i] == 0 or b[j] == 0:
                continue
            elem = mul(G[i], G[j])
            idx = G.index(elem)
            res[idx] = (res[idx] + a[i] * b[j]) % 5
    return tuple(res)

def is_zero_vector(v):
    return all(x == 0 for x in v)

def is_zero_syndrome(syndrome_list):
    return all(is_zero_vector(s_vec) for s_vec in syndrome_list)

def C(i, h):
    x = [0] * len(G)
    x[i] = 1
    return mul_inF_5_S_4(tuple(x), e[h])

def encrypt_char(char_to_encrypt):
    if len(char_to_encrypt) != 1:
        raise ValueError("Input must be a single ASCII character.")
    ascii_val = ord(char_to_encrypt)
    binary_str = format(ascii_val, '08b')
    bits = [int(bit) for bit in binary_str]

    noisy_codewords = []
    for bit_val in bits:
        multiplier = random.choice([1, 3]) if bit_val == 1 else random.choice([2, 4])
        codeword = mul_scalar_vector(multiplier, e[4])
        noisy_word, errors = add_random_errors(codeword, 3)
        noisy_codewords.append(noisy_word)
    return noisy_codewords

def add_random_errors(codeword, num_errors):
    word_list = list(codeword)
    n = len(word_list)
    error_positions = random.sample(range(n), num_errors)
    errors_added = {}
    for pos in error_positions:
        error_value = random.randint(1, 4)
        errors_added[pos] = error_value
        word_list[pos] = (word_list[pos] + error_value) % 5
    return tuple(word_list), errors_added

def decrypt_and_reconstruct_char(noisy_codewords):
    reconstructed_bits = []
    for received_word in noisy_codewords:
        corrected_word = correct_errors(received_word)
        if corrected_word is None:
            reconstructed_bits.append(0)
            continue
        ref_idx = next((j for j, val in enumerate(e[4]) if val != 0), -1)
        if ref_idx == -1:
            reconstructed_bits.append(0)
            continue
        potential_multiplier = (corrected_word[ref_idx] * multiplicative_inverse[e[4][ref_idx]]) % 5
        is_valid_multiple = all((potential_multiplier * e[4][j]) % 5 == corrected_word[j] for j in range(len(corrected_word)))
        if is_valid_multiple:
            parity = 'odd' if potential_multiplier % 2 != 0 else 'even'
            reconstructed_bit = 1 if parity == 'odd' else 0
        else:
            reconstructed_bit = 0
        reconstructed_bits.append(reconstructed_bit)

    binary_str = ''.join(map(str, reconstructed_bits)).zfill(8)
    ascii_val = int(binary_str, 2)
    return chr(ascii_val)

def correct_errors(received_word_input):
    s = [mul_inF_5_S_4(received_word_input, e[h]) for h in range(4)]
    if is_zero_syndrome(s):
        return received_word_input

    n_elements = len(G)
    max_attempts = 5000
    SS_combined_for_check = tuple([item for sublist in s for item in sublist])

    for attempt in range(max_attempts):
        try:
            id0, id1, id2 = random.sample(range(n_elements), 3)
        except ValueError:
            return None

        P, Q, R = [], [], []
        for h in range(4):
            P.extend(C(id0, h))
            Q.extend(C(id1, h))
            R.extend(C(id2, h))
        P, Q, R = tuple(P), tuple(Q), tuple(R)

        for i_mag in range(5):
            for j_mag in range(5):
                for k_mag in range(5):
                    if i_mag == j_mag == k_mag == 0:
                        continue
                    predicted = [(i_mag * P[x] + j_mag * Q[x] + k_mag * R[x]) % 5 for x in range(len(P))]
                    if predicted == list(SS_combined_for_check):
                        corrected_word = list(received_word_input)
                        corrected_word[id0] = (corrected_word[id0] - i_mag) % 5
                        corrected_word[id1] = (corrected_word[id1] - j_mag) % 5
                        corrected_word[id2] = (corrected_word[id2] - k_mag) % 5
                        return tuple(corrected_word)
    return None

if __name__ == "__main__":
    print("\n--- Single Character Encryption/Decryption Test ---")

    # Get character input from the user
    original_char_input = input("Enter a single ASCII character to encrypt: ")

    # Encrypt the character, introducing random errors
    noisy_char_codewords = encrypt_char(original_char_input)

    # Attempt to decrypt the noisy codewords and reconstruct the character
    reconstructed_char_output = decrypt_and_reconstruct_char(noisy_char_codewords)

    # Display the final result and compare original and reconstructed characters
    print("\n=== Test Summary ===")
    print(f"Original Character: '{original_char_input}'")
    print(f"Reconstructed Character: '{reconstructed_char_output}'")

    # Determine and print the test status
    if original_char_input == reconstructed_char_output:
        print("Status: ✅ SUCCESS - The single character was reconstructed correctly.")
    else:
        print("Status: ❌ FAILURE - The single character was NOT reconstructed correctly.")
        print("Note: Failure might occur if random error correction attempts did not find the correct solution or if the error was uncorrectable.")
    print("====================\n")

import os
import time
import numpy as np
import matplotlib.pyplot as plt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

file_sizes = [1, 5, 10, 50]

aes_times = []
rsa_times = []

for size in file_sizes:
    data = os.urandom(size * 1024 * 1024)  # datos aleatorios

    # AES-256 CBC
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher_aes = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    start = time.perf_counter()
    encryptor = cipher_aes.encryptor()
    padded_data = data + b'\x00' * (16 - len(data) % 16)
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    decryptor = cipher_aes.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    end = time.perf_counter()
    aes_times.append(end - start)

    # RSA OAEP
    key_rsa = RSA.generate(2048)
    cipher_rsa = PKCS1_OAEP.new(key_rsa)

    start = time.perf_counter()
    for i in range(0, len(data), 190):
        block = data[i:i+190]
        cipher_rsa.encrypt(block)
    end = time.perf_counter()
    rsa_times.append(end - start)

file_sizes = np.array(file_sizes)
aes_times = np.array(aes_times)
rsa_times = np.array(rsa_times)

# Grafico
plt.figure(figsize=(8,5))
plt.plot(file_sizes, aes_times, marker='o', label='AES-256')
plt.plot(file_sizes, rsa_times, marker='s', label='RSA-2048')
plt.xlabel('Tamaño de archivo (MB)')
plt.ylabel('Tiempo total (s)')
plt.title('Comparación de tiempos de ejecución: AES-256 vs RSA-2048')
plt.yscale('log')  # <- escala logarítmica en Y
plt.grid(True, which="both", ls="--")
plt.legend()
plt.show()


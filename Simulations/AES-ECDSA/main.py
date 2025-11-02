import os
import time
from pathlib import Path
import pandas as pd
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

FILES_DIR = Path("files")
repetitions = 100

file_groups = {
    "PlainText": [("PlainText_1KB.txt", 1024),
                  ("PlainText_488KB.txt", 488_000),
                  ("PlainText_2441KB.txt", 2_441_000),
                  ("PlainText_500MB.txt", 500_000_000)],
    "BinaryDLL": [("Binary_1KB.dll", 1024),
                  ("Binary_488KB.dll", 488_000),
                  ("Binary_2441KB.dll", 2_441_000),
                  ("Binary_500MB.dll", 500_000_000)],
    "ImageJPG": [("Image_720p.jpg", 1280 * 720 // 2),
                 ("Image_1080p.jpg", 1920 * 1080 // 2),
                 ("Image_4k.jpg", 3840 * 2160 // 2)]
}

def apply_padding(data):
    padder = padding.PKCS7(128).padder()
    return padder.update(data) + padder.finalize()

def benchmark_aes(data, key, iv):
    padded_data = apply_padding(data)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    times = []
    for _ in range(repetitions):
        start = time.perf_counter()
        encryptor.update(padded_data)
        end = time.perf_counter()
        times.append(end - start)
    encryptor.finalize()
    return times

def benchmark_ecdsa(data, private_key):
    times = []
    for _ in range(repetitions):
        start = time.perf_counter()
        private_key.sign(data, ec.ECDSA(hashes.SHA256()))
        end = time.perf_counter()
        times.append(end - start)
    return times

aes_key = os.urandom(32)
aes_iv = os.urandom(16)
ecdsa_private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())

summary_results = []
detailed_results = []

for data_type, files in file_groups.items():
    for filename, size in files:
        file_path = FILES_DIR / filename
        if not file_path.exists():
            print(f"Archivo no encontrado: {file_path}")
            continue
        with open(file_path, "rb") as f:
            data = f.read()

        aes_times = benchmark_aes(data, aes_key, aes_iv)
        ecdsa_times = benchmark_ecdsa(data, ecdsa_private_key)

        summary_results.append({
            "Tipo de dato": data_type,
            "Archivo": filename,
            "Tamaño (bytes)": len(data),
            "AES-256 tiempo total (s)": round(sum(aes_times), 6),
            "ECDSA tiempo total (s)": round(sum(ecdsa_times), 6),
            "AES-256 tiempo medio/op": round(sum(aes_times) / repetitions, 8),
            "ECDSA tiempo medio/op": round(sum(ecdsa_times) / repetitions, 8),
        })

        for i in range(repetitions):
            detailed_results.append({
                "Tipo de dato": data_type,
                "Archivo": filename,
                "Tamaño (bytes)": len(data),
                "Repetición": i + 1,
                "AES-256 tiempo (s)": round(aes_times[i], 8),
                "ECDSA tiempo (s)": round(ecdsa_times[i], 8),
            })

summary_df = pd.DataFrame(summary_results)
detailed_df = pd.DataFrame(detailed_results)

summary_df.to_csv("resultados.csv", index=False)
detailed_df.to_csv("resultados_max.csv", index=False)

print("Done")

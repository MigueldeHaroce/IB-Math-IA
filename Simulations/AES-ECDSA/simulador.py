import os
import time
import pandas as pd

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import HKDF

FILES_DIR = "files"
OUTPUT_CSV = "results/raw_results.csv"
REPETITIONS = 1000

def read_file(path):
    with open(path, "rb") as f:
        return f.read()

def aes_encrypt(data, key):
    nonce = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    start = time.perf_counter()
    cipher.encrypt_and_digest(data)
    end = time.perf_counter()
    return end - start

def ecies_encrypt(data, recipient_pubkey):
    eph_key = ECC.generate(curve="P-256")

    shared_point = recipient_pubkey.pointQ * eph_key.d
    shared_secret = int(shared_point.x).to_bytes(32, "big")

    aes_key = HKDF(
        master=shared_secret,
        key_len=32,
        salt=None,
        hashmod=SHA256,
        context=b"ECIES"
    )

    nonce = get_random_bytes(12)
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)

    start = time.perf_counter()
    cipher.encrypt_and_digest(data)
    end = time.perf_counter()

    return end - start


def main():
    os.makedirs("results", exist_ok=True)

    files = os.listdir(FILES_DIR)

    recipient_key = ECC.generate(curve="P-256")
    recipient_pubkey = recipient_key.public_key()

    results = []

    for file in files:
        path = os.path.join(FILES_DIR, file)
        data = read_file(path)
        size_bytes = len(data)

        print(f"Processing {file} ({size_bytes / 1024:.2f} KB)")

        for _ in range(REPETITIONS):
            aes_key = get_random_bytes(32)
            t_aes = aes_encrypt(data, aes_key)

            results.append({
                "file": file,
                "algorithm": "AES-256",
                "size_bytes": size_bytes,
                "time_sec": t_aes
            })

            t_ecies = ecies_encrypt(data, recipient_pubkey)

            results.append({
                "file": file,
                "algorithm": "ECIES",
                "size_bytes": size_bytes,
                "time_sec": t_ecies
            })

    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_CSV, index=False)
    print("Simulation completed. Results saved.")

if __name__ == "__main__":
    main()

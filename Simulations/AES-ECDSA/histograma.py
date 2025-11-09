import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

df = pd.read_csv("resultados.csv")

aes_data_1kb = df[(df["Archivo"] != "AES-256 tiempo (s)") & (df["Archivo"] == "PlainText_1KB.txt")]["ECDSA tiempo (s)"]
aes_data_500mb = df[(df["Archivo"] != "AES-256 tiempo (s)") & (df["Archivo"] == "PlainText_500MB.txt")]["ECDSA tiempo (s)"]

def plot_histogram(data, label, filename):
    log_data = np.log10(data)
    mu, std = log_data.mean(), log_data.std()
    x = np.linspace(mu - 4*std, mu + 4*std, 100)
    pdf = norm.pdf(x, mu, std)

    plt.figure(figsize=(10, 5))
    plt.hist(log_data, bins=30, density=True, alpha=0.6, label=f"log10({label})")
    plt.plot(x, pdf, 'r-', label="Normal curve")
    plt.title(f"Histograma logarítmico + curva normal (ECDSA, {label})")
    ticks = np.round(np.linspace(log_data.min(), log_data.max(), 5), 2)
    plt.xticks(ticks, [f"{10 ** t:.5f}" for t in ticks])
    plt.xlabel("Tiempo (segundos)")
    plt.ylabel("Densidad")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"histograma_log_aes_{filename}.png")

plot_histogram(aes_data_1kb, "PlainText_1KB.txt", "1kb")
plot_histogram(aes_data_500mb, "PlainText_500MB.txt", "500mb")

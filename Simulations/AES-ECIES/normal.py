import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

df = pd.read_csv("results/raw/raw_results.csv")

aes_1kb = df[(df["file"] == "PlainText_1KB.txt") & (df["algorithm"] == "AES-256")]["time_sec"]
ecies_1kb = df[(df["file"] == "PlainText_1KB.txt") & (df["algorithm"] == "ECIES")]["time_sec"]

aes_500mb = df[(df["file"] == "PlainText_500MB.txt") & (df["algorithm"] == "AES-256")]["time_sec"]
ecies_500mb = df[(df["file"] == "PlainText_500MB.txt") & (df["algorithm"] == "ECIES")]["time_sec"]

def plot_comparison(data1, data2, label1, label2, title, filename):
    log1 = np.log10(data1)
    log2 = np.log10(data2)

    mu1, std1 = log1.mean(), log1.std()
    mu2, std2 = log2.mean(), log2.std()

    x1 = np.linspace(mu1 - 4*std1, mu1 + 4*std1, 300)
    x2 = np.linspace(mu2 - 4*std2, mu2 + 4*std2, 300)

    pdf1 = norm.pdf(x1, mu1, std1)
    pdf2 = norm.pdf(x2, mu2, std2)

    plt.figure(figsize=(10, 5))

    plt.hist(log1, bins=30, density=True, alpha=0.5,
             color="steelblue", label=label1)

    plt.hist(log2, bins=30, density=True, alpha=0.5,
             color="orange", label=label2)

    plt.plot(x1, pdf1, color="steelblue", linewidth=2)
    plt.plot(x2, pdf2, color="peru", linewidth=2)

    ticks = np.round(
        np.linspace(min(log1.min(), log2.min()), max(log1.max(), log2.max()), 5),
        2
    )
    plt.xticks(ticks, [f"{10**t:.5f}" for t in ticks])

    plt.xlabel("Tiempo (segundos)")
    plt.ylabel("Densidad")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

plot_comparison(
    aes_1kb,
    ecies_1kb,
    "AES-256 (1 KB)",
    "ECIES (1 KB)",
    "Distribución logarítmica del tiempo de cifrado (1 KB)",
    "histograma_log_1kb_AES_vs_ECIES.png"
)

plot_comparison(
    aes_500mb,
    ecies_500mb,
    "AES-256 (500 MB)",
    "ECIES (500 MB)",
    "Distribución logarítmica del tiempo de cifrado (500 MB)",
    "histograma_log_500mb_AES_vs_ECIES.png"
)

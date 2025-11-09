import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

df = pd.read_csv("resultados.csv")

aes_data_1kb = df[df["Archivo"] == "PlainText_1KB.txt"]["AES-256 tiempo (s)"]
ecdsa_data_1kb = df[df["Archivo"] == "PlainText_1KB.txt"]["ECDSA tiempo (s)"]

aes_data_500mb = df[df["Archivo"] == "PlainText_500MB.txt"]["AES-256 tiempo (s)"]
ecdsa_data_500mb = df[df["Archivo"] == "PlainText_500MB.txt"]["ECDSA tiempo (s)"]

def plot_comparison(aes_data, ecdsa_data, label_file, output_name):
    fig, axs = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

    for ax, data, label in zip(
        axs,
        [aes_data, ecdsa_data],
        ["AES-256", "ECDSA"]
    ):
        log_data = np.log10(data)
        mu, std = log_data.mean(), log_data.std()
        x = np.linspace(mu - 4 * std, mu + 4 * std, 100)
        pdf = norm.pdf(x, mu, std)

        ax.hist(log_data, bins=30, density=True, alpha=0.6, label=f"log10({label})")
        ax.plot(x, pdf, 'r-', label="Normal curve")
        ticks = np.round(np.linspace(log_data.min(), log_data.max(), 5), 2)
        tick_labels = [f"{10**t:.1e}" if 10**t < 0.001 else f"{10**t:.5f}" for t in ticks]
        ax.set_xticks(ticks)
        ax.set_xticklabels(tick_labels)
        ax.set_title(f"{label} - {label_file}")
        ax.set_xlabel("Tiempo (segundos)")
        ax.legend()
        ax.grid(True)

    axs[0].set_ylabel("Densidad")
    plt.tight_layout()
    plt.savefig(f"histograma_comparado_{output_name}.png")  # Guarda localmente
    plt.show()

plot_comparison(aes_data_1kb, ecdsa_data_1kb, "PlainText_1KB.txt", "1kb")
plot_comparison(aes_data_500mb, ecdsa_data_500mb, "PlainText_500MB.txt", "500mb")

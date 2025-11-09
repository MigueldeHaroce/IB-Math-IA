import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv("resultados.csv")

stats = df.melt(
    id_vars=["Tipo de dato", "Archivo", "Tamaño (bytes)", "Repetición"],
    value_vars=["AES-256 tiempo (s)", "ECDSA tiempo (s)"],
    var_name="Protocolo",
    value_name="Tiempo (s)"
)

stats["log10(Tiempo)"] = np.log10(stats["Tiempo (s)"])

plt.figure(figsize=(12, 6))
sns.boxplot(data=stats, x="Protocolo", y="log10(Tiempo)", hue="Tipo de dato")
plt.title("Boxplot logarítmico del tiempo de ejecución (log10 segundos)")
plt.ylabel("log10(Tiempo en segundos)")
plt.grid(True)
plt.tight_layout()
plt.savefig("boxplot_log_tiempos.png")


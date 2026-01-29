import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv("results/raw/raw_results.csv")
#df = df[df["size_bytes"] == 1024]
#print(df)

df["Tipo de dato"] = df["file"].apply(lambda x: x.split("_")[0])
df["Archivo"] = df["file"]
df["Tamaño (bytes)"] = df["size_bytes"]
df["Repetición"] = df.groupby(["file", "algorithm"]).cumcount()

df_pivot = df.pivot_table(
    index=["Tipo de dato", "Archivo", "Tamaño (bytes)", "Repetición"],
    columns="algorithm",
    values="time_sec"
).reset_index()

df_pivot = df_pivot.rename(columns={
    "AES-256": "AES-256 tiempo (s)",
    "ECIES": "ECIES tiempo (s)"
})

stats = df_pivot.melt(
    id_vars=["Tipo de dato", "Archivo", "Tamaño (bytes)", "Repetición"],
    value_vars=["AES-256 tiempo (s)", "ECIES tiempo (s)"],
    var_name="Protocolo",
    value_name="Tiempo (s)"
)

stats["log10(Tiempo)"] = np.log10(stats["Tiempo (s)"])

plt.figure(figsize=(12, 6))
sns.boxplot(
    data=stats,
    x="Protocolo",
    y="log10(Tiempo)",
    hue="Tipo de dato"
)

plt.title("Diagrama de cajas y bigotes logarítmico del tiempo de ejecución 1kb")
plt.ylabel("log10(Tiempo en segundos)")
plt.grid(True)
plt.tight_layout()
plt.savefig("boxplot_log_tiempos.png")
plt.show()

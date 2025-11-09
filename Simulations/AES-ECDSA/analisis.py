import pandas as pd

df = pd.read_csv("resultados.csv")

stats = df.melt(
    id_vars=["Tipo de dato", "Archivo", "Tamaño (bytes)", "Repetición"],
    value_vars=["AES-256 tiempo (s)", "ECDSA tiempo (s)"],
    var_name="Protocolo",
    value_name="Tiempo (s)"
)

grouped = stats.groupby(["Archivo", "Protocolo"])["Tiempo (s)"]
summary = grouped.agg([
    ("media", "mean"),
    ("mediana", "median"),
    ("Desviación estándar", "std"),
    ("Varianza", "var"),
    ("min_time", "min"),
    ("max_time", "max"),
])

summary["coef_variation"] = summary["Desviación estándar"] / summary["media"]
summary.reset_index(inplace=True)

summary.to_csv("analisis_estadistico.csv", index=False)

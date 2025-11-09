import pandas as pd

df = pd.read_csv("resultados.csv")

stats = df.melt(id_vars=["Tipo de dato", "Archivo", "Tamaño (bytes)", "Repetición"],
                value_vars=["AES-256 tiempo (s)", "ECDSA tiempo (s)"],
                var_name="Protocolo", value_name="Tiempo (s)")

summary = stats.groupby(["Tipo de dato", "Archivo", "Protocolo"]).agg(
    media_mean=("Tiempo (s)", "mean"),
    std_dev=("Tiempo (s)", "std"),
    median_val=("Tiempo (s)", "median"),
    var_val=("Tiempo (s)", "var"),
    min_val=("Tiempo (s)", "min"),
    max_val=("Tiempo (s)", "max")
).reset_index()

summary["coef_var"] = summary["std_dev"] / summary["media_mean"]

column = ["Tipo de dato", "Archivo", "max_val", "coef_var"]

filter = summary[column]

filter.to_csv("analisis.csv", index=False)

filter.head()

print(summary)


import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")

for archivo in DATA_DIR.glob("*.csv"):
    df = pd.read_csv(archivo)

    print(f"\n{'=' * 60}")
    print(f"ARCHIVO: {archivo.name}")
    print(f"{'=' * 60}")

    print(f"Filas: {len(df)}")
    print(f"Columnas: {len(df.columns)}")

    print("\nValores nulos:")
    print(df.isnull().sum())

    print("\nFilas duplicadas:")
    print(df.duplicated().sum())

    print("\nTipos de datos:")
    print(df.dtypes)

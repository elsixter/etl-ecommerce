import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")

for archivo in DATA_DIR.glob("*.csv"):
    df = pd.read_csv(archivo)

    print(f"\nArchivo: {archivo.name}")
    print(f"Filas: {len(df)}")
    print(f"Columnas: {len(df.columns)}")
    print(f"Columnas: {list(df.columns)}")

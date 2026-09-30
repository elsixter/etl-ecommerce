import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")

# ============================================================
# 1. ANALISIS GENERAL DE TODOS LOS ARCHIVOS
# ============================================================

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

# ============================================================
# 2. ANALISIS ESPECIFICO DE GEOLOCATION
# ============================================================

print(f"\n{'=' * 60}")
print("ANALISIS ESPECIFICO: GEOLOCATION")
print(f"{'=' * 60}")

geo = pd.read_csv(
    DATA_DIR / "olist_geolocation_dataset.csv"
)

print("\nTotal de filas:")
print(len(geo))

print("\nFilas duplicadas exactas:")
print(geo.duplicated().sum())

# Eliminar únicamente duplicados exactos
geo_limpio = geo.drop_duplicates()

print("\nFilas después de eliminar duplicados:")
print(len(geo_limpio))

print("\nDuplicados restantes:")
print(geo_limpio.duplicated().sum())

print("\nEjemplo de duplicados:")

duplicados = geo[geo.duplicated(keep=False)]

print(
    duplicados
    .sort_values([
        "geolocation_zip_code_prefix",
        "geolocation_lat",
        "geolocation_lng"
    ])
    .head(20)
)

# Guardar datos transformados
geo_limpio.to_csv(
    "data/processed/geolocation_clean.csv",
    index=False
)

print("\nArchivo procesado guardado correctamente.")

# ============================================================
# 3. CONVERSION DE FECHAS
# ============================================================

print(f"\n{'=' * 60}")
print("TRANSFORMACION DE FECHAS - ORDERS")
print(f"{'=' * 60}")

orders = pd.read_csv(
    DATA_DIR / "olist_orders_dataset.csv"
)

columnas_fecha = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for columna in columnas_fecha:
    orders[columna] = pd.to_datetime(
        orders[columna],
        errors="coerce"
    )

print("\nTipos de datos después de la transformación:")

print(orders[columnas_fecha].dtypes)

# ============================================================
# 4. ANALISIS DE VALORES NULOS EN ORDERS
# ============================================================

print(f"\n{'=' * 60}")
print("ANALISIS DE NULOS - ORDERS")
print(f"{'=' * 60}")

print("\nPedidos con fecha de entrega al cliente nula:")
print(
    orders["order_delivered_customer_date"]
    .isnull()
    .sum()
)

print("\nEstado de los pedidos con fecha de entrega nula:")

print(
    orders.loc[
        orders["order_delivered_customer_date"].isnull(),
        "order_status"
    ].value_counts()
)

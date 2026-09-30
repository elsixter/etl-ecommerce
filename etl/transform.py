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

# ============================================================
# 5. ANALISIS DE NULOS - PRODUCTS
# ============================================================

print(f"\n{'=' * 60}")
print("ANALISIS DE NULOS - PRODUCTS")
print(f"{'=' * 60}")

products = pd.read_csv(
    DATA_DIR / "olist_products_dataset.csv"
)

print("\nValores nulos por columna:")

print(
    products.isnull().sum()
)

print("\nPorcentaje de nulos por columna:")

print(
    (products.isnull().mean() * 100).round(2)
)

# ============================================================
# 6. TRANSFORMACION - PRODUCTS
# ============================================================

print(f"\n{'=' * 60}")
print("TRANSFORMACION - PRODUCTS")
print(f"{'=' * 60}")

products_clean = products.rename(
    columns={
        "product_name_lenght": "product_name_length",
        "product_description_lenght": "product_description_length"
    }
)

print("\nColumnas después de la transformación:")
print(list(products_clean.columns))

print("\nValores nulos conservados:")
print(products_clean.isnull().sum())

# Guardar datos transformados
products_clean.to_csv(
    "data/processed/products_clean.csv",
    index=False
)

print("\nArchivo products_clean.csv guardado correctamente.")

# ============================================================
# 7. TRANSFORMACION - ORDERS
# ============================================================

print(f"\n{'=' * 60}")
print("TRANSFORMACION - ORDERS")
print(f"{'=' * 60}")

orders_clean = orders.copy()

orders_clean["order_purchase_year"] = (
    orders_clean["order_purchase_timestamp"].dt.year
)

orders_clean["order_purchase_month"] = (
    orders_clean["order_purchase_timestamp"].dt.month
)

orders_clean["order_purchase_date"] = (
    orders_clean["order_purchase_timestamp"].dt.date
)

print("\nNuevas columnas creadas:")

print(
    orders_clean[
        [
            "order_purchase_timestamp",
            "order_purchase_year",
            "order_purchase_month",
            "order_purchase_date"
        ]
    ].head()
)

# Guardar datos transformados
orders_clean.to_csv(
    "data/processed/orders_clean.csv",
    index=False
)

print("\nArchivo orders_clean.csv guardado correctamente.")

# ============================================================
# 8. ANALISIS - ORDER ITEMS
# ============================================================

print(f"\n{'=' * 60}")
print("ANALISIS - ORDER ITEMS")
print(f"{'=' * 60}")

order_items = pd.read_csv(
    DATA_DIR / "olist_order_items_dataset.csv"
)

print("\nFilas:")
print(len(order_items))

print("\nValores nulos:")
print(order_items.isnull().sum())

print("\nDuplicados exactos:")
print(order_items.duplicated().sum())

print("\nTipos de datos:")
print(order_items.dtypes)

print("\nValores estadísticos:")
print(
    order_items[
        ["price", "freight_value"]
    ].describe()
)

# ============================================================
# 9. TRANSFORMACION - ORDER ITEMS
# ============================================================

print(f"\n{'=' * 60}")
print("TRANSFORMACION - ORDER ITEMS")
print(f"{'=' * 60}")

order_items_clean = order_items.copy()

order_items_clean["shipping_limit_date"] = pd.to_datetime(
    order_items_clean["shipping_limit_date"],
    errors="coerce"
)

order_items_clean["shipping_limit_year"] = (
    order_items_clean["shipping_limit_date"].dt.year
)

order_items_clean["shipping_limit_month"] = (
    order_items_clean["shipping_limit_date"].dt.month
)

print("\nTipos de datos después de la transformación:")

print(
    order_items_clean[
        [
            "shipping_limit_date",
            "shipping_limit_year",
            "shipping_limit_month"
        ]
    ].dtypes
)

print("\nEjemplo de datos transformados:")

print(
    order_items_clean[
        [
            "order_id",
            "product_id",
            "price",
            "freight_value",
            "shipping_limit_date",
            "shipping_limit_year",
            "shipping_limit_month"
        ]
    ].head()
)

# Guardar datos transformados
order_items_clean.to_csv(
    "data/processed/order_items_clean.csv",
    index=False
)

print("\nArchivo order_items_clean.csv guardado correctamente.")

# ============================================================
# 10. ANALISIS - ORDER PAYMENTS
# ============================================================

print(f"\n{'=' * 60}")
print("ANALISIS - ORDER PAYMENTS")
print(f"{'=' * 60}")

payments = pd.read_csv(
    DATA_DIR / "olist_order_payments_dataset.csv"
)

print("\nFilas:")
print(len(payments))

print("\nValores nulos:")
print(payments.isnull().sum())

print("\nDuplicados exactos:")
print(payments.duplicated().sum())

print("\nTipos de datos:")
print(payments.dtypes)

print("\nTipos de pago:")
print(payments["payment_type"].value_counts())

print("\nEstadísticas de payment_value:")
print(payments["payment_value"].describe())

print("\nEstadísticas de payment_installments:")
print(payments["payment_installments"].describe())

# ============================================================
# 11. TRANSFORMACION - ORDER PAYMENTS
# ============================================================

print(f"\n{'=' * 60}")
print("TRANSFORMACION - ORDER PAYMENTS")
print(f"{'=' * 60}")

payments_clean = payments.copy()

payment_type_description = {
    "credit_card": "Tarjeta de crédito",
    "boleto": "Boleto",
    "voucher": "Voucher",
    "debit_card": "Tarjeta de débito",
    "not_defined": "No definido"
}

payments_clean["payment_type_description"] = (
    payments_clean["payment_type"]
    .map(payment_type_description)
)

print("\nEjemplo de datos transformados:")

print(
    payments_clean[
        [
            "order_id",
            "payment_type",
            "payment_type_description",
            "payment_installments",
            "payment_value"
        ]
    ].head()
)

print("\nTipos de pago después de la transformación:")

print(
    payments_clean[
        [
            "payment_type",
            "payment_type_description"
        ]
    ].drop_duplicates()
)

# Guardar datos transformados
payments_clean.to_csv(
    "data/processed/order_payments_clean.csv",
    index=False
)

print("\nArchivo order_payments_clean.csv guardado correctamente.")

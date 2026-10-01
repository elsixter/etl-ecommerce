import pandas as pd
import psycopg2

# ============================================================
# CONEXIÓN A POSTGRESQL
# ============================================================

conn = psycopg2.connect(
    host="localhost",
    port=5435,
    database="ecommerce_dw",
    user="JUAREZ",
    password="sixter007"
)

cursor = conn.cursor()

print("Conexión a PostgreSQL establecida.")
print()


# ============================================================
# DIM_FECHA
# ============================================================

print("=" * 60)
print("CARGANDO DIM_FECHA")
print("=" * 60)

orders = pd.read_csv(
    "data/processed/orders_clean.csv",
    parse_dates=["order_purchase_timestamp"]
)

fechas = orders["order_purchase_timestamp"].dt.date.drop_duplicates()

for fecha in fechas:

    fecha_ts = pd.Timestamp(fecha)

    fecha_key = int(fecha_ts.strftime("%Y%m%d"))
    anio = fecha_ts.year
    mes = fecha_ts.month
    nombre_mes = fecha_ts.strftime("%B")
    trimestre = fecha_ts.quarter
    dia = fecha_ts.day

    cursor.execute(
        """
        INSERT INTO dw.dim_fecha (
            fecha_key,
            fecha,
            anio,
            mes,
            nombre_mes,
            trimestre,
            dia
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (fecha_key) DO NOTHING;
        """,
        (
            fecha_key,
            fecha,
            anio,
            mes,
            nombre_mes,
            trimestre,
            dia
        )
    )

conn.commit()

cursor.execute("SELECT COUNT(*) FROM dw.dim_fecha")
total_fechas = cursor.fetchone()[0]

print(f"Fechas procesadas: {len(fechas)}")
print(f"Fechas en DW: {total_fechas}")
print("Carga de dim_fecha completada.")
print()


# ============================================================
# DIM_CLIENTE
# ============================================================

print("=" * 60)
print("CARGANDO DIM_CLIENTE")
print("=" * 60)

customers = pd.read_csv(
    "data/processed/customers_clean.csv"
)

customers = customers.drop_duplicates(
    subset=["customer_unique_id"]
)

for _, cliente in customers.iterrows():

    cursor.execute(
        """
        INSERT INTO dw.dim_cliente (
            customer_unique_id,
            customer_city,
            customer_state,
            customer_zip_code
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (customer_unique_id) DO NOTHING;
        """,
        (
            cliente["customer_unique_id"],
            cliente["customer_city"],
            cliente["customer_state"],
            cliente["customer_zip_code"]
        )
    )

conn.commit()

cursor.execute("SELECT COUNT(*) FROM dw.dim_cliente")
total_clientes = cursor.fetchone()[0]

print(f"Clientes procesados: {len(customers)}")
print(f"Clientes en DW: {total_clientes}")
print("Carga de dim_cliente completada.")
print()

# ============================================================
# DIM_PRODUCTO
# ============================================================

print("=" * 60)
print("CARGANDO DIM_PRODUCTO")
print("=" * 60)

products = pd.read_csv(
    "data/processed/products_clean.csv"
)

categories = pd.read_csv(
    "data/processed/product_category_translation_clean.csv"
)

# Unir productos con la traducción de categorías
products = products.merge(
    categories,
    left_on="product_category_name",
    right_on="category_name",
    how="left"
)

# El producto debe aparecer una sola vez
products = products.drop_duplicates(
    subset=["product_id"]
)

for _, producto in products.iterrows():

    cursor.execute(
        """
        INSERT INTO dw.dim_producto (
            product_id,
            category_name,
            category_name_english
        )
        VALUES (%s, %s, %s)
        ON CONFLICT (product_id) DO NOTHING;
        """,
        (
            producto["product_id"],
            producto["product_category_name"],
            producto["category_name_english"]
        )
    )

conn.commit()

cursor.execute("SELECT COUNT(*) FROM dw.dim_producto")
total_productos = cursor.fetchone()[0]

print(f"Productos procesados: {len(products)}")
print(f"Productos en DW: {total_productos}")
print("Carga de dim_producto completada.")
print()

# ============================================================
# DIM_VENDEDOR
# ============================================================

print("=" * 60)
print("CARGANDO DIM_VENDEDOR")
print("=" * 60)

sellers = pd.read_csv(
    "data/processed/sellers_clean.csv"
)

sellers = sellers.drop_duplicates(
    subset=["seller_id"]
)

for _, vendedor in sellers.iterrows():

    cursor.execute(
        """
        INSERT INTO dw.dim_vendedor (
            seller_id,
            seller_city,
            seller_state,
            seller_zip_code
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (seller_id) DO NOTHING;
        """,
        (
            vendedor["seller_id"],
            vendedor["seller_city"],
            vendedor["seller_state"],
            vendedor["seller_zip_code"]
        )
    )

conn.commit()

cursor.execute("SELECT COUNT(*) FROM dw.dim_vendedor")
total_vendedores = cursor.fetchone()[0]

print(f"Vendedores procesados: {len(sellers)}")
print(f"Vendedores en DW: {total_vendedores}")
print("Carga de dim_vendedor completada.")
print()

# ============================================================
# FACT_VENTAS
# ============================================================

print("=" * 60)
print("CARGANDO FACT_VENTAS")
print("=" * 60)

order_items = pd.read_csv(
    "data/processed/order_items_clean.csv"
)

orders = pd.read_csv(
    "data/processed/orders_clean.csv",
    parse_dates=["order_purchase_timestamp"]
)

# ------------------------------------------------------------
# Obtener información del cliente y fecha desde las órdenes
# ------------------------------------------------------------

ventas = order_items.merge(
    orders[
        [
            "order_id",
            "customer_id",
            "order_purchase_timestamp"
        ]
    ],
    on="order_id",
    how="inner"
)

print(f"Líneas de venta después del JOIN: {len(ventas)}")

# ------------------------------------------------------------
# Obtener customer_unique_id
# ------------------------------------------------------------

customers = pd.read_csv(
    "data/processed/customers_clean.csv"
)

ventas = ventas.merge(
    customers[
        [
            "customer_id",
            "customer_unique_id"
        ]
    ],
    on="customer_id",
    how="left"
)

# ------------------------------------------------------------
# Obtener las claves del Data Warehouse
# ------------------------------------------------------------

dim_cliente = pd.read_sql(
    """
    SELECT cliente_key, customer_unique_id
    FROM dw.dim_cliente
    """,
    conn
)

dim_producto = pd.read_sql(
    """
    SELECT producto_key, product_id
    FROM dw.dim_producto
    """,
    conn
)

dim_vendedor = pd.read_sql(
    """
    SELECT vendedor_key, seller_id
    FROM dw.dim_vendedor
    """,
    conn
)

# ------------------------------------------------------------
# Unir claves de dimensiones
# ------------------------------------------------------------

ventas = ventas.merge(
    dim_cliente,
    on="customer_unique_id",
    how="left"
)

ventas = ventas.merge(
    dim_producto,
    on="product_id",
    how="left"
)

ventas = ventas.merge(
    dim_vendedor,
    on="seller_id",
    how="left"
)

# ------------------------------------------------------------
# Crear fecha_key
# ------------------------------------------------------------

ventas["fecha"] = ventas[
    "order_purchase_timestamp"
].dt.date

dim_fecha = pd.read_sql(
    """
    SELECT fecha_key, fecha
    FROM dw.dim_fecha
    """,
    conn
)

ventas = ventas.merge(
    dim_fecha,
    on="fecha",
    how="left"
)

# ------------------------------------------------------------
# Validar claves
# ------------------------------------------------------------

print(
    "Filas sin cliente:",
    ventas["cliente_key"].isna().sum()
)

print(
    "Filas sin producto:",
    ventas["producto_key"].isna().sum()
)

print(
    "Filas sin vendedor:",
    ventas["vendedor_key"].isna().sum()
)

print(
    "Filas sin fecha:",
    ventas["fecha_key"].isna().sum()
)

# ------------------------------------------------------------
# Insertar fact_ventas
# ------------------------------------------------------------

for _, venta in ventas.iterrows():

    cursor.execute(
        """
        INSERT INTO dw.fact_ventas (
            order_id,
            order_item_id,
            cliente_key,
            producto_key,
            vendedor_key,
            fecha_key,
            price,
            freight_value
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (order_id, order_item_id) DO NOTHING;
        """,
        (
            venta["order_id"],
            int(venta["order_item_id"]),
            int(venta["cliente_key"]),
            int(venta["producto_key"]),
            int(venta["vendedor_key"]),
            int(venta["fecha_key"]),
            venta["price"],
            venta["freight_value"]
        )
    )

conn.commit()

cursor.execute(
    "SELECT COUNT(*) FROM dw.fact_ventas"
)

total_ventas = cursor.fetchone()[0]

print(f"Filas procesadas: {len(ventas)}")
print(f"Ventas en DW: {total_ventas}")
print("Carga de fact_ventas completada.")
print()


# ============================================================
# CERRAR CONEXIÓN
# ============================================================

cursor.close()
conn.close()

print("=" * 60)
print("ETL DE DIMENSIONES COMPLETADO")
print("=" * 60)

-- ============================================================
-- DATA WAREHOUSE - E-COMMERCE OLIST
-- Script de creación del esquema dimensional
-- ============================================================

-- ============================================================
-- 1. CREAR ESQUEMA
-- ============================================================

CREATE SCHEMA IF NOT EXISTS dw;

-- ============================================================
-- 2. DIMENSIÓN FECHA
-- ============================================================

CREATE TABLE IF NOT EXISTS dw.dim_fecha (
fecha_key INTEGER PRIMARY KEY,
fecha DATE NOT NULL,
anio INTEGER NOT NULL,
mes INTEGER NOT NULL,
nombre_mes VARCHAR(20) NOT NULL,
trimestre INTEGER NOT NULL,
dia INTEGER NOT NULL
);

-- ============================================================
-- 3. DIMENSIÓN CLIENTE
-- ============================================================

CREATE TABLE IF NOT EXISTS dw.dim_cliente (
cliente_key SERIAL PRIMARY KEY,
customer_unique_id VARCHAR(50) NOT NULL UNIQUE,
customer_city VARCHAR(100),
customer_state VARCHAR(10),
customer_zip_code INTEGER
);

-- ============================================================
-- 4. DIMENSIÓN PRODUCTO
-- ============================================================

CREATE TABLE IF NOT EXISTS dw.dim_producto (
producto_key SERIAL PRIMARY KEY,
product_id VARCHAR(50) NOT NULL UNIQUE,
category_name VARCHAR(100),
category_name_english VARCHAR(100)
);

-- ============================================================
-- 5. DIMENSIÓN VENDEDOR
-- ============================================================

CREATE TABLE IF NOT EXISTS dw.dim_vendedor (
vendedor_key SERIAL PRIMARY KEY,
seller_id VARCHAR(50) NOT NULL UNIQUE,
seller_city VARCHAR(100),
seller_state VARCHAR(10),
seller_zip_code INTEGER
);

-- ============================================================
-- 6. TABLA DE HECHOS: VENTAS
-- ============================================================

CREATE TABLE IF NOT EXISTS dw.fact_ventas (
venta_key BIGSERIAL PRIMARY KEY,

order_id VARCHAR(50) NOT NULL,
order_item_id INTEGER NOT NULL,

cliente_key INTEGER NOT NULL,
producto_key INTEGER NOT NULL,
vendedor_key INTEGER NOT NULL,
fecha_key INTEGER NOT NULL,

price NUMERIC(12,2) NOT NULL,
freight_value NUMERIC(12,2) NOT NULL,

CONSTRAINT fk_fact_cliente
    FOREIGN KEY (cliente_key)
    REFERENCES dw.dim_cliente(cliente_key),

CONSTRAINT fk_fact_producto
    FOREIGN KEY (producto_key)
    REFERENCES dw.dim_producto(producto_key),

CONSTRAINT fk_fact_vendedor
    FOREIGN KEY (vendedor_key)
    REFERENCES dw.dim_vendedor(vendedor_key),

CONSTRAINT fk_fact_fecha
    FOREIGN KEY (fecha_key)
    REFERENCES dw.dim_fecha(fecha_key),

CONSTRAINT uq_fact_venta
    UNIQUE (order_id, order_item_id)

);

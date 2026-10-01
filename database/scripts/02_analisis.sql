-- ============================================================
-- ANÁLISIS DEL DATA WAREHOUSE
-- Proyecto: ETL E-Commerce Olist
-- ============================================================


-- ============================================================
-- 1. VENTAS MENSUALES
-- ============================================================

SELECT
    f.anio,
    f.mes,
    f.nombre_mes,
    COUNT(*) AS cantidad_ventas,
    SUM(v.price) AS ventas_totales,
    SUM(v.freight_value) AS flete_total
FROM dw.fact_ventas v
JOIN dw.dim_fecha f
    ON v.fecha_key = f.fecha_key
GROUP BY
    f.anio,
    f.mes,
    f.nombre_mes
ORDER BY
    f.anio,
    f.mes;


-- ============================================================
-- 2. VENTAS POR CATEGORÍA
-- ============================================================

SELECT
    p.category_name_english AS categoria,
    COUNT(*) AS cantidad_ventas,
    SUM(v.price) AS ventas_totales,
    ROUND(AVG(v.price), 2) AS precio_promedio
FROM dw.fact_ventas v
JOIN dw.dim_producto p
    ON v.producto_key = p.producto_key
GROUP BY
    p.category_name_english
ORDER BY
    ventas_totales DESC;


-- ============================================================
-- 3. VENTAS POR VENDEDOR
-- ============================================================

SELECT
    v.seller_id AS vendedor,
    v.seller_city AS ciudad,
    v.seller_state AS estado,
    COUNT(*) AS cantidad_ventas,
    SUM(f.price) AS ventas_totales,
    ROUND(AVG(f.price), 2) AS venta_promedio
FROM dw.fact_ventas f
JOIN dw.dim_vendedor v
    ON f.vendedor_key = v.vendedor_key
GROUP BY
    v.seller_id,
    v.seller_city,
    v.seller_state
ORDER BY
    ventas_totales DESC;


-- ============================================================
-- 4. VENTAS POR CLIENTE
-- ============================================================

SELECT
    c.cliente_key AS cliente,
    c.customer_city AS ciudad,
    c.customer_state AS estado,
    COUNT(DISTINCT f.order_id) AS cantidad_ordenes,
    COUNT(*) AS cantidad_productos,
    SUM(f.price) AS gasto_total,
    ROUND(
        SUM(f.price) / COUNT(DISTINCT f.order_id),
        2
    ) AS gasto_promedio_por_orden
FROM dw.fact_ventas f
JOIN dw.dim_cliente c
    ON f.cliente_key = c.cliente_key
GROUP BY
    c.cliente_key,
    c.customer_city,
    c.customer_state
ORDER BY
    gasto_total DESC;


-- ============================================================
-- 5. VENTAS POR PRODUCTO
-- ============================================================

SELECT
    p.product_id AS producto,
    p.category_name_english AS categoria,
    COUNT(*) AS cantidad_vendida,
    SUM(f.price) AS ventas_totales,
    ROUND(AVG(f.price), 2) AS precio_promedio
FROM dw.fact_ventas f
JOIN dw.dim_producto p
    ON f.producto_key = p.producto_key
GROUP BY
    p.product_id,
    p.category_name_english
ORDER BY
    ventas_totales DESC;


-- ============================================================
-- 6. VENTAS POR ESTADO
-- ============================================================

SELECT
    c.customer_state AS estado,
    COUNT(*) AS cantidad_ventas,
    SUM(f.price) AS ventas_totales
FROM dw.fact_ventas f
JOIN dw.dim_cliente c
    ON f.cliente_key = c.cliente_key
GROUP BY
    c.customer_state
ORDER BY
    ventas_totales DESC;


-- ============================================================
-- 7. PRODUCTOS MÁS VENDIDOS
-- ============================================================

SELECT
    p.product_id AS producto,
    p.category_name_english AS categoria,
    COUNT(*) AS cantidad_vendida,
    SUM(f.price) AS ventas_totales
FROM dw.fact_ventas f
JOIN dw.dim_producto p
    ON f.producto_key = p.producto_key
GROUP BY
    p.product_id,
    p.category_name_english
ORDER BY
    cantidad_vendida DESC
LIMIT 10;


-- ============================================================
-- 8. VENDEDORES CON MAYOR VENTA PROMEDIO
-- ============================================================

SELECT
    v.seller_id AS vendedor,
    COUNT(*) AS cantidad_ventas,
    SUM(f.price) AS ventas_totales,
    ROUND(
        SUM(f.price) / COUNT(*),
        2
    ) AS venta_promedio
FROM dw.fact_ventas f
JOIN dw.dim_vendedor v
    ON f.vendedor_key = v.vendedor_key
GROUP BY
    v.seller_id
HAVING COUNT(*) >= 100
ORDER BY
    venta_promedio DESC
LIMIT 10;

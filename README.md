# ETL E-Commerce Data Warehouse

Proyecto de ingeniería de datos basado en el Brazilian E-Commerce Public Dataset de Olist.

El proyecto implementa un proceso ETL utilizando Python y Pandas para extraer, transformar y cargar información comercial en un Data Warehouse desarrollado en PostgreSQL.

## Arquitectura

```text
CSV originales
      |
      v
   EXTRACT
      |
      v
  TRANSFORM
      |
      v
     LOAD
      |
      v
PostgreSQL
      |
      v
Data Warehouse
      |
      v
Análisis SQL
```

## Tecnologías

* Python
* Pandas
* PostgreSQL
* SQL
* ETL
* Data Warehouse
* Git / GitHub

## Estructura del proyecto

etl-ecommerce/
├── data/
│   ├── raw/                  # Datos originales CSV
│   └── processed/            # Datos transformados
│
├── etl/
│   ├── extract.py           
│   ├── transform.py          
│   ├── load.py               
│   └── pipeline.py           
│
├── database/
│   └── scripts/
│       ├── 01_dw_schema.sql  
│       ├── 02_analisis.sql   
│       └── 03_views.sql      
│
├── notebooks/
├── requirements.txt
├── README.md
└── .gitignore

## Proceso ETL

### 1. Extract

`extract.py` identifica y lee los archivos CSV originales utilizando Pandas.

Durante esta etapa se revisa:

* Número de filas.
* Número de columnas.
* Nombres de columnas.
* Archivos disponibles.

### 2. Transform

`transform.py` realiza procesos de limpieza y validación sobre los diferentes datasets.

Entre las transformaciones realizadas se encuentran:

* Análisis de valores nulos.
* Detección de duplicados.
* Conversión de tipos de datos.
* Transformación de fechas.
* Limpieza de nombres de columnas.
* Eliminación de duplicados en geolocalización.
* Clasificación de reseñas.
* Traducción de categorías.
* Generación de archivos procesados.

Los datos originales se mantienen separados de los datos procesados.

### 3. Load

`load.py` carga la información transformada en PostgreSQL.

El Data Warehouse utiliza un modelo dimensional tipo estrella.

## Data Warehouse

El proyecto utiliza un modelo dimensional tipo estrella.

### Tablas de dimensiones

- `dw.dim_fecha`
- `dw.dim_cliente`
- `dw.dim_producto`
- `dw.dim_vendedor`

### Tabla de hechos

- `dw.fact_ventas`

La granularidad de `fact_ventas` es una línea de producto dentro de una orden.

### Vistas analíticas

- `dw.vw_ventas_mensuales`
- `dw.vw_ventas_categoria`
- `dw.vw_ventas_vendedor`
- `dw.vw_ventas_cliente`
- `dw.vw_ventas_producto`

## Orden de ejecución

Para ejecutar el proyecto desde cero se recomienda seguir el siguiente orden.

### 1. Crear el esquema del Data Warehouse

```bash
psql -U JUAREZ -h localhost -p 5435 -d ecommerce_dw -f database/scripts/01_dw_schema.sql
```

Este script crea el esquema `dw`, las dimensiones y la tabla de hechos.

### 2. Ejecutar el pipeline ETL

Desde la raíz del proyecto:

```bash
python etl/pipeline.py
```

El pipeline ejecuta automáticamente:

1. Extracción de los archivos CSV.
2. Transformación y limpieza de los datos.
3. Carga de las dimensiones y la tabla de hechos.

### 3. Crear las vistas analíticas

```bash
psql -U JUAREZ -h localhost -p 5435 -d ecommerce_dw -f database/scripts/03_views.sql
```

Este script crea las vistas utilizadas para facilitar las consultas y análisis del Data Warehouse.

### 4. Ejecutar análisis SQL

Las consultas analíticas se encuentran en:

```text
database/scripts/02_analisis.sql
```

Estas consultas permiten analizar las ventas por periodo, categoría, vendedor, cliente, producto y estado.

### Flujo general

```text
01_dw_schema.sql
        ↓
   pipeline.py
        ↓
03_views.sql
        ↓
02_analisis.sql
```

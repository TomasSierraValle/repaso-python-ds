# Práctica de SQL - Analista de Datos

## Descripción
Segundo ejercicio del curso de Analista de Datos, orientado a la extracción, filtrado y análisis de datos mediante consultas SQL.

Se utiliza SQLite desde Python en Google Colab para crear una tabla de ventas tecnológicas y realizar consultas sobre los datos.

## Objetivos
- Consultar productos y precios mediante `SELECT`.
- Filtrar ventas por país y precio utilizando `WHERE`.
- Identificar registros con valores nulos mediante `IS NULL`.
- Calcular ingresos por categoría utilizando `SUM()` y `GROUP BY`.
- Filtrar categorías según sus ingresos totales mediante `HAVING`.
- Ordenar resultados alfabéticamente con `ORDER BY`.

## Tecnologías utilizadas
- Python 3
- Google Colab
- SQLite (`sqlite3`)
- Pandas

## Estructura del proyecto
- `practica_sql_ventas.ipynb`: notebook con la creación de la tabla, los datos de ejemplo y las consultas SQL.

## Datos utilizados
Se crea una tabla llamada `ventas_tecnologia` con las siguientes columnas:
- `id_venta`: identificador de la venta.
- `producto`: nombre del producto.
- `categoria`: categoría del producto.
- `precio_unitario`: precio por unidad.
- `cantidad`: unidades vendidas.
- `fecha`: fecha de la venta.
- `pais`: país donde se realizó la venta.

Los registros utilizados son ficticios y se emplean exclusivamente para practicar las consultas SQL.

## Consultas realizadas
1. Selección de productos y precios ordenados alfabéticamente.
2. Filtrado de ventas de Colombia con precios superiores a 500.
3. Identificación de ventas sin categoría asignada.
4. Cálculo de ingresos totales por categoría.
5. Selección de categorías con ingresos superiores a 10.000.


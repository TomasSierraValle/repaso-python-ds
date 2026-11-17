# Pre-entrega: Adquisición y Normalización con Pandas

## Objetivo
Integrar datos de ventas provenientes de dos fuentes con formatos diferentes:
- `data/transacciones.csv`: transacciones con ID de producto, cantidad y fecha.
- `data/catalogo_productos.xlsx`: catálogo de productos con nombre y precio unitario.

El proceso normaliza tipos, trata valores nulos, realiza un `merge`, calcula `total_venta` y exporta el resultado a Parquet.

## Estructura del repositorio

```text
pre-entrega-pandas/
├── data/
│   ├── transacciones.csv
│   └── catalogo_productos.xlsx
├── output/
│   └── ventas_normalizadas.parquet
├── main.py
├── requirements.txt
└── README.md
```

## Requisitos
- Python 3.10 o superior
- pandas
- numpy
- openpyxl
- pyarrow

## Instalación

Crear y activar un entorno virtual (opcional, recomendado):

```bash
python -m venv .venv
```

En Windows:

```bash
.venv\Scripts\activate
```

En macOS/Linux:

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

Desde la carpeta raíz del proyecto:

```bash
python main.py
```

El archivo `output/ventas_normalizadas.parquet` se genera automáticamente.

## Decisiones de limpieza y normalización
1. Se leen los archivos con `read_csv` y `read_excel`.
2. `id_producto` se convierte a tipo entero nullable (`Int64`) en ambas fuentes para asegurar una llave compatible.
3. `cantidad` y `precio_unitario` se convierten a valores numéricos.
4. `fecha` se convierte a `datetime` mediante `pd.to_datetime`.
5. Se eliminan filas con datos críticos nulos o inválidos.
6. Se descartan cantidades no positivas y precios negativos.
7. Se eliminan IDs duplicados del catálogo para garantizar una relación muchos-a-uno.
8. Se usa `merge(..., how="inner", validate="many_to_one")`: solo quedan transacciones cuyo producto existe en el catálogo.
9. Se calcula `total_venta = cantidad * precio_unitario`.
10. Se valida que los campos críticos no tengan nulos antes de exportar.

## Lectura del archivo Parquet

```python
import pandas as pd

df = pd.read_parquet("output/ventas_normalizadas.parquet")
print(df.head())
print(df.dtypes)
```

## Fuentes de ejemplo
Los archivos incluidos son datos ficticios creados exclusivamente para demostrar el flujo de adquisición, integración y normalización.

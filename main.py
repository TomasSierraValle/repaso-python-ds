"""
Pre-entrega: Adquisición y Normalización con Pandas
Carga transacciones CSV y catálogo XLSX, valida, integra y exporta a Parquet.
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

def main():
    # 1. Adquisición desde dos fuentes y formatos diferentes
    transacciones = pd.read_csv(DATA_DIR / "transacciones.csv")
    productos = pd.read_excel(DATA_DIR / "catalogo_productos.xlsx", engine="openpyxl")

    # 2. Normalización de tipos
    transacciones["id_producto"] = pd.to_numeric(
        transacciones["id_producto"], errors="coerce"
    ).astype("Int64")
    productos["id_producto"] = pd.to_numeric(
        productos["id_producto"], errors="coerce"
    ).astype("Int64")

    transacciones["cantidad"] = pd.to_numeric(
        transacciones["cantidad"], errors="coerce"
    )
    transacciones["fecha"] = pd.to_datetime(
        transacciones["fecha"], errors="coerce"
    )
    productos["precio_unitario"] = pd.to_numeric(
        productos["precio_unitario"], errors="coerce"
    )

    # 3. Tratamiento de nulos en campos críticos.
    # Se eliminan registros sin ID, cantidad, fecha o precio válido.
    transacciones = transacciones.dropna(
        subset=["id_producto", "cantidad", "fecha"]
    )
    productos = productos.dropna(
        subset=["id_producto", "nombre_producto", "precio_unitario"]
    )

    # Validaciones de dominio para evitar cantidades/precios no válidos.
    transacciones = transacciones[transacciones["cantidad"] > 0]
    productos = productos[productos["precio_unitario"] >= 0]

    # Evitar duplicados en el catálogo: un ID debe identificar un producto.
    productos = productos.drop_duplicates(subset=["id_producto"], keep="last")

    # 4. Integración: conservar solo transacciones con producto existente.
    dataset_final = transacciones.merge(
        productos,
        on="id_producto",
        how="inner",
        validate="many_to_one"
    )

    # 5. Columna calculada
    dataset_final["total_venta"] = (
        dataset_final["cantidad"] * dataset_final["precio_unitario"]
    )

    # Orden y control final
    dataset_final = dataset_final[
        ["id_producto", "nombre_producto", "cantidad",
         "fecha", "precio_unitario", "total_venta"]
    ].sort_values(["fecha", "id_producto"]).reset_index(drop=True)

    campos_criticos = [
        "id_producto", "nombre_producto", "cantidad",
        "fecha", "precio_unitario", "total_venta"
    ]
    if dataset_final[campos_criticos].isna().any().any():
        raise ValueError("El dataset final contiene nulos en campos críticos.")
    if dataset_final.empty:
        raise ValueError("El dataset final quedó vacío. Revisá los archivos fuente.")

    # 6. Exportación a Parquet
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ruta_salida = OUTPUT_DIR / "ventas_normalizadas.parquet"
    dataset_final.to_parquet(ruta_salida, index=False, engine="pyarrow")

    print("Proceso finalizado correctamente.")
    print(f"Filas integradas: {len(dataset_final)}")
    print(f"Ventas totales: ${dataset_final['total_venta'].sum():,.2f}")
    print(f"Archivo generado: {ruta_salida}")

if __name__ == "__main__":
    main()

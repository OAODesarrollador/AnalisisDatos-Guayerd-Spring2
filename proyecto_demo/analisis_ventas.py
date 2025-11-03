"""
Análisis de Ventas — Demo Sincrónica (Python)
Autor: Oscar Ortiz Dev Studio™
Requisitos: pandas, numpy, matplotlib
Ejecución:
    python analisis_ventas.py
    o
    python analisis_ventas.py "ruta/a/tu/carpeta/data"
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# ========================= CONFIGURACIÓN DE RUTAS =========================
BASE = os.path.dirname(__file__)
DATA = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(BASE, "..", "data"))

OUT = os.path.join(BASE, "proyecto_demo2")
PLOTS = os.path.join(OUT, "plots")
TABLES = os.path.join(OUT, "tablas")
os.makedirs(PLOTS, exist_ok=True)
os.makedirs(TABLES, exist_ok=True)

# Verificación rápida de existencia de archivos
print("📂 Buscando archivos en:", DATA)
for f in ["clientes99.csv", "productos99.csv", "ventas99.csv", "detalle_ventas99.csv"]:
    path = os.path.join(DATA, f)
    print(f"   {f} → {'✅ encontrado' if os.path.exists(path) else '❌ no encontrado'}")
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró el archivo requerido: {path}")

# ========================= CARGA DE DATOS =========================
clientes = pd.read_csv(os.path.join(DATA, "clientes99.csv"))
productos = pd.read_csv(os.path.join(DATA, "productos99.csv"))
ventas = pd.read_csv(os.path.join(DATA, "ventas99.csv"), sep=";")
detalle = pd.read_csv(os.path.join(DATA, "detalle_ventas99.csv"))

# ========================= LIMPIEZA Y TIPIFICACIÓN =========================
ventas["fecha"] = pd.to_datetime(ventas["fecha"], errors="coerce")

for c in ["cantidad", "precio_unitario", "importe"]:
    if c in detalle.columns:
        detalle[c] = pd.to_numeric(detalle[c], errors="coerce")

if "precio_unitario" in productos.columns:
    productos["precio_unitario"] = pd.to_numeric(productos["precio_unitario"], errors="coerce")

# --- 🔧 NORMALIZAR TIPOS DE CLAVES PARA MERGE SEGURO ---
for df in [detalle, productos, ventas, clientes]:
    for col in df.columns:
        if "id" in col:
            df[col] = df[col].astype(str).str.strip()

# ========================= INTEGRACIÓN DE TABLAS =========================
df = detalle.merge(productos, on="id_producto", how="left", suffixes=("", "_prod"))
df = df.merge(ventas, on="id_venta", how="left")
if "id_cliente" in clientes.columns:
    df = df.merge(clientes[["id_cliente", "ciudad"]], on="id_cliente", how="left")

# ========================= VARIABLES DERIVADAS =========================
if {"cantidad", "precio_unitario"}.issubset(df.columns):
    df["subtotal_calc"] = df["cantidad"] * df["precio_unitario"]
if {"importe", "subtotal_calc"}.issubset(df.columns):
    df["desvio_importe"] = df["importe"] - df["subtotal_calc"]

ticket = (
    df.groupby("id_venta")
      .agg(
          fecha=("fecha", "first"),
          id_cliente=("id_cliente", "first"),
          medio_pago=("medio_pago", "first"),
          items=("cantidad", "sum"),
          total=("importe", "sum")
      )
      .reset_index()
)

# ========================= VISUALIZACIONES =========================
plt.figure()
ticket["total"].plot(kind="hist", bins=20, title="Distribución del total por ticket")
plt.xlabel("Total por ticket")
plt.savefig(os.path.join(PLOTS, "hist_total_ticket.png"), bbox_inches="tight")
plt.close()

plt.figure()
df.boxplot(column="importe", by="categoria")
plt.title("Boxplot de importe por categoría")
plt.suptitle("")
plt.savefig(os.path.join(PLOTS, "box_importe_categoria.png"), bbox_inches="tight")
plt.close()

plt.figure()
plt.scatter(df["cantidad"], df["precio_unitario"])
plt.title("Relación cantidad vs. precio unitario")
plt.xlabel("Cantidad")
plt.ylabel("Precio unitario")
plt.savefig(os.path.join(PLOTS, "scatter_cantidad_precio.png"), bbox_inches="tight")
plt.close()

cat_summary = df.groupby("categoria")["importe"].sum().sort_values(ascending=False)
plt.figure()
cat_summary.plot(kind="bar", title="Ingresos por categoría")
plt.ylabel("Ingresos")
plt.savefig(os.path.join(PLOTS, "bar_ingresos_categoria.png"), bbox_inches="tight")
plt.close()

# ========================= TABLAS Y REPORTES =========================
df[["cantidad", "precio_unitario", "importe"]].describe().T.to_csv(os.path.join(TABLES, "desc_detalle.csv"))
ticket[["items", "total"]].describe().T.to_csv(os.path.join(TABLES, "desc_ticket.csv"))
cat_summary.to_csv(os.path.join(TABLES, "resumen_categoria.csv"))
ticket.to_csv(os.path.join(TABLES, "tickets.csv"), index=False)

print("✅ Análisis finalizado.")
print("📊 Resultados guardados en:", OUT)

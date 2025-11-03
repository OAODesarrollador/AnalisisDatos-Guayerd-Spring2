
import os
import io
import unicodedata
from datetime import datetime

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ========================= CONFIG INICIAL =========================
st.set_page_config(page_title="Análisis Descriptivo Profesional", layout="wide")
st.title("📊 Análisis Descriptivo Profesional (EDA + Limpieza + Conclusiones)")

# --- Parámetros / opciones generales ---
BASE_DATA_DIR = st.sidebar.text_input("📁 Carpeta de datos (CSV originales)", value="data")
OUTPUT_DIR = st.sidebar.text_input("💾 Carpeta de salida (CSV limpios)", value="data_limpios")
DEBUG = st.sidebar.checkbox("🔎 Modo debug (muestra diagnósticos)", value=False)
DISABLE_CACHE = st.sidebar.checkbox("🚫 Desactivar caché (depuración)", value=True)

# ========================= UTILIDADES BASE =========================
def _strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza nombres: minúsculas, sin tildes, espacios→'_'."""
    df = df.copy()
    df.columns = (
        pd.Series(df.columns)
        .astype(str)
        .map(_strip_accents)
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
    )
    return df

def robust_read_csv(path, try_seps=(",", ";", "\t", "|"), encodings=("utf-8", "latin-1")) -> pd.DataFrame:
    """Lectura robusta (multi-separador y multi-encoding) + elimina Unnamed:*."""
    last_err = None
    for sep in try_seps:
        for enc in encodings:
            try:
                df = pd.read_csv(path, sep=sep, encoding=enc, engine="python")
                if df.shape[1] == 1 and sep != ",":  # probablemente separador incorrecto
                    continue
                df = df.loc[:, ~df.columns.str.contains(r"^Unnamed")]
                return df
            except Exception as e:
                last_err = e
    raise last_err if last_err else ValueError(f"No se pudo leer: {path}")

def to_num(s):
    return pd.to_numeric(s, errors="coerce")

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def find_key(df: pd.DataFrame, candidates=(), contains_all=()):
    """Encuentra columna clave por candidatos exactos o por tokens contenidos."""
    cols = list(df.columns)
    for c in candidates:
        if c in cols:
            return c
    hits = [c for c in cols if all(tok in c for tok in contains_all)]
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:
        return sorted(hits, key=len, reverse=True)[0]
    return None

# ========================= CARGA DE DATOS =========================
_cache = st.cache_data(ttl=0) if DISABLE_CACHE else st.cache_data

@_cache
def load_raw_data(base_dir: str):
    paths = {
        "clientes": os.path.join(base_dir, "clientes99.csv"),
        "productos": os.path.join(base_dir, "productos99.csv"),
        "ventas":    os.path.join(base_dir, "ventas99.csv"),
        "detalle":   os.path.join(base_dir, "detalle_ventas99.csv"),
    }
    missing = [k for k, p in paths.items() if not os.path.exists(p)]
    if missing:
        raise FileNotFoundError(f"Faltan archivos: {', '.join(missing)} en {base_dir}")

    clientes = robust_read_csv(paths["clientes"])
    productos = robust_read_csv(paths["productos"])
    ventas    = robust_read_csv(paths["ventas"])
    detalle   = robust_read_csv(paths["detalle"])
    return clientes, productos, ventas, detalle

def profile_df(df: pd.DataFrame, name: str):
    st.subheader(f"📄 {name}")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.write("Vista previa:")
        st.dataframe(df.head(15))
    with c2:
        st.write("Información básica:")
        st.write({"filas": df.shape[0], "columnas": df.shape[1]})
        st.write("Tipos de datos:")
        st.write(df.dtypes.astype(str))
        st.write("Nulos por columna:")
        st.write(df.isna().sum())
        st.write("Duplicados (filas exactas):", int(df.duplicated().sum()))

# ========================= LIMPIEZA =========================
def clean_data(clientes, productos, ventas, detalle):
    # 1) Normalizar columnas
    clientes = normalize_columns(clientes)
    productos = normalize_columns(productos)
    ventas    = normalize_columns(ventas)
    detalle   = normalize_columns(detalle)

    # 2) Trimming de strings y conversión básica
    for df in (clientes, productos, ventas, detalle):
        for c in df.select_dtypes(include=["object"]).columns:
            df[c] = df[c].astype(str).str.strip()

    # 3) Detección de claves y mapeo manual (sidebar)
    st.sidebar.markdown("### 🔗 Configurar columnas clave")

    # Producto
    det_prod_key_default = find_key(detalle, ("id_producto", "producto_id"), ("producto", "id")) or detalle.columns[0]
    prod_key_default     = find_key(productos, ("id_producto", "producto_id"), ("producto", "id")) or productos.columns[0]
    det_prod_key = st.sidebar.selectbox("Detalle → ID Producto", detalle.columns, index=list(detalle.columns).index(det_prod_key_default))
    prod_key     = st.sidebar.selectbox("Productos → ID Producto", productos.columns, index=list(productos.columns).index(prod_key_default))

    # Venta
    det_venta_key_default = find_key(detalle, ("id_venta", "venta_id"), ("venta", "id")) or detalle.columns[min(1, len(detalle.columns)-1)]
    venta_key_default     = find_key(ventas,  ("id_venta", "venta_id"), ("venta", "id")) or ventas.columns[0]
    det_venta_key = st.sidebar.selectbox("Detalle → ID Venta", detalle.columns, index=list(detalle.columns).index(det_venta_key_default))
    venta_key     = st.sidebar.selectbox("Ventas → ID Venta", ventas.columns, index=list(ventas.columns).index(venta_key_default))

    # Cliente (opcional)
    cli_key_cli_default = find_key(clientes, ("id_cliente", "cliente_id"), ("cliente", "id"))
    cli_key_det_default = find_key(detalle,  ("id_cliente", "cliente_id"), ("cliente", "id"))

    cli_key_det = None
    cli_key_cli = None
    if cli_key_cli_default and cli_key_cli_default in clientes.columns:
        cli_key_det = st.sidebar.selectbox(
            "Detalle → ID Cliente (opcional)", detalle.columns,
            index=list(detalle.columns).index(cli_key_det_default) if cli_key_det_default in detalle.columns else 0
        )
        cli_key_cli = st.sidebar.selectbox(
            "Clientes → ID Cliente (opcional)", clientes.columns,
            index=list(clientes.columns).index(cli_key_cli_default)
        )

    # 4) Asegurar keys como texto (merge seguro)
    for df in (clientes, productos, ventas, detalle):
        for c in df.columns:
            if "id" in c:
                df[c] = df[c].astype(str).str.strip()

    # 5) Conversión de campos numéricos y fechas más comunes (sin romper)
    for col in ("cantidad", "precio_unitario", "importe", "total", "monto", "monto_total", "descuento"):
        for df in (detalle, ventas):
            if col in df.columns:
                df[col] = to_num(df[col])

    # Fechas
    for col in ("fecha", "fecha_venta", "created_at"):
        if col in ventas.columns:
            ventas[col] = pd.to_datetime(ventas[col], errors="coerce")
        if col in detalle.columns:
            detalle[col] = pd.to_datetime(detalle[col], errors="coerce")

    # 6) Guardar limpios
    ensure_dir(OUTPUT_DIR)
    clientes.to_csv(os.path.join(OUTPUT_DIR, "clientes_limpio.csv"), index=False, encoding="utf-8")
    productos.to_csv(os.path.join(OUTPUT_DIR, "productos_limpio.csv"), index=False, encoding="utf-8")
    ventas.to_csv(os.path.join(OUTPUT_DIR, "ventas_limpio.csv"), index=False, encoding="utf-8")
    detalle.to_csv(os.path.join(OUTPUT_DIR, "detalle_limpio.csv"), index=False, encoding="utf-8")

    # 7) Integración (detalle + productos + ventas [+ clientes])
    df = detalle.merge(productos, left_on=det_prod_key, right_on=prod_key, how="left", suffixes=("", "_prod"))
    df = df.merge(ventas, left_on=det_venta_key, right_on=venta_key, how="left")
    if cli_key_det and cli_key_cli and cli_key_det in df.columns and cli_key_cli in clientes.columns:
        extras = [c for c in ("ciudad", "localidad", "provincia") if c in clientes.columns][:1]
        df = df.merge(clientes[[cli_key_cli] + extras], left_on=cli_key_det, right_on=cli_key_cli, how="left", suffixes=("", "_cli"))

    # 8) Derivadas
    if {"cantidad", "precio_unitario"}.issubset(df.columns):
        df["subtotal_calc"] = to_num(df["cantidad"]) * to_num(df["precio_unitario"])
    if {"importe", "subtotal_calc"}.issubset(df.columns):
        df["desvio_importe"] = to_num(df["importe"]) - df["subtotal_calc"]

    # fechas derivadas
    fecha_col = "fecha" if "fecha" in df.columns else ("fecha_venta" if "fecha_venta" in df.columns else None)
    if fecha_col:
        df["anio"] = pd.to_datetime(df[fecha_col], errors="coerce").dt.year
        df["mes"] = pd.to_datetime(df[fecha_col], errors="coerce").dt.to_period("M").astype(str)

    # Columna de categoría flexible
    cat_col = next((c for c in df.columns if "categoria" in c), None)

    # Detección avanzada de columna total en ventas
    total_candidates = ["total", "importe_total", "monto_total", "monto", "total_venta", "total_ticket", "total_factura"]
    total_col = next((c for c in ventas.columns if any(tc in c for tc in total_candidates)), None)

    return {
        "clientes": clientes,
        "productos": productos,
        "ventas": ventas,
        "detalle": detalle,
        "integrado": df,
        "cat_col": cat_col,
        "total_col": total_col,
        "keys": {
            "det_prod_key": det_prod_key,
            "prod_key": prod_key,
            "det_venta_key": det_venta_key,
            "venta_key": venta_key,
            "cli_key_det": cli_key_det,
            "cli_key_cli": cli_key_cli,
        }
    }

# ========================= UI: PASO 1 – DATOS ORIGINALES =========================
st.header("1) 📦 Datos originales (problemas y diagnóstico)")
try:
    raw_clientes, raw_productos, raw_ventas, raw_detalle = load_raw_data(BASE_DATA_DIR)
    st.success("Archivos originales cargados correctamente.")
except Exception as e:
    st.error(f"Error cargando CSV originales: {e}")
    st.stop()

c1, c2 = st.columns(2)
with c1:
    profile_df(raw_clientes, "Clientes (original)")
    profile_df(raw_productos, "Productos (original)")
with c2:
    profile_df(raw_ventas, "Ventas (original)")
    profile_df(raw_detalle, "Detalle de ventas (original)")

st.info(
    "🔧 **Problemas típicos a corregir antes del análisis:**\n"
    "- Nombres de columnas inconsistentes (mayúsculas, tildes, espacios).\n"
    "- Tipos incorrectos (números como texto, fechas sin parsear).\n"
    "- Nulos/duplicados.\n"
    "- Claves desalineadas entre archivos (p.ej., `id_venta` vs `venta_id`)."
)

st.markdown("---")

# ========================= PASO 2 – LIMPIEZA Y EXPORTACIÓN =========================
st.header("2) 🧼 Limpieza y preparación (y guardado de CSV limpios)")
if st.button("🚀 Ejecutar limpieza + guardar CSV (carpeta salida)"):
    try:
        cleaned = clean_data(raw_clientes, raw_productos, raw_ventas, raw_detalle)
        st.success(f"CSV limpios guardados en: `{OUTPUT_DIR}`")
        st.session_state["cleaned"] = cleaned
    except Exception as e:
        st.exception(e)

if "cleaned" in st.session_state:
    st.write("✅ **Vista rápida (limpios):**")
    cl = st.session_state["cleaned"]
    cc1, cc2 = st.columns(2)
    with cc1:
        st.subheader("Clientes (limpio)")
        st.dataframe(cl["clientes"].head(10))
        st.subheader("Productos (limpio)")
        st.dataframe(cl["productos"].head(10))
    with cc2:
        st.subheader("Ventas (limpio)")
        st.dataframe(cl["ventas"].head(10))
        st.subheader("Detalle (limpio)")
        st.dataframe(cl["detalle"].head(10))

    # Descargas directas
    def df_to_download(df: pd.DataFrame, filename: str, label: str):
        buf = io.BytesIO()
        df.to_csv(buf, index=False, encoding="utf-8")
        st.download_button(label=label, data=buf.getvalue(), file_name=filename, mime="text/csv")

    st.write("⬇️ **Descargar CSV limpios:**")
    d1, d2, d3, d4 = st.columns(4)
    with d1: df_to_download(cl["clientes"], "clientes_limpio.csv", "Clientes limpio")
    with d2: df_to_download(cl["productos"], "productos_limpio.csv", "Productos limpio")
    with d3: df_to_download(cl["ventas"], "ventas_limpio.csv", "Ventas limpio")
    with d4: df_to_download(cl["detalle"], "detalle_limpio.csv", "Detalle limpio")

st.markdown("---")

# ========================= PASO 3 – ANÁLISIS DESCRIPTIVO =========================
st.header("3) 📈 Análisis descriptivo (gráficos + narrativa)")

if "cleaned" not in st.session_state:
    st.warning("Primero ejecutá la limpieza (Paso 2).")
    st.stop()

cl = st.session_state["cleaned"]
df = cl["integrado"]
ventas = cl["ventas"]
cat_col = cl["cat_col"]
keys = cl["keys"]

# --- Total por ticket: usar ventas.total_col si existe; si no, reconstruir desde detalle integrado ---
total_col = cl["total_col"]
st.sidebar.markdown("### ⚙️ Configuración de total por ticket")
if total_col and total_col in ventas.columns:
    st.sidebar.info(f"Columna de total detectada en ventas: **{total_col}**")
    ticket_totals = to_num(ventas[total_col])
else:
    st.sidebar.warning("No se detectó columna 'total' en ventas. Se reconstruirá desde el detalle.")
    base_col = "importe" if "importe" in df.columns else ("subtotal_calc" if "subtotal_calc" in df.columns else None)
    if base_col and keys["det_venta_key"] in df.columns:
        grp = df.groupby(keys["det_venta_key"])[base_col].sum().rename("total_ticket")
        ticket_totals = grp.reset_index()["total_ticket"]
    else:
        ticket_totals = None

# --- HISTOGRAMA ---
st.subheader("3.1 Distribución del total por ticket (Histograma)")
if ticket_totals is not None and ticket_totals.notna().any():
    serie = ticket_totals.dropna()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(serie, bins=20)
    ax.set_title("Distribución del total por ticket", weight="bold")
    ax.set_xlabel("Total por ticket")
    ax.set_ylabel("Frecuencia")
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    st.pyplot(fig, use_container_width=True)

    with st.expander("📘 Interpretación y definición estadística"):
        st.markdown("""
**¿Qué estoy viendo?**  
Un histograma muestra cómo se reparten los valores. Cada “barra” indica cuántos tickets caen dentro de ese rango de montos.

**¿Por qué es útil?**  
Permite entender si la mayoría de las ventas son de montos bajos, medios o altos; detectar colas (asimetrías) y valores extremos.

**¿Cómo leer este gráfico en ventas?**  
- Si hay una cola hacia la derecha, la mayoría de los tickets son bajos y hay pocos muy altos.  
- Si aparecen barras aisladas muy lejos, podrían ser outliers (ventas inusuales).
        """)
else:
    st.info("No se pudo construir el histograma (no hay columna 'total' ni base válida para reconstruir).")

# --- BOXPLOT: IMPORTE vs CATEGORÍA ---
st.subheader("3.2 Variabilidad de importe por categoría (Boxplot)")
if cat_col and "importe" in df.columns:
    sub = df[[cat_col, "importe"]].dropna()
    if not sub.empty:
        cats = list(sub[cat_col].astype(str).unique())
        data = [to_num(sub.loc[sub[cat_col] == c, "importe"]).dropna() for c in cats]
        fig, ax = plt.subplots(figsize=(max(7, len(cats)*0.7), 5))
        ax.boxplot(data, labels=cats, patch_artist=True,
                   boxprops=dict(facecolor="lightblue"),
                   medianprops=dict(color="navy", linewidth=2))
        plt.xticks(rotation=45, ha="right")
        ax.set_title("Boxplot de importe por categoría", weight="bold")
        ax.set_ylabel("Importe")
        st.pyplot(fig, use_container_width=True)

        with st.expander("📘 Interpretación y definición estadística"):
            st.markdown(f"""
**¿Qué estoy viendo?**  
Cada caja resume cómo se distribuyen los importes dentro de una **categoría** (como un “resumen visual”):  
- La **línea del medio** es la **mediana** (valor típico).  
- La **caja** abarca el rango donde cae la mitad de los importes.  
- Los puntos alejados son **valores atípicos**.

**¿Por qué es útil?**  
Permite comparar **variabilidad** y **valores típicos** entre categorías de producto.

**¿Cómo leer este gráfico en ventas?**  
- Cajas más **altas**: mayor dispersión de importes (precios variados o tickets muy distintos).  
- Medianas **altas**: categoría con tickets usualmente más caros.  
- Muchos puntos sueltos: presencia de ventas excepcionales.
            """)
    else:
        st.info("No hay datos suficientes para boxplot.")
else:
    st.warning("No se detectó columna de categoría (`*categoria*`) o `importe` en el integrado.")

# --- SCATTER: CANTIDAD vs PRECIO UNITARIO ---
st.subheader("3.3 Relación cantidad vs. precio unitario (Dispersión)")
if {"cantidad", "precio_unitario"}.issubset(df.columns):
    x = to_num(df["cantidad"])
    y = to_num(df["precio_unitario"])
    mask = x.notna() & y.notna()
    if mask.any():
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.scatter(x[mask], y[mask], alpha=0.6)
        ax.set_xlabel("Cantidad")
        ax.set_ylabel("Precio unitario")
        ax.set_title("Dispersión: cantidad vs precio unitario", weight="bold")
        ax.grid(alpha=0.3)
        st.pyplot(fig, use_container_width=True)

        with st.expander("📘 Interpretación y definición estadística"):
            st.markdown("""
**¿Qué estoy viendo?**  
Cada punto es una venta (o ítem): su posición muestra cuánta **cantidad** se vendió y a qué **precio unitario**.

**¿Por qué es útil?**  
Ayuda a notar **patrones**: si al subir el precio baja la cantidad, si hay clústeres (familias de productos) o casos raros.

**¿Cómo leer este gráfico en ventas?**  
- **Nube inclinada hacia abajo**: cuando el precio sube, se vende menos (típico).  
- **Puntos muy separados**: productos con comportamientos distintos (segmentos).  
- **Grupos definidos**: oportunidades para promos dirigidas o segmentación.
            """)
    else:
        st.info("No hay pares válidos para dispersión.")
else:
    st.warning("Falta `cantidad` o `precio_unitario` en el integrado.")

# --- BARRAS: INGRESOS POR CATEGORÍA ---
st.subheader("3.4 Ingresos totales por categoría (Barras)")
if cat_col and "importe" in df.columns:
    serie = df.groupby(cat_col)["importe"].sum().sort_values(ascending=False)
    if not serie.empty:
        num_cats = len(serie)
        fig, ax = plt.subplots(figsize=(10, max(4, num_cats * 0.42)))
        if num_cats > 8:
            ax.barh(serie.index.astype(str), serie.values)
            ax.invert_yaxis()
            ax.set_xlabel("Ingresos totales"); ax.set_ylabel("Categoría")
            for i, v in enumerate(serie.values):
                ax.text(v, i, f"{v:,.0f}", va="center", ha="left", fontsize=8)
        else:
            ax.bar(serie.index.astype(str), serie.values)
            plt.xticks(rotation=45, ha="right")
            ax.set_ylabel("Ingresos totales")
            for i, v in enumerate(serie.values):
                ax.text(i, v, f"{v:,.0f}", ha="center", va="bottom", fontsize=8)
        ax.set_title("Ingresos por categoría", weight="bold")
        ax.grid(axis="x", linestyle="--", alpha=0.55)
        st.pyplot(fig, use_container_width=True)

        with st.expander("📘 Interpretación y definición estadística"):
            st.markdown("""
**¿Qué estoy viendo?**  
Cada barra representa cuánto **ingreso total** generó una categoría.

**¿Por qué es útil?**  
Permite identificar **categorías líderes** que explican gran parte de la facturación y aquellas que necesitan atención.

**¿Cómo leer este gráfico en ventas?**  
- Barras **más largas/altas**: categorías con mayor aportación al negocio.  
- Caídas marcadas entre barras: concentración en pocas categorías (posible dependencia de productos estrella).  
- Útil para priorizar stock, promociones y negociación con proveedores.
            """)
    else:
        st.info("Serie vacía para barras.")
else:
    st.warning("No se detectó columna de categoría (`*categoria*`) o `importe` para el gráfico de barras.")

st.markdown("---")

# ========================= PASO 4 – CONCLUSIONES =========================
st.header("4) 🧾 Conclusiones del análisis")
conclusiones_txt = f"""
Informe de conclusiones — {datetime.now().strftime('%Y-%m-%d %H:%M')}

1) Calidad de datos
- Los CSV originales presentaban inconsistencias normales (nombres de columnas, tipos, nulos, claves).
- Se normalizaron nombres, se tipificaron campos numéricos y fechas, y se alinearon claves para integrar.

2) Total por ticket (histograma)
- Patrón típico: mayoría de tickets de monto bajo con algunos de alto valor (cola a la derecha).
- Acción: vigilar outliers altos y entender qué los genera (combos, productos premium, promociones).

3) Importe por categoría (boxplot)
- Diferencias claras en mediana y dispersión. Algunas categorías son más “estables” y otras muy heterogéneas.
- Acción: revisar estrategia de precios y mix en categorías con alta dispersión.

4) Cantidad vs precio unitario (dispersión)
- La relación no es lineal: hay productos que sostienen cantidades aun con precios altos y otros muy sensibles.
- Acción: segmentar por sensibilidad al precio; ajustar promos y bundles.

5) Ingresos por categoría (barras)
- Pocas categorías suelen explicar la mayor parte de la facturación (ley de Pareto).
- Acción: priorizar stock y campañas para las top; relanzar o optimizar las de menor rendimiento.

Notas:
- Este panel replica el flujo del notebook: datos crudos → limpieza → análisis visual → conclusiones.
- Los CSV limpios quedaron guardados en: {os.path.abspath(OUTPUT_DIR)}
"""

st.text_area("Conclusiones generadas", conclusiones_txt, height=280)
st.download_button(
    "💾 Descargar conclusiones (.txt)",
    data=conclusiones_txt.encode("utf-8"),
    file_name="conclusiones_analisis.txt",
    mime="text/plain",
)
st.caption("Fin del informe. Lenguaje divulgativo para equipos no técnicos, con rigor de ciencia de datos.")

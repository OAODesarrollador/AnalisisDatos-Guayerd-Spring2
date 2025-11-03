
# 🧠 Análisis de Ventas — EDA + Streamlit + Ciencia de Datos Aplicada  

![Banner](https://img.shields.io/badge/EDA-DataScience-blue?style=for-the-badge) 
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow?style=for-the-badge&logo=python) 
![Pandas](https://img.shields.io/badge/Pandas-DataFrame-green?style=for-the-badge&logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualización-lightgrey?style=for-the-badge&logo=plotly)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit)

---

### 🚀 Proyecto profesional de Análisis Exploratorio de Datos (EDA)  
**Autor:** Oscar Ortiz Dev Studio™  
**Lenguaje:** Python  
**Frameworks:** Streamlit, Pandas, Matplotlib, NumPy  
**Objetivo:** desarrollar un flujo de trabajo completo de limpieza, análisis estadístico y visualización descriptiva a partir de datos reales de ventas, clientes y productos.

---

## 🎯 Objetivo General
El propósito de este proyecto es **demostrar un proceso profesional de Ciencia de Datos aplicada al análisis comercial**, integrando las etapas de:  
- Carga y limpieza de datos.  
- Preparación de un dataset analítico integrado.  
- Análisis exploratorio y estadístico descriptivo.  
- Visualizaciones explicativas y narrativa interpretativa.  
- Conclusiones orientadas a la toma de decisiones.

---

## ⚙️ Arquitectura del Proyecto

```
Clientes.csv      Productos.csv
     │                  │
     │                  ▼
     │          ┌───────────────┐
     │          │ Preprocesamiento │
     │          └───────────────┘
     │                  │
     ▼                  ▼
Ventas.csv ───────────▶ Detalle_Ventas.csv
          │
          ▼
 Integración (Fact Table) → Limpieza → EDA → Visualizaciones → Conclusiones
```

---

## 💡 Principales Características

✅ **EDA completo y reproducible** — implementado tanto en Jupyter Notebook como en una App Streamlit interactiva.  
✅ **Detección automática de separadores y encoding** (archivos CSV robustos).  
✅ **Tipificación y normalización** de datos (fechas, numéricos, categorías).  
✅ **Validación de integridad** mediante cálculo de `subtotal_calc` y `desvio_importe`.  
✅ **Integración relacional** entre clientes, ventas, productos y detalle de ventas.  
✅ **Análisis estadístico descriptivo** (media, mediana, moda, desviación, cuartiles).  
✅ **Visualizaciones profesionales** (histograma, boxplot, scatter, barras comparativas).  
✅ **Narrativa explicativa** en lenguaje divulgativo pero con rigor académico.  
✅ **Descarga automática** de CSV limpios y reporte final en Streamlit.

---

## 📊 Visualizaciones destacadas

| Tipo de gráfico | Propósito | Ejemplo |
|-----------------|------------|----------|
| **Histograma** | Distribución del total por ticket | ![Histograma](proyecto_demo2/plots/hist_total_ticket.png) |
| **Boxplot** | Dispersión e outliers por categoría | ![Boxplot](proyecto_demo2/plots/box_importe_categoria.png) |
| **Scatterplot** | Relación cantidad–precio unitario | ![Scatter](proyecto_demo2/plots/scatter_cantidad_precio.png) |
| **Barras** | Ingresos por categoría | ![Barras](proyecto_demo2/plots/bar_ingresos_categoria.png) |

---

## 🧮 Resultados del Análisis

- **Patrón de Pareto (80/20):** unas pocas categorías concentran la mayoría de ingresos.  
- **Outliers identificados:** valores extremos explicables por ventas especiales o errores.  
- **Dispersión elevada:** heterogeneidad entre categorías → oportunidad de optimizar precios.  
- **Correlaciones positivas:** coherencia entre cantidad e importe total.  
- **Desvíos detectados:** indicador útil para control de calidad del proceso de ventas.

> 💬 *Conclusión metodológica:*  
> Este proyecto constituye un **ejemplo integral de EDA profesional** — reproducible, documentado y defendible en una presentación técnica o académica.

---

## 🧩 Estructura del Repositorio

```
📦 AnalisisVentas
 ┣ 📂 data/                ← Archivos CSV originales
 ┣ 📂 proyecto_demo2/
 ┃ ┣ 📂 plots/             ← Gráficos generados (PNG)
 ┃ ┣ 📂 tablas/            ← Tablas descriptivas (CSV)
 ┃ ┣ 📜 analisis_completo_demo2.ipynb
 ┃ ┣ 📜 documentacion_proyecto.md
 ┃ ┣ 📜 analisis_ventas.py
 ┃ ┗ 📜 resumen_demo.pptx
 ┣ 📜 app.py               ← App Streamlit interactiva
 ┣ 📜 README.md            ← Este documento
 ┗ 📜 requirements.txt     ← Dependencias del entorno
```

---

## 🧭 Ejecución del Proyecto

### 🧪 Opción 1 — Notebook interactivo
```bash
jupyter notebook analisis_completo_demo2.ipynb
```

### 🌐 Opción 2 — App Streamlit interactiva
```bash
streamlit run app.py
```

La app permite:
- Cargar los archivos CSV.  
- Ver diagnóstico de calidad de datos.  
- Aplicar limpieza y exportar los datasets limpios.  
- Generar gráficos descriptivos con interpretación automática.  
- Descargar reportes y conclusiones finales.

---

## 📘 Capturas de la App (Streamlit)

| Paso | Descripción | Vista |
|------|--------------|-------|
| 1️⃣ | Diagnóstico de datos originales | ![Step1](https://imgur.com/placeholder1.png) |
| 2️⃣ | Limpieza automática y exportación | ![Step2](https://imgur.com/placeholder2.png) |
| 3️⃣ | Análisis descriptivo y gráficos | ![Step3](https://imgur.com/placeholder3.png) |
| 4️⃣ | Conclusiones finales descargables | ![Step4](https://imgur.com/placeholder4.png) |

> 🔧 *Las imágenes pueden personalizarse con capturas reales de tu entorno Streamlit.*

---

## 🧠 Conclusión Final

El proyecto combina **ciencia de datos aplicada, estadística descriptiva avanzada y visualización moderna**, demostrando competencias profesionales en:  
- Limpieza y preprocesamiento de datos reales.  
- Interpretación estadística y análisis exploratorio.  
- Comunicación visual de resultados mediante herramientas interactivas.

> 💼 Ideal para portfolio profesional, docencia o presentaciones académicas.

---

## 👨‍💻 Autor

**Oscar Ortiz Dev Studio™**  
Desarrollador Full‑Stack & Científico de Datos  
📍 Argentina | 🌐 [LinkedIn](https://www.linkedin.com/in/oscar-alejandro-ortiz-desarrollador-fullstack/)  
💬 *Innovación, análisis y visualización aplicada a proyectos reales.*

---



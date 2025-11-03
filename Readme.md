# 🧠 Análisis Descriptivo Profesional – Tienda Saludable / Dataset Demo

![Python](https://img.shields.io/badge/Python-3.9→3.12-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Estado-En%20Desarrollo%20Activo-success)
![License](https://img.shields.io/badge/Licencia-MIT-lightgrey)
![DataScience](https://img.shields.io/badge/Disciplina-Ciencia%20de%20Datos-orange?logo=anaconda)

---

## 🌍 Descripción General

Este proyecto transforma un **análisis exploratorio de datos (EDA)** clásico —originalmente en un notebook Jupyter— en una **aplicación interactiva e intuitiva** construida con **Streamlit**.  
El objetivo es mostrar cómo un flujo de análisis profesional puede ser presentado de forma **clara, visual y comprensible incluso para públicos no técnicos**, manteniendo el rigor estadístico.

> 🎯 **Objetivo:** Convertir el proceso de limpieza, exploración y análisis descriptivo de datos en una experiencia visual, educativa y dinámica, donde cada gráfico cuenta una historia.

---

## 🧩 Características principales

### 🟦 1. Carga de datos crudos
- Lectura **robusta** de múltiples archivos CSV con detección automática de separadores y codificación (`utf-8`, `latin-1`).
- Diagnóstico inicial con conteo de nulos, duplicados y tipos de datos.
- Presentación visual tipo “panel de control”.

### 🟨 2. Limpieza y normalización automática
- Estandarización de nombres de columnas (sin tildes, espacios o mayúsculas).
- Conversión automática de tipos (numéricos, fechas, strings).
- Corrección de claves entre tablas (`id_venta`, `id_producto`, `id_cliente`).
- Exportación de CSVs **limpios** en carpeta `data_limpios/`.

### 🟩 3. Análisis descriptivo visual (EDA)
Cuatro visualizaciones principales con interpretación explicativa desplegable:
1. **Histograma** — Distribución del total por ticket.  
2. **Boxplot** — Variabilidad de importe por categoría.  
3. **Scatterplot** — Relación cantidad vs precio unitario.  
4. **Gráfico de barras** — Ingresos totales por categoría.

Cada gráfico incluye un panel “📘 Ver interpretación”, que explica con lenguaje **divulgativo** qué representa, por qué se usa y cómo se interpreta.

### 🟥 4. Conclusiones automáticas
- Generación automática de **conclusiones interpretadas**, redactadas con lenguaje profesional pero accesible.
- Descarga directa del informe en formato `.txt`.

---

## 💡 Filosofía del proyecto

> “La estadística no solo describe el mundo: **lo hace visible.**  
> Esta aplicación busca que cada persona —sin importar su formación— pueda entender qué le están diciendo sus datos.”

Diseñado como una herramienta de **alfabetización de datos (data literacy)** para PyMEs, estudiantes, y analistas que comienzan en el campo.

---

## ⚙️ Instalación y ejecución

### 🔧 Requisitos
- Python 3.9 o superior (probado hasta 3.12)
- pip actualizado

### 📦 Instalación

```bash
git clone https://github.com/OAODesarrollador/analisis-descriptivo-streamlit.git
cd analisis-descriptivo-streamlit
pip install -r requirements.txt
```

### 🚀 Ejecución local

```bash
streamlit run app.py
```

Luego abrir [http://localhost:8501](http://localhost:8501) en tu navegador.

---

## ☁️ Deploy en Streamlit Cloud

1. Subí este repositorio a tu GitHub.  
2. Iniciá sesión en [streamlit.io](https://streamlit.io/cloud).  
3. Elegí **New app → GitHub repo → `main` branch → app.py**.  
4. Aceptá las dependencias de `requirements.txt`.  
5. ¡Listo! Tu análisis estará disponible online con URL pública.

---

## 🧮 Estructura del proyecto

```
📦 analisis-descriptivo-streamlit/
 ┣ 📂 data/                 → CSV originales
 ┣ 📂 data_limpios/         → CSV generados tras limpieza
 ┣ 📄 app.py                → Aplicación principal (Streamlit)
 ┣ 📄 requirements.txt      → Dependencias del entorno
 ┣ 📄 README.md             → Este archivo
 ┗ 📜 conclusiones_analisis.txt  → Informe descargable (opcional)
```

---

## 🎨 Estilo visual y UX
- Diseño minimalista y adaptable.
- Gráficos interactivos con narrativa expandible.
- Colores suaves, tipografía profesional.
- Presentación paso a paso: **Datos → Limpieza → Análisis → Conclusiones**.

---

## 🧠 Conocimientos y herramientas aplicadas

| Área | Competencia | Herramientas |
|------|--------------|--------------|
| Estadística descriptiva | Distribuciones, asimetría, dispersión, outliers | Pandas, NumPy |
| Visualización de datos | Análisis visual interpretativo | Matplotlib |
| Limpieza y preparación | Normalización, parsing de fechas, tipificación | Pandas |
| Presentación interactiva | UI científica, storytelling visual | Streamlit |
| Documentación | Comunicación técnica + lenguaje divulgativo | Markdown |

---

## 🪄 Ejemplo visual

```
Distribución del total por ticket
┌───────────────────────────────┐
│   📘 Ver interpretación ▼     │
│   Este gráfico muestra cómo…  │
└───────────────────────────────┘
```

*(cada gráfico incluye un expander con explicación divulgativa)*

---

## 🧾 Créditos

**Desarrollado por:**  
👨‍💻 **Oscar Alejandro Ortiz - Dev Studio™**  
Desarrollador Full Stack | Científico de Datos | Educador Técnico  

🔗 [LinkedIn](https://www.linkedin.com/in/oscar-alejandro-ortiz-desarrollador-fullstack)  
💼 [GitHub](https://github.com/OAODesarrollador)  
📬 [WhatsApp](https://wa.me/543704054127)

> 💬 “Los datos cuentan historias; tu trabajo es darles voz.”

---

## 🧩 Licencia


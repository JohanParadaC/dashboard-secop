import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Dashboard Contratación Estatal", layout="wide", page_icon="📊")

# Estilo personalizado para las métricas
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 28px; }
    </style>
    """, unsafe_allow_stdio=True)

st.title("📊 Análisis de Contratación Estatal - Resultados Finales")
st.markdown("---")

# --- BLOQUE 1: RESUMEN GENERAL (PUNTOS 1, 2, 3) ---
st.header("1. Indicadores Globales")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Registros (Punto 1)", "1,003,902")
with col2:
    st.metric("Total Variables (Punto 2)", "84")
with col3:
    st.metric("Contratos Año 2025 (Punto 3)", "999,490", help="Nota: La mayoría son contratos proyectados.")

# --- BLOQUE 2: PYMES (PUNTOS 4, 5) ---
st.subheader("Análisis de Pymes")
col_p1, col_p2 = st.columns(2)

with col_p1:
    st.info(f"**Proporción Pymes (Punto 4):** 13.20%")
with col_p2:
    st.info(f"**Número de Contratos (Punto 5):** 132,479")

st.divider()

# --- BLOQUE 3: GEOGRAFÍA Y MODALIDADES (PUNTOS 6, 7, 8, 9) ---
st.header("2. Geografía y Modalidades")
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("Top 10 Departamentos (Punto 6)")
    deptos_lista = "Distrito Capital de Bogotá, Valle del Cauca, Antioquia, Cundinamarca, Santander, Magdalena, Bolívar, Atlántico, Boyacá, Tolima"
    st.code(deptos_lista, language="text")
    st.write(f"**Punto 7:** Magdalena (Posición 6) ejecutó **32,097** contratos.")

with col_g2:
    st.subheader("Modalidad Preferida (Puntos 8, 9)")
    st.success("**Contratación Directa**")
    st.metric("Total Contratos Modalidad", "759,993")

st.divider()

# --- BLOQUE 4: FINANZAS Y TIPOS (PUNTOS 10, 11, 12) ---
st.header("3. Ejecución Financiera y Tipos")

st.subheader("Top 3 Entidades por Monto (Punto 10)")
st.code("""
Top1, DISTRITO ESPECIAL DE CIENCIA TECNOLOGIA E INNOVACION DE MEDELLIN, 7,192,818,196,456.00; 
Top2, MINISTERIO DE MINAS Y ENERGIA, 5,117,844,982,872.00; 
Top3, DEPARTAMENTO DE ANTIOQUIA//, 3,842,869,199,771.00
""", language="text")

col_t1, col_t2 = st.columns([2, 1])

with col_t1:
    st.subheader("Top 5 Tipos de Contrato (Punto 11)")
    data_tipos = {
        "Tipo de Contrato": ["Prestación de servicios", "Decreto 092 de 2017", "Otro", "Suministros", "Compraventa"],
        "Registros": [860913, 41384, 37616, 22669, 16845]
    }
    df_tipos = pd.DataFrame(data_tipos)
    st.table(df_tipos)

with col_t2:
    st.subheader("Dominio (Punto 12)")
    st.metric("Frecuencia Prestación Servicios", "85.76%")
    st.write("Representa la gran mayoría del total de registros.")

st.divider()

# --- BLOQUE 5: ANOMALÍAS Y AMBIENTAL (PUNTOS 13, 14, 15, 17) ---
st.header("4. Hallazgos Especiales")

st.subheader("Top 3 Valores Anómalos Validados (Punto 13)")
anomalias = [
    {"Entidad": "MINISTERIO DE MINAS Y ENERGIA", "Monto": "4.2B", "Veredicto": "Verídico", "Justificación": "Programa Colombia Solar (Nacional)."},
    {"Entidad": "MINCIT", "Monto": "2.8B", "Veredicto": "Verídico", "Justificación": "Arrendamiento Zona Franca Barranquilla."},
    {"Entidad": "RNEC", "Monto": "2.5B", "Veredicto": "Verídico", "Justificación": "Logística electoral procesos 2025-2026."}
]
cols_an = st.columns(3)
for i, an in enumerate(anomalias):
    cols_an[i].warning(f"**{an['Entidad']}**\n\n**Monto:** {an['Monto']}\n\n**Estado:** {an['Veredicto']}\n\n{an['Justificación']}")

col_extra1, col_extra2 = st.columns(2)
with col_extra1:
    st.subheader("Pagos Adelantados (Punto 14)")
    st.metric("Porcentaje de Contratos", "0.08%")
with col_extra2:
    st.subheader("Cláusulas Ambientales (Punto 15 y 17)")
    st.metric("Contratos con 'Si'", "21,347")

st.divider()

# --- BLOQUE 6: PARETO Y GÉNERO (PUNTOS 16, 18, 19) ---
st.header("5. Análisis de Concentración y Género")

st.subheader("Principio de Pareto 80/20 (Puntos 16, 18)")
st.info("""
**Resultado:** Se cumple y supera el principio.
- **Evidencia:** El **20%** de los contratos concentra el **90.75%** del valor total ejecutado.
- **Conclusión:** Existe una altísima concentración de recursos en una minoría de contratos.
""")

st.subheader("Brecha de Género Financiera (Punto 19)")
data_genero = {
    "Género": ["Mujer", "Hombre", "No Definido"],
    "Total Ejecutado (COP)": [36474139893372.00, 53439223860712.00, 75497039656375.00],
    "Cantidad": [434081, 378213, 188960],
    "Promedio por Contrato": [84026114.70, 141293990.06, 399539794.96]
}
df_genero = pd.DataFrame(data_genero)
st.dataframe(df_genero, width=1200) # Usamos width para evitar warnings
st.write("**Análisis:** Existe una brecha clara. Aunque las mujeres tienen más contratos, el valor promedio de los contratos de hombres es **68% superior** ($141M vs $84M).")

st.divider()

# --- BLOQUE 7: CALIDAD DE DATOS (PUNTO 20) ---
st.header("6. Revisión de Calidad de Datos")
anomalias_datos = [
    ["Valor del Contrato", "Objeto (Texto)", "Numérico (Float)", "Impide cálculos financieros directos."],
    ["NIT / Documento", "Objeto / Numérico", "Objeto (Texto)", "Problemas con ceros iniciales y consistencia."],
    ["Fechas (Firma, Inicio, etc.)", "Objeto (Texto)", "Date / Datetime", "Impide análisis de series de tiempo."],
    ["Es Pyme / Obligación Amb.", "Objeto ('Si'/'No')", "Booleano", "Iniciado como categoría, debería ser lógico."],
    ["Duración del contrato", "Objeto (Texto)", "Numérico / Timedelta", "Dificulta medir tiempos de ejecución."]
]
df_anomalias = pd.DataFrame(anomalias_datos, columns=["Variable", "Tipo Actual", "Tipo Correcto", "Explicación"])
st.table(df_anomalias)

st.success("Dashboard generado exitosamente para revisión interinstitucional.")
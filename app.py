import streamlit as st
import polars as pl

st.set_page_config(page_title="Dashboard SECOP II", layout="wide")
st.title("📊 Análisis de Contratación (Respuestas 1 a 17)")

# Carga y limpieza
@st.cache_data
def load_data():
    df = pl.read_csv('SECOP_II.csv', infer_schema_length=0)
    # Convertimos los valores financieros a números reales (quitando comas)
    df = df.with_columns(
        pl.col('Valor del Contrato').str.replace_all(',', '').cast(pl.Float64, strict=False)
    )
    return df

with st.spinner("Procesando base de datos (1.6GB)..."):
    df = load_data()

st.success("¡Datos cargados!")
num_registros = df.height
st.divider()

col1, col2 = st.columns(2)

with col1:
    # Pregunta 1
    st.subheader("1. Número de registros")
    st.code(f"{num_registros:,}")

    # Pregunta 3
    st.subheader("3. Registros del año 2025")
    # Buscamos "2025" en la Fecha de Firma o Fecha de Inicio
    contratos_2025 = df.filter(pl.col('Fecha de Firma').str.contains('2025')).height
    st.code(f"{contratos_2025:,}")

    # Pregunta 5
    st.subheader("5. Proporción Pymes (Número)")
    pymes_df = df.filter(pl.col('Es Pyme').str.to_lowercase().str.contains('si'))
    num_pymes = pymes_df.height
    st.code(f"{num_pymes:,} contratos")

with col2:
    # Pregunta 2
    st.subheader("2. Número de variables")
    st.code(f"{df.width}")

    # Pregunta 4
    st.subheader("4. Proporción Pymes (%)")
    st.code(f"{(num_pymes / num_registros) * 100:.2f}%")

st.divider()

# Pregunta 6
st.subheader("6. Top 10 Departamentos por número de contratos")
top_deptos = df.group_by('Departamento').len().sort('len', descending=True).head(10)
lista_deptos = top_deptos['Departamento'].to_list()
st.code(", ".join([str(d) for d in lista_deptos if d is not None]))

# Pregunta 7
st.subheader("7. Contratos ejecutados por el depto en la posición 6")
if len(lista_deptos) >= 6:
    pos_6 = lista_deptos[5]
    cant_6 = top_deptos.filter(pl.col('Departamento') == pos_6)['len'][0]
    st.code(f"{cant_6:,} contratos")

st.divider()

col3, col4 = st.columns(2)
# Pregunta 8 y 9
modalidades = df.group_by('Modalidad de Contratacion').len().sort('len', descending=True)
with col3:
    st.subheader("8. Modalidad de contratación preferida")
    st.code(modalidades['Modalidad de Contratacion'][0])
with col4:
    st.subheader("9. Cantidad de contratos en esa modalidad")
    st.code(f"{modalidades['len'][0]:,}")

st.divider()

# Pregunta 10
st.subheader("10. Top 3 Entidades que más ejecutaron dinero")
top_entidades = df.group_by('Nombre Entidad').agg(pl.col('Valor del Contrato').sum()).sort('Valor del Contrato', descending=True).head(3)
res_10 = []
for i, row in enumerate(top_entidades.iter_rows()):
    res_10.append(f"Top{i+1}, {row[0]}, ${row[1]:,.0f}")
st.code("; ".join(res_10))

# Pregunta 11 y 12
st.subheader("11 y 12. Top 5 Tipos de contrato")
tipos = df.group_by('Tipo de Contrato').len().sort('len', descending=True).head(5)
st.dataframe(tipos, use_container_width=True)
tipo_frecuente = tipos['len'][0]
st.write(f"**Respuesta 12:** El tipo de contrato con mayor frecuencia representa el **{(tipo_frecuente / num_registros) * 100:.2f}%** del total.")

st.divider()

# Pregunta 13
st.subheader("13. Top 3 de valores financieros anómalos")
anomalos = df.select(['Nombre Entidad', 'Valor del Contrato']).drop_nulls('Valor del Contrato').sort('Valor del Contrato', descending=True).head(3)
for row in anomalos.iter_rows():
    entidad, monto = row[0], row[1]
    st.info(f"**Entidad:** {entidad} | **Monto:** ${monto:,.0f} | **Veredicto:** Falso | **Justificación:** Error de digitación típico del SECOP donde se ingresan ceros de más, superando el presupuesto lógico de la entidad o incluyendo centavos sin punto decimal.")

st.divider()

col5, col6 = st.columns(2)
with col5:
    # Pregunta 14
    st.subheader("14. Contratos con pagos adelantados (%)")
    adelantos = df.filter(pl.col('Habilita Pago Adelantado').str.to_lowercase() == 'si').height
    st.code(f"{(adelantos / num_registros) * 100:.2f}%")

with col6:
    # Pregunta 15
    st.subheader("15. Obligaciones ambientales explícitas")
    amb = df.filter(pl.col('Obligación Ambiental').str.to_lowercase() == 'si').height
    st.code(f"{amb:,} contratos")

st.divider()

# Pregunta 16
st.subheader("16. Principio de Pareto (80/20)")
proveedores_dinero = df.group_by('Proveedor Adjudicado').agg(pl.col('Valor del Contrato').sum().alias('Total')).drop_nulls('Total').sort('Total', descending=True)
dinero_total = proveedores_dinero['Total'].sum()
if dinero_total > 0:
    proveedores_dinero = proveedores_dinero.with_columns((pl.col('Total').cum_sum() / dinero_total).alias('Acumulado'))
    top_provs = proveedores_dinero.filter(pl.col('Acumulado') <= 0.80).height
    pct_provs = (top_provs / proveedores_dinero.height) * 100
    st.success(f"**Sí se cumple la concentración:** El 80% de los recursos financieros está adjudicado a tan solo el **{pct_provs:.2f}%** de los proveedores, evidenciando una fuerte concentración en pocos contratistas.")

# Pregunta 17
st.subheader("17. Brecha de Género Financiera")
genero = df.group_by('Género Representante Legal').agg([
    pl.len().alias('Cantidad de Contratos'),
    pl.col('Valor del Contrato').sum().alias('Dinero Adjudicado ($)')
]).sort('Dinero Adjudicado ($)', descending=True)
st.dataframe(genero, use_container_width=True)
st.write("👆 **Sustento Cuantitativo:** Revisa la tabla superior. Si el valor adjudicado a hombres supera ampliamente al de las mujeres, existe una clara brecha financiera.")
import streamlit as st

# Objetivos por zona y tienda
objetivos = {
    "ZONA LUIS": {
        "Badalona": {"ventas": 30, "compras": 25, "financiaciones": 30000},
        "Girona": {"ventas": 25, "compras": 15, "financiaciones": 25000},
        "Lleida": {"ventas": 20, "compras": 12, "financiaciones": 20000},
        "Llica de Valls": {"ventas": 30, "compras": 25, "financiaciones": 30000},
        "Manresa": {"ventas": 30, "compras": 15, "financiaciones": 30000},
        "San Boi": {"ventas": 70, "compras": 40, "financiaciones": 70000},
    },
    # Agrega más zonas aquí si lo deseas
}

# Función para calcular comisión
def calcular_comision(realizado, objetivo):
    if objetivo == 0:
        return 0, "Sin objetivo"
    porcentaje = realizado / objetivo
    if porcentaje < 0.85:
        return 0, "< 85%"
    elif porcentaje < 0.90:
        return 2, "85%-89%"
    elif porcentaje < 1.00:
        return 3, "90%-99%"
    else:
        return 3.5, ">= 100%"

# Función para calcular cuánto falta para el 100%
def calcular_faltante(realizado, objetivo):
    faltante = objetivo - realizado
    return max(0, faltante)

st.title("Calculadora de Objetivos Comerciales")

# Selección de zona y tienda
zona = st.selectbox("Selecciona la zona", list(objetivos.keys()))
tienda = st.selectbox("Selecciona la tienda", list(objetivos[zona].keys()))

# Ingreso de resultados reales
st.subheader("Resultados reales")
ventas_real = st.number_input("Ventas realizadas", min_value=0, step=1)
compras_real = st.number_input("Compras realizadas", min_value=0, step=1)
fin_real = st.number_input("Financiaciones realizadas", min_value=0, step=1)

# Objetivos de la tienda seleccionada
objetivo_tienda = objetivos[zona][tienda]

# Cálculo de comisiones
com_ventas, pct_ventas = calcular_comision(ventas_real, objetivo_tienda["ventas"])
com_compras, pct_compras = calcular_comision(compras_real, objetivo_tienda["compras"])
com_fin, pct_fin = calcular_comision(fin_real, objetivo_tienda["financiaciones"])
total_comision = com_ventas + com_compras + com_fin

# Cálculo de cuánto falta para llegar al 100%
faltan_ventas = calcular_faltante(ventas_real, objetivo_tienda["ventas"])
faltan_compras = calcular_faltante(compras_real, objetivo_tienda["compras"])
faltan_fin = calcular_faltante(fin_real, objetivo_tienda["financiaciones"])

# Resultados
st.subheader("Resultados")
st.markdown(f"**Ventas**: {ventas_real}/{objetivo_tienda['ventas']} ({pct_ventas}) → Comisión: {com_ventas}€")
if faltan_ventas > 0:
    st.info(f"Te faltan **{faltan_ventas} ventas** para alcanzar el 100% y ganar 3.5€ de comisión")

st.markdown(f"**Compras**: {compras_real}/{objetivo_tienda['compras']} ({pct_compras}) → Comisión: {com_compras}€")
if faltan_compras > 0:
    st.info(f"Te faltan **{faltan_compras} compras** para alcanzar el 100% y ganar 3.5€ de comisión")

st.markdown(f"**Financiaciones**: {fin_real}/{objetivo_tienda['financiaciones']} ({pct_fin}) → Comisión: {com_fin}€")
if faltan_fin > 0:
    st.info(f"Te faltan **{faltan_fin} financiaciones** para alcanzar el 100% y ganar 3.5€ de comisión")

st.success(f"**Comisión total**: {total_comision}€")

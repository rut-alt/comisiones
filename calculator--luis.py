import streamlit as st

# Inicializa las claves de sesión si no existen
if "reset" not in st.session_state:
    st.session_state.reset = False

# Función para resetear campos
def reset_campos():
    for key in list(st.session_state.keys()):
        if key.endswith("_ventas") or key.endswith("_compras") or key.endswith("_fin") or key.endswith("_garantias"):
            st.session_state[key] = 0
    st.session_state.reset = True

# Título y botón
col1, col2 = st.columns([4, 1])
with col1:
    st.title("Comisiones por Tienda - Zona Luis")
with col2:
    if st.button("🧹 Borrar registros"):
        reset_campos()

# Objetivos por zona y tienda
objetivos = {
    "ZONA LUIS": {
        "Badalona": {"ventas": 30, "compras": 25, "financiaciones": 30000, "garantias": 9000},
        "Girona": {"ventas": 25, "compras": 15, "financiaciones": 25000, "garantias": 7500},
        "Lleida": {"ventas": 20, "compras": 12, "financiaciones": 20000, "garantias": 6000},
        "Llica de Valls": {"ventas": 30, "compras": 25, "financiaciones": 30000, "garantias": 9000},
        "Manresa": {"ventas": 30, "compras": 15, "financiaciones": 30000, "garantias": 9000},
        "San Boi": {"ventas": 70, "compras": 40, "financiaciones": 70000, "garantias": 21000},
    },
}

# Comisión variable por unidad (ventas, compras)
def calcular_comision_por_unidad(realizado, objetivo):
    if objetivo == 0:
        return 0, 0, "Sin objetivo"
    porcentaje = realizado / objetivo
    if porcentaje < 0.85:
        return 0, 0, "< 85%"
    elif porcentaje < 0.90:
        return 2, realizado * 2, "85%-89%"
    elif porcentaje <= 1.00:
        return 3, realizado * 3, "90%-100%"
    else:
        return 3.5, realizado * 3.5, "> 100%"

# Comisión fija por tramos (financiaciones y garantías premium)
def calcular_comision_fija(realizado, objetivo, tramos):
    if objetivo == 0:
        return 0, "Sin objetivo"
    porcentaje = realizado / objetivo
    if porcentaje < 0.85:
        return 0, "< 85%"
    elif porcentaje < 0.90:
        return tramos[0], "85%-89%"
    elif porcentaje <= 1.00:
        return tramos[1], "90%-100%"
    else:
        return tramos[2], "> 100%"

zona = "ZONA LUIS"
total_general = 0

for tienda, objetivos_tienda in objetivos[zona].items():
    st.subheader(f"📍 {tienda}")
    
    ventas_real = st.number_input(f"Ventas realizadas en {tienda}", min_value=0, step=1, key=f"{tienda}_ventas")
    compras_real = st.number_input(f"Compras realizadas en {tienda}", min_value=0, step=1, key=f"{tienda}_compras")
    fin_real = st.number_input(f"Financiaciones realizadas en {tienda}", min_value=0, step=1, key=f"{tienda}_fin")
    garantias_real = st.number_input(f"€ Garantías Premium vendidas en {tienda}", min_value=0, step=100, key=f"{tienda}_garantias")

    tarifa_v, com_v, pct_v = calcular_comision_por_unidad(ventas_real, objetivos_tienda["ventas"])
    tarifa_c, com_c, pct_c = calcular_comision_por_unidad(compras_real, objetivos_tienda["compras"])
    com_f, pct_f = calcular_comision_fija(fin_real, objetivos_tienda["financiaciones"], [100, 200, 300])
    com_g, pct_g = calcular_comision_fija(garantias_real, objetivos_tienda["garantias"], [75, 125, 180])

    total_tienda = com_v + com_c + com_f + com_g
    total_general += total_tienda

    st.markdown(f"**Ventas**: {ventas_real}/{objetivos_tienda['ventas']} → {pct_v} → {tarifa_v}€/venta → **{com_v}€**")
    st.markdown(f"**Compras**: {compras_real}/{objetivos_tienda['compras']} → {pct_c} → {tarifa_c}€/compra → **{com_c}€**")
    st.markdown(f"**Financiaciones**: {fin_real}/{objetivos_tienda['financiaciones']} → {pct_f} → Comisión fija: **{com_f}€**")
    st.markdown(f"**Garantías Premium**: {garantias_real}€ / {objetivos_tienda['garantias']}€ → {pct_g} → Comisión fija: **{com_g}€**")

    faltan_ventas = max(0, objetivos_tienda["ventas"] - ventas_real)
    faltan_compras = max(0, objetivos_tienda["compras"] - compras_real)
    faltan_fin = max(0, objetivos_tienda["financiaciones"] - fin_real)
    faltan_garantias = max(0, objetivos_tienda["garantias"] - garantias_real)

    st.warning(
        f"🔄 Te faltan **{faltan_ventas} ventas**, **{faltan_compras} compras**, "
        f"**{faltan_fin}€ en financiaciones** y **{faltan_garantias}€ en garantías** "
        "para llegar al 100% de tus objetivos en esta tienda."
    )

    st.info(f"💰 Comisión total en {tienda}: **{total_tienda}€**")
    st.divider()

st.success(f"🏁 **Comisión total acumulada en todas las tiendas de {zona}: {total_general}€**")



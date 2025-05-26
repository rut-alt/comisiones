import streamlit as st

# Inicialización
if "reset" not in st.session_state:
    st.session_state.reset = False

def reset_campos():
    for key in list(st.session_state.keys()):
        if any(key.endswith(sufijo) for sufijo in [
            "_ventas", "_compras", "_fin", "_garantias"
        ]):
            st.session_state[key] = 0
    st.session_state.reset = True

# Comisiones
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

# Datos de objetivos
objetivos_por_zona = {
    "ZONA NICOLÁS": {
        "Alicante": {"ventas": 45, "compras": 40, "financiaciones": 40000, "garantias": 13500},
        "Murcia": {"ventas": 35, "compras": 25, "financiaciones": 36000, "garantias": 9625},
        "Valencia": {"ventas": 65, "compras": 45, "financiaciones": 52000, "garantias": 17875},
        "Paterna": {"ventas": 30, "compras": 20, "financiaciones": 27000, "garantias": 13400},
    },
    "ZONA LUIS": {
        "Badalona": {"ventas": 30, "compras": 25, "financiaciones": 30000, "garantias": 9000},
        "Girona": {"ventas": 25, "compras": 15, "financiaciones": 25000, "garantias": 7500},
        "Lleida": {"ventas": 20, "compras": 12, "financiaciones": 20000, "garantias": 6000},
        "Llica de Valls": {"ventas": 30, "compras": 25, "financiaciones": 30000, "garantias": 9000},
        "Manresa": {"ventas": 30, "compras": 15, "financiaciones": 30000, "garantias": 9000},
        "San Boi": {"ventas": 70, "compras": 40, "financiaciones": 70000, "garantias": 21000},
    },
    "ZONA DAVID": {
        "Alcalá de Guadaira": {"ventas": 35, "compras": 20, "financiaciones": 38500, "garantias": 10500},
        "Malaga Ortega": {"ventas": 20, "compras": 10, "financiaciones": 20000, "garantias": 6000},
        "Malaga Almacha": {"ventas": 20, "compras": 25, "financiaciones": 20000, "garantias": 6000},
        "Sevilla": {"ventas": 35, "compras": 30, "financiaciones": 38500, "garantias": 10500},
        "Palma": {"ventas": 27, "compras": 20, "financiaciones": 24300, "garantias": 8100},
    },
}

# Interfaz
zona_seleccionada = st.selectbox("Selecciona una zona:", list(objetivos_por_zona.keys()))

col1, col2 = st.columns([4, 1])
with col1:
    st.title(f"Comisiones por Tienda - {zona_seleccionada}")
with col2:
    if st.button("🧹 Borrar registros"):
        reset_campos()

# ✅ Modo de objetivos GLOBAL
modo_objetivos = st.radio("¿Cómo quieres definir los objetivos?", ["Por defecto", "Manual"])

total_general = 0

for tienda, objetivos_defecto in objetivos_por_zona[zona_seleccionada].items():
    st.subheader(f"📍 {tienda}")

    if modo_objetivos == "Manual":
        with st.expander("📋 Introducir objetivos manuales"):
            ventas_obj = st.number_input(f"🎯 Objetivo VENTAS - {tienda}", 0, key=f"{tienda}_obj_ventas")
            compras_obj = st.number_input(f"🎯 Objetivo COMPRAS - {tienda}", 0, key=f"{tienda}_obj_compras")
            fin_obj = st.number_input(f"🎯 Objetivo FINANCIACIÓN - {tienda}", 0, step=100, key=f"{tienda}_obj_fin")
            garantias_obj = st.number_input(f"🎯 Objetivo GARANTÍAS - {tienda}", 0, step=100, key=f"{tienda}_obj_garantias")

            objetivos_tienda = {
                "ventas": ventas_obj or objetivos_defecto["ventas"],
                "compras": compras_obj or objetivos_defecto["compras"],
                "financiaciones": fin_obj or objetivos_defecto["financiaciones"],
                "garantias": garantias_obj or objetivos_defecto["garantias"],
            }
    else:
        objetivos_tienda = objetivos_defecto

    # Valores reales
    ventas_real = st.number_input(f"Ventas en {tienda}", 0, key=f"{tienda}_ventas")
    compras_real = st.number_input(f"Compras en {tienda}", 0, key=f"{tienda}_compras")
    fin_real = st.number_input(f"Financiaciones en {tienda}", 0, step=100, key=f"{tienda}_fin")
    garantias_real = st.number_input(f"€ Garantías Premium en {tienda}", 0, step=100, key=f"{tienda}_garantias")

    # Comisiones
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

    st.warning(
        f"🔄 Faltan **{max(0, objetivos_tienda['ventas'] - ventas_real)} ventas**, "
        f"**{max(0, objetivos_tienda['compras'] - compras_real)} compras**, "
        f"**{max(0, objetivos_tienda['financiaciones'] - fin_real)}€ en financiaciones**, "
        f"**{max(0, objetivos_tienda['garantias'] - garantias_real)}€ en garantías**"
    )
    
    st.info(f"💰 Comisión total en {tienda}: **{total_tienda}€**")
    st.divider()

# Total final
st.success(f"🏁 **Comisión total en {zona_seleccionada}: {total_general}€**")

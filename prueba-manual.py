import streamlit as st

# Simulamos los objetivos por defecto (puedes cargar esto desde un archivo o base de datos)
objetivos = {
    "Zona Norte": {
        "Tienda A": {"ventas": 100, "compras": 80, "financiaciones": 50, "garantias": 30},
        "Tienda B": {"ventas": 120, "compras": 90, "financiaciones": 60, "garantias": 35},
    }
}

# Selección de zona
zona = st.selectbox("Selecciona una zona", list(objetivos.keys()))

# Modo de entrada de objetivos
modo_objetivos = st.radio(
    "¿Cómo quieres definir los objetivos?",
    ["Usar los objetivos por defecto", "Quiero introducirlos manualmente"]
)

# Botón para resetear campos
if "reset" not in st.session_state:
    st.session_state.reset = False

def reset_campos():
    for key in list(st.session_state.keys()):
        if (
            key.endswith("_ventas") or 
            key.endswith("_compras") or 
            key.endswith("_fin") or 
            key.endswith("_garantias")
        ) and not key.endswith("_obj"):
            st.session_state[key] = 0
    st.session_state.reset = True

if st.button("🧹 Borrar registros"):
    reset_campos()

# Mostrar inputs por tienda
for tienda, objetivos_defecto in objetivos[zona].items():
    st.subheader(f"📍 {tienda}")

    if modo_objetivos == "Quiero introducirlos manualmente":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            ventas_obj = st.number_input(
                f"🎯 Ventas objetivo - {tienda}", min_value=0, value=objetivos_defecto["ventas"], key=f"{tienda}_ventas_obj"
            )
        with col2:
            compras_obj = st.number_input(
                f"🎯 Compras objetivo - {tienda}", min_value=0, value=objetivos_defecto["compras"], key=f"{tienda}_compras_obj"
            )
        with col3:
            fin_obj = st.number_input(
                f"🎯 € Financiaciones objetivo - {tienda}", min_value=0, value=objetivos_defecto["financiaciones"], key=f"{tienda}_fin_obj"
            )
        with col4:
            garantias_obj = st.number_input(
                f"🎯 € Garantías objetivo - {tienda}", min_value=0, value=objetivos_defecto["garantias"], key=f"{tienda}_garantias_obj"
            )

        # Usar los valores introducidos si no son 0, sino usar defecto
        objetivos_tienda = {
            "ventas": ventas_obj or objetivos_defecto["ventas"],
            "compras": compras_obj or objetivos_defecto["compras"],
            "financiaciones": fin_obj or objetivos_defecto["financiaciones"],
            "garantias": garantias_obj or objetivos_defecto["garantias"]
        }

    else:
        objetivos_tienda = objetivos_defecto

    # Aquí podrías usar objetivos_tienda para comparar con valores reales
    st.write("Objetivos activos para esta tienda:", objetivos_tienda)

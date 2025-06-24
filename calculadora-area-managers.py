import streamlit as st

# ----------  ESTILOS  -------------------------------------------------------
st.markdown(
    """
    <style>
        /* Fondo blanco + texto negro por defecto */
        .stApp, .block-container, body {background-color:white!important;color:black!important;}

        /* Encabezados, párrafos, etc. en negro */
        h1,h2,h3,h4,h5,h6,p,label,div,span{color:black!important;}

        /* Inputs visibles */
        .stNumberInput,.stRadio,.stSelectbox{color:black!important;}

        /* Expander */
        div[data-testid="stExpander"] div[role="button"]{
            background-color:#f2f2f2!important;color:black!important;
        }

        /* Botones normales */
        .stButton>button{
            background-color:#0f62fe!important;color:white!important;
            border:none;border-radius:5px;padding:0.5em 1em;
        }

        /* Selectbox (valor seleccionado) en fondo azul y texto blanco */
        div[data-testid="stSelectbox"]>div{
            background-color:#0f62fe!important;color:white!important;
            border-radius:5px;padding:0.25em 0.5em;
        }

        /* Alertas (success, warning…) en negro */
        .stAlert{color:black!important;}
    </style>
    """,
    unsafe_allow_html=True
)

# ----------  ESTADO / RESET  ------------------------------------------------
if "reset" not in st.session_state:
    st.session_state.reset = False

def reset_campos():
    for key in list(st.session_state.keys()):
        if any(key.endswith(sufijo) for sufijo in ["_entregas","_compras","_fin","_garantias"]):
            st.session_state[key] = 0
    st.session_state.reset = True

# ----------  FUNCIONES DE COMISIÓN  ----------------------------------------
def calcular_comision_por_unidad(realizado, objetivo):
    if objetivo == 0:
        return 0, 0, "Sin objetivo"
    porcentaje = realizado / objetivo
    if porcentaje < 0.85:
        return 0, 0, "< 85 %"
    elif porcentaje < 0.90:
        return 2, realizado * 2, "85 %-89 %"
    elif porcentaje <= 1.00:
        return 3, realizado * 3, "90 %-100 %"
    else:
        return 3.5, realizado * 3.5, "> 100 %"

def calcular_comision_fija(realizado, objetivo, tramos):
    if objetivo == 0:
        return 0, "Sin objetivo"
    porcentaje = realizado / objetivo
    if porcentaje < 0.85:
        return 0, "< 85 %"
    elif porcentaje < 0.90:
        return tramos[0], "85 %-89 %"
    elif porcentaje <= 1.00:
        return tramos[1], "90 %-100 %"
    else:
        return tramos[2], "> 100 %"

# ----------  OBJETIVOS POR ZONA  -------------------------------------------
objetivos_por_zona = {
    # (antiguas zonas; “ventas” -> “entregas”)
    "ZONA NICOLÁS": {
        "Alicante":   {"entregas":45,"compras":40,"financiaciones":40000,"garantias":13500},
        "Murcia":     {"entregas":35,"compras":25,"financiaciones":36000,"garantias":9625},
        "Valencia":   {"entregas":65,"compras":45,"financiaciones":52000,"garantias":17875},
        "Paterna":    {"entregas":30,"compras":20,"financiaciones":27000,"garantias":13400},
    },
    "ZONA LUIS": {
        "Badalona":   {"entregas":30,"compras":25,"financiaciones":30000,"garantias":9000},
        "Girona":     {"entregas":25,"compras":15,"financiaciones":25000,"garantias":7500},
        "Lleida":     {"entregas":20,"compras":12,"financiaciones":20000,"garantias":6000},
        "Llica de Valls":{"entregas":30,"compras":25,"financiaciones":30000,"garantias":9000},
        "Manresa":    {"entregas":30,"compras":15,"financiaciones":30000,"garantias":9000},
        "San Boi":    {"entregas":70,"compras":40,"financiaciones":70000,"garantias":21000},
    },
    "ZONA DAVID": {
        "Alcalá de Guadaira":{"entregas":35,"compras":20,"financiaciones":38500,"garantias":10500},
        "Malaga Ortega":     {"entregas":20,"compras":10,"financiaciones":20000,"garantias":6000},
        "Malaga Almacha":    {"entregas":20,"compras":25,"financiaciones":20000,"garantias":6000},
        "Sevilla":           {"entregas":35,"compras":30,"financiaciones":38500,"garantias":10500},
        "Palma":             {"entregas":27,"compras":20,"financiaciones":24300,"garantias":8100},
    },

    # ----------  NUEVAS ZONAS  ---------------------------------------------
    "ZONA FELIX": {
        "GIJON":       {"entregas":0,"compras":0,"financiaciones":0,"garantias":0},
        "A CORUÑA":    {"entregas":0,"compras":0,"financiaciones":0,"garantias":0},
        "RIVAS":       {"entregas":0,"compras":0,"financiaciones":0,"garantias":0},
        "ALCOBENDAS":  {"entregas":0,"compras":0,"financiaciones":0,"garantias":0},
        "TORREJON":    {"entregas":0,"compras":0,"financiaciones":0,"garantias":0},
        "VALLADOLID":  {"entregas":0,"compras":0,"financiaciones":0,"garantias":0},
        "VILLALBA":    {"entregas":0,"compras":0,"financiaciones":0,"garantias":0},
    },
    "ZONA OSCAR": {
        "PAMPLONA":        {"entregas":0,"compras":0,"financiaciones":0,"garantias":0},
        "BILBAO":          {"entregas":0,"compras":0,"financiaciones":0,"garantias":0},
        "SAN SEBASTIAN":   {"entregas":0,"compras":0,"financiaciones":0,"garantias":0},
        "FONTELLAS":       {"entregas":0,"compras":0,"financiaciones":0,"garantias":0},
        "ZARAGOZA":        {"entregas":0,"compras":0,"financiaciones":0,"garantias":0},
    },
}

# ----------  INTERFAZ  ------------------------------------------------------
zona_seleccionada = st.selectbox("Selecciona una zona:", list(objetivos_por_zona.keys()))

col1, col2 = st.columns([4,1])
with col1:
    st.title(f"Comisiones por Tienda – {zona_seleccionada}")
with col2:
    if st.button("🧹 Borrar registros"):
        reset_campos()

modo_objetivos = st.radio("¿Cómo quieres definir los objetivos?", ["Por defecto","Manual"])
total_general = 0

# ----------  BUCLE POR TIENDAS  --------------------------------------------
for tienda, objetivos_defecto in objetivos_por_zona[zona_seleccionada].items():
    st.subheader(f"📍 {tienda}")

    # ----- Objetivos (manuales o por defecto)
    if modo_objetivos == "Manual":
        with st.expander("📋 Introducir objetivos manuales"):
            ent_obj  = st.number_input(f"🎯 Objetivo ENTREGAS – {tienda}", 0, key=f"{tienda}_obj_entregas")
            comp_obj = st.number_input(f"🎯 Objetivo COMPRAS – {tienda}", 0, key=f"{tienda}_obj_compras")
            fin_obj  = st.number_input(f"🎯 Objetivo FINANCIACIÓN – {tienda}", 0, step=100, key=f"{tienda}_obj_fin")
            gar_obj  = st.number_input(f"🎯 Objetivo GARANTÍAS – {tienda}", 0, step=100, key=f"{tienda}_obj_garantias")

            objetivos_tienda = {
                "entregas":      ent_obj  or objetivos_defecto["entregas"],
                "compras":       comp_obj or objetivos_defecto["compras"],
                "financiaciones":fin_obj  or objetivos_defecto["financiaciones"],
                "garantias":     gar_obj  or objetivos_defecto["garantias"],
            }
    else:
        objetivos_tienda = objetivos_defecto

    # ----- Valores reales introducidos
    entregas_real  = st.number_input(f"Entregas en {tienda}", 0, key=f"{tienda}_entregas")
    compras_real   = st.number_input(f"Compras en {tienda}", 0, key=f"{tienda}_compras")
    fin_real       = st.number_input(f"Financiaciones en {tienda}", 0, step=100, key=f"{tienda}_fin")
    garantias_real = st.number_input(f"€ Garantías Premium en {tienda}", 0, step=100, key=f"{tienda}_garantias")

    # ----- Cálculo de comisiones
    tarifa_e, com_e, pct_e = calcular_comision_por_unidad(entregas_real, objetivos_tienda["entregas"])
    tarifa_c, com_c, pct_c = calcular_comision_por_unidad(compras_real,  objetivos_tienda["compras"])
    com_f, pct_f           = calcular_comision_fija(fin_real,       objetivos_tienda["financiaciones"], [100, 200, 300])
    com_g, pct_g           = calcular_comision_fija(garantias_real, objetivos_tienda["garantias"],      [75, 125, 180])

    total_tienda = com_e + com_c + com_f + com_g
    total_general += total_tienda

    # ----- Resultados visibles
    st.markdown(f"**Entregas**: {entregas_real}/{objetivos_tienda['entregas']} → {pct_e} → {tarifa_e} €/entrega → **{com_e} €**")
    st.markdown(f"**Compras**: {compras_real}/{objetivos_tienda['compras']} → {pct_c} → {tarifa_c} €/compra → **{com_c} €**")
    st.markdown(f"**Financiaciones**: {fin_real}/{objetivos_tienda['financiaciones']} → {pct_f} → Comisión fija: **{com_f} €**")
    st.markdown(f"**Garantías Premium**: {garantias_real} € / {objetivos_tienda['garantias']} € → {pct_g} → Comisión fija: **{com_g} €**")

    st.warning(
        f"🔄 Faltan **{max(0, objetivos_tienda['entregas'] - entregas_real)} entregas**, "
        f"**{max(0, objetivos_tienda['compras'] - compras_real)} compras**, "
        f"**{max(0, objetivos_tienda['financiaciones'] - fin_real)} € en financiaciones**, "
        f"**{max(0, objetivos_tienda['garantias'] - garantias_real)} € en garantías**"
    )

    st.info(f"💰 Comisión total en {tienda}: **{total_tienda} €**")
    st.divider()

# ----------  TOTAL GENERAL  -------------------------------------------------
st.success(f"🏁 **Comisión total en {zona_seleccionada}: {total_general} €**")



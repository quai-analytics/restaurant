# Importando librerias
import streamlit as st
import pandas as pd
import datetime

# ----------------------------------------------
# --- Configuración de la Página ---
st.set_page_config(
    page_title = "QuAI Analytics - Demo de Restaurante",
    layout = "wide"
)

st.title("Restaurante El Analítico")

# ----------------------------------------------
# --- Inicializar el DataFrame en Session State ---

if 'informes_df' not in st.session_state:
    st.session_state.informes_df = pd.DataFrame(columns=[
        "Fecha",
        "Venta Interna",
        "Venta Delivery",
        "Venta Total", # Calculado
        "Tip Visa",
        "Tip Amex",
        "Tip Efectivo",
        "Tip Total",     # Calculado
        "Otros Ingresos",
        "Gastos",
        "Saldo Inicial",
        "Total en Caja"  # Calculado
    ])

# ----------------------------------------------
# --- El Formulario (Arriba) ---
st.header("Informe diario de venta")

with st.form(key="informe_diario_form", clear_on_submit=True):
    
    # Fecha del informe
    fecha = st.date_input("Fecha del Informe", datetime.date.today())

    # Organizamos los campos en columnas para que se parezca al Excel
    col_ventas, col_tips, col_caja = st.columns(3)

    with col_ventas:
        st.subheader("Ventas")
        venta_interna = st.number_input("Venta Interna", min_value=0.0, format="%.2f")
        venta_delivery = st.number_input("Venta Delivery", min_value=0.0, format="%.2f")

    with col_tips:
        st.subheader("Detalle del Tip")
        tip_visa = st.number_input("Tip Visa", min_value=0.0, format="%.2f")
        tip_amex = st.number_input("Tip Amex", min_value=0.0, format="%.2f")
        tip_efectivo = st.number_input("Tip Efectivo", min_value=0.0, format="%.2f")

    with col_caja:
        st.subheader("Caja y Gastos")
        saldo_inicial = st.number_input("Saldo Inicial", min_value=0.0, format="%.2f")
        otros_ingresos = st.number_input("Otros Ingresos", min_value=0.0, format="%.2f")
        gastos = st.number_input("Gastos", min_value=0.0, format="%.2f")

    # Botón de envío
    submitted = st.form_submit_button("Guardar Informe Diario")

# ----------------------------------------------
# --- Lógica de Procesamiento ---
if submitted:
    # Realizamos los cálculos que en tu Excel parecen automáticos
    venta_total = venta_interna + venta_delivery
    tip_total = tip_visa + tip_amex + tip_efectivo
    
    # Cálculo simple de caja (puedes ajustar esta fórmula)
    total_en_caja = (saldo_inicial + venta_total + tip_efectivo + otros_ingresos) - gastos
    
    # Creamos la nueva fila
    nueva_fila = {
        "Fecha": [fecha],
        "Venta Interna": [venta_interna],
        "Venta Delivery": [venta_delivery],
        "Venta Total": [venta_total],
        "Tip Visa": [tip_visa],
        "Tip Amex": [tip_amex],
        "Tip Efectivo": [tip_efectivo],
        "Tip Total": [tip_total],
        "Otros Ingresos": [otros_ingresos],
        "Gastos": [gastos],
        "Saldo Inicial": [saldo_inicial],
        "Total en Caja": [total_en_caja]
    }
    
    df_nueva_fila = pd.DataFrame(nueva_fila)
    
    # Usamos pd.concat para "alimentar" el DataFrame principal
    st.session_state.informes_df = pd.concat(
        [st.session_state.informes_df, df_nueva_fila],
        ignore_index=True
    )
    
    st.success(f"¡Informe del {fecha.strftime('%d/%m/%Y')} agregado con éxito!")

# ----------------------------------------------
# --- 4. El DataFrame (Abajo) ---
st.divider()
st.header("📊 Historial de Informes de Venta")

# Hacemos una copia para no modificar el original en session_state
df_display = st.session_state.informes_df.copy()

# Ordenamos por fecha, el más reciente primero
df_display = df_display.sort_values(by="Fecha", ascending=False)

# Usamos st.dataframe con configuración para formatear los números
st.dataframe(
    df_display,
    width='stretch',
    column_config={
        "Fecha": st.column_config.DateColumn(
            "Fecha",
            format="DD/MM/YYYY"
        ),
        # Formateamos todas las columnas de dinero
        "Venta Interna": st.column_config.NumberColumn(format="$ %.2f"),
        "Venta Delivery": st.column_config.NumberColumn(format="$ %.2f"),
        "Venta Total": st.column_config.NumberColumn(format="$ %.2f"),
        "Tip Visa": st.column_config.NumberColumn(format="$ %.2f"),
        "Tip Amex": st.column_config.NumberColumn(format="$ %.2f"),
        "Tip Efectivo": st.column_config.NumberColumn(format="$ %.2f"),
        "Tip Total": st.column_config.NumberColumn(format="$ %.2f"),
        "Otros Ingresos": st.column_config.NumberColumn(format="$ %.2f"),
        "Gastos": st.column_config.NumberColumn(format="$ %.2f"),
        "Saldo Inicial": st.column_config.NumberColumn(format="$ %.2f"),
        "Total en Caja": st.column_config.NumberColumn(format="$ %.2f"),
    },
    hide_index=True # Ocultamos el índice para que se vea más limpio
)

# --- (Opcional) Botón para limpiar ---
if st.button("🧹 Limpiar Historial"):
    st.session_state.informes_df = pd.DataFrame(columns=st.session_state.informes_df.columns)
    st.rerun()

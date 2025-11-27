# Importando librerias
import datetime
import time
import os
import json
import io

import streamlit as st
import altair as alt
import pandas as pd

from utils import *

# Importar librerías necesarias para BigQuery y pandas
from google.cloud import storage
from google.oauth2 import service_account


# ----------------------------------------------
# --- Configuración de la Página ---
st.set_page_config(
    page_title = "QuAI Analytics - Demo de Restaurante",
    layout = "wide"
)

st.title("Restaurante El Analítico")

# ----------------------------------------------
# --- Formato QuAI ---

apply_sidebar_style()
mostrar_sidebar_con_logo()
mostrar_sidebar_footer()


# ----------------------------------------------
# --- Variables de inicio ---
BUCKET_NAME = "data_quai_dev"
FILE_NAME = "restaurante_diario.csv"

# ----------------------------------------------
# --- Configuración de GCP.    ---
BUCKET_NAME = "data_quai_dev" # Nombre del bucket

if os.environ['USER'] == "appuser":
    # En Streamlit Community Cloud
    Credentials = st.secrets["google_cloud"]["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(Credentials)
    )
else:
    service_account_path = os.path.join(
        os.path.dirname(__file__), "..","secrets.json"
    )
    credentials = service_account.Credentials.from_service_account_file(service_account_path)

client = storage.Client(credentials=credentials, project=credentials.project_id)
bucket = client.bucket(BUCKET_NAME)

COLUMNAS_ESPERADAS = [
    "Fecha",
    "Tipo de Pago",
    "Tipo de Venta",
    "Monto",
    "Tip",
    "Impuesto",
    "Sucursal",
    "Area",
    "Total Calculado"
]

# ----------------------------------------------
# --- Inicializar el DataFrame en Session State ---

if 'informes_individual_df' not in st.session_state:
    # 1. Cargar del bucket usando el nombre CORRECTO de variable
    df_cargado = cargar_df_del_bucket(
        bucket, 
        FILE_NAME, 
        columnas_esperadas=COLUMNAS_ESPERADAS
    )
    
    # 2. Asegurar que la columna Fecha sea tipo datetime (crucial para gráficos)
    if not df_cargado.empty:
        df_cargado['Fecha'] = pd.to_datetime(df_cargado['Fecha'])
        
    st.session_state.informes_individual_df = df_cargado
    print("✅ DataFrame cargado en informes_individual_df.")

# 'ultimo_calculo' guardará solo los datos del resumen de la derecha
if 'ultimo_calculo' not in st.session_state:
    st.session_state.ultimo_calculo = None

# Cálculos
df = st.session_state.informes_individual_df
total_ventas = df['Monto'].sum() if not df.empty else 0
total_impuestos = df['Impuesto'].sum() if not df.empty else 0
total_tips = df['Tip'].sum() if not df.empty else 0

# --- KPIs en Contenedores (Cards) ---
with st.container():
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        with st.container(border=True):
            st.metric("💰 Ventas Netas", f"${total_ventas:,.2f}")
    with c2:
        with st.container(border=True):
            st.metric("🏛️ Impuestos", f"${total_impuestos:,.2f}")
    with c3:
        with st.container(border=True):
            st.metric("🤝 Tips Staff", f"${total_tips:,.2f}")
    with c4:
        with st.container(border=True):
            # Métrica calculada: Ticket promedio
            ticket_prom = total_ventas / len(df) if len(df) > 0 else 0
            st.metric("Ticket Promedio", f"${ticket_prom:,.2f}")

st.divider()

# ----------------------------------------------
# --- El Formulario (Arriba) ---
st.header("Reporte de venta individual")

# Organizamos la pantalla en columnas
col_form, col_resumen = st.columns([0.65, 0.35], gap="large")
    
with col_form:
    with st.form(key="informe_individual_form", clear_on_submit=True):

        # Organizamos el header en dos columnas
        col_fecha, col_sucursal = st.columns(2)
        
        # Fecha del informe
        with col_fecha:
            fecha = st.date_input("Fecha", datetime.date.today())

            # Tipo de venta
            tipo_venta = st.selectbox("Tipo", ("Interna", "Delivery"))

            st.subheader("Montos")

            # Monto de la venta
            monto_venta = st.number_input("Monto", min_value=0.0, format="%.2f")

            # Monto del tax
            monto_tax = st.number_input("Impuesto", min_value=0.0, format="%.2f")

        
        # Tipo de venta
        with col_sucursal:
            sucursal = st.selectbox("Sucursal", ("Costa del Este", "San Francisco"))

            # Area
            area_venta = st.selectbox("Area", ("Restaurante", "Bar", "Paellas"))

            st.subheader("")

            # Tipo de pago
            modo_pago = st.selectbox("Modo de Pago", ("VISA", "Cash", "AMEX"))

            # Monto del tip
            monto_tip = st.number_input("Tip", min_value=0.0, format="%.2f")

    
        # Botón de envío
        submitted = st.form_submit_button("Guardar...")

    # --- DERECHA: Resumen (Look de Recibo) ---
with col_resumen:
    st.subheader("🧾 Ticket Actual")
    
    # --- MEJORA 2: Contenedor con borde para simular un recibo ---
    with st.container(border=True):
        if submitted:
            # Lógica
            total_venta = monto_venta + monto_tax + monto_tip
            
            st.session_state.ultimo_calculo = {
                "monto": monto_venta,
                "impuesto": monto_tax,
                "tip": monto_tip,
                "total": total_venta
            }
            
            # Guardar en DF
            nueva_fila = pd.DataFrame([{
                "Fecha": pd.to_datetime(fecha), # Asegurar formato fecha
                "Tipo de Pago": modo_pago,
                "Tipo de Venta": tipo_venta,
                "Monto": monto_venta,
                "Tip": monto_tip,
                "Impuesto": monto_tax,
                "Sucursal": sucursal,
                "Area": area_venta,
                "Total Calculado": total_venta
            }])
            
            st.session_state.informes_individual_df = pd.concat(
                [st.session_state.informes_individual_df, nueva_fila], 
                ignore_index=True
            )

            # --- NUEVO: GUARDAR EN LA NUBE ---
            guardar_df_en_bucket(st.session_state.informes_individual_df, bucket, FILE_NAME)
            
            st.toast("✅ Venta registrada exitosamente", icon="🎉")
            st.rerun()

        # Visualización del Ticket
        datos = st.session_state.ultimo_calculo
        
        if datos:
            st.markdown(f"""
            <div style="padding: 10px; background-color: rgba(255,255,255,0.05); border-radius: 5px;">
                <div style="display:flex; justify-content:space-between;"><span>Subtotal:</span> <strong>${datos['monto']:.2f}</strong></div>
                <div style="display:flex; justify-content:space-between; color: #aaa;"><span>Tax:</span> <span>${datos['impuesto']:.2f}</span></div>
                <div style="display:flex; justify-content:space-between; color: #aaa;"><span>Tip:</span> <span>${datos['tip']:.2f}</span></div>
                <hr style="margin: 10px 0;">
                <div style="display:flex; justify-content:space-between; font-size: 1.2em;"><span>TOTAL:</span> <strong style="color:#00CC96">${datos['total']:.2f}</strong></div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Limpiar Ticket", use_container_width=True):
                st.session_state.ultimo_calculo = None
                st.rerun()
        else:
            st.info("Ingresa los datos en el formulario para ver la previsualización del ticket.")
            st.image("https://cdn-icons-png.flaticon.com/512/1055/1055646.png", width=50) # Icono placeholder opcional

st.divider()
st.header("Historial de Ventas Guardadas")


# --- MEJORA 3: Pestañas para ver Datos vs Gráficos ---
tab1, tab2 = st.tabs(["📊 Historial Detallado", "📈 Tendencia de Ventas"])

with tab1:
    # DataFrame con column_config para formateo automático de dinero
    df_individual = st.dataframe(
        st.session_state.informes_individual_df,
        use_container_width=True,
        selection_mode="multi-row",
        on_select='rerun',
        hide_index=True,
        column_config={
            "Fecha": st.column_config.DateColumn("Fecha", format="DD/MM/YYYY"),
            "Monto": st.column_config.NumberColumn("Venta Neta", format="$ %.2f"),
            "Impuesto": st.column_config.NumberColumn("Tax", format="$ %.2f"),
            "Tip": st.column_config.NumberColumn("Tip", format="$ %.2f"),
            "Total Calculado": st.column_config.ProgressColumn(
                "Total Operación", 
                format="$ %.2f", 
                min_value=0, 
                max_value=1000 # Ajustar según tu realidad
            ),
            "Tipo de Pago": st.column_config.Column(
                "Pago",
                width="small"
            )
        }
    )

    # 2. Capturar los índices de las filas seleccionadas
    filas_seleccionadas = df_individual.selection.rows

    # 3. Mostrar el botón de borrar SOLO si hay algo seleccionado
    if filas_seleccionadas:
        st.warning(f"Has seleccionado {len(filas_seleccionadas)} fila(s).")

        if st.button("🗑️ Eliminar Filas Seleccionadas", type="primary"):

            # A) Usar la variable CORRECTA: informes_individual_df
            st.session_state.informes_individual_df = st.session_state.informes_individual_df.drop(
                st.session_state.informes_individual_df.index[filas_seleccionadas]
            ).reset_index(drop=True)
            
            # B) Guardar el cambio en el Bucket
            guardar_df_en_bucket(st.session_state.informes_individual_df, bucket, FILE_NAME)
            
            
            # C) Mensaje de éxito y recarga
            st.success("✅ Filas eliminadas y bucket actualizado.")
            time.sleep(1)  # Pequeña pausa para asegurar que el guardado se complete
            st.rerun()

with tab2:
    if not df.empty:
        # Un gráfico simple de barras con Altair
        chart = alt.Chart(df).mark_bar().encode(
            x='Fecha:T',
            y='Total Calculado:Q',
            color='Sucursal:N',
            tooltip=['Fecha', 'Total Calculado', 'Sucursal']
        ).interactive()
        st.altair_chart(chart, use_container_width=True)
    else:
        st.write("No hay datos para graficar aún.")

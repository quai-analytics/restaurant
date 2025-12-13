# Importando librerias
import datetime
import sys
import os
import json
import io
import time
from google.cloud.exceptions import NotFound

import streamlit as st
import pandas as pd

# Importar librerías necesarias para BigQuery y pandas
from google.cloud import storage
from google.oauth2 import service_account

from utils import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ----------------------------------------------
# --- Formato QuAI ---

apply_sidebar_style()
mostrar_sidebar_con_logo()
mostrar_sidebar_footer()

# ----------------------------------------------
# --- Variables de inicio ---
TITULO_APP = "QuAI Analytics - Demo Restaurante"
BUCKET_NAME = "data_quai_dev"
FILE_NAME = "restaurante_informes.csv"


# ----------------------------------------------
# --- Configuración de la Página ---
st.set_page_config(
    page_title = TITULO_APP,
    layout = "wide"
)

st.title("Restaurante El Analítico")

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
        os.path.dirname(__file__), "secrets.json"
    )
    credentials = service_account.Credentials.from_service_account_file(service_account_path)

client = storage.Client(credentials=credentials, project=credentials.project_id)
bucket = client.bucket(BUCKET_NAME)

# ----------------------------------------------
# --- Columnas y datos    ---

# Definir columnas esperadas
COLUMNAS_ESPERADAS = [
    "Fecha",
    "Venta Interna",
    "Venta Delivery",
    "Venta Total",
    "Tip Visa",
    "Tip Amex",
    "Tip Efectivo",
    "Tip Total",
    "Otros Ingresos",
    "Gastos",
    "Saldo Inicial",
    "Total en Caja"
]

# ----------------------------------------------
# --- Inicializar el DataFrame en Session State ---

if "informes_df" not in st.session_state:
    print("Inicializando el DataFrame en session_state...")
    # Cargar el CSV del bucket (o crear uno vacío si no existe)
    st.session_state.informes_df = cargar_df_del_bucket(
        bucket, 
        FILE_NAME, 
        columnas_esperadas=COLUMNAS_ESPERADAS
    )
    print("✅ DataFrame cargado en session_state.")

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
        venta_interna = st.number_input("Venta Interna", min_value=0.0, format="%.2f",placeholder= None)
        venta_delivery = st.number_input("Venta Delivery", min_value=0.0, format="%.2f",placeholder= None)

    with col_tips:
        st.subheader("Detalle del Tip")
        tip_visa = st.number_input("Tip Visa", min_value=0.0, format="%.2f",placeholder= None)
        tip_amex = st.number_input("Tip Amex", min_value=0.0, format="%.2f",placeholder= None)
        tip_efectivo = st.number_input("Tip Efectivo", min_value=0.0, format="%.2f",placeholder= None)

    with col_caja:
        st.subheader("Caja y Gastos")
        saldo_inicial = st.number_input("Saldo Inicial", min_value=0.0, format="%.2f",placeholder= None)
        otros_ingresos = st.number_input("Otros Ingresos", min_value=0.0, format="%.2f",placeholder= None)
        gastos = st.number_input("Gastos", min_value=0.0, format="%.2f",placeholder= None)

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
    
    # 💾 Guardar el DataFrame actualizado en el bucket
    guardar_df_en_bucket(st.session_state.informes_df, bucket, FILE_NAME)
    
    st.success(f"¡Informe del {fecha.strftime('%d/%m/%Y')} agregado con éxito!")

# ----------------------------------------------
# --- 4. El DataFrame (Abajo) ---
st.divider()
st.header("📊 Historial de Informes de Venta")

# Hacemos una copia para no modificar el original en session_state
df_display = st.session_state.informes_df.copy()

# Ordenamos por fecha, el más reciente primero
#df_display = df_display.sort_values(by="Fecha", ascending=False)

# Usamos st.dataframe con configuración para formatear los números
df_event = st.dataframe(
    df_display,
    width='stretch',
    selection_mode="multi-row",
    on_select='rerun',
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

# 2. Capturar los índices de las filas seleccionadas
filas_seleccionadas = df_event.selection.rows

# 3. Mostrar el botón de borrar SOLO si hay algo seleccionado
if filas_seleccionadas:
    st.warning(f"Has seleccionado {len(filas_seleccionadas)} fila(s).")

    if st.button("🗑️ Eliminar Filas Seleccionadas", type="primary"):
        
        # A) Eliminar las filas del DataFrame en memoria
        # Usamos .drop() pasando los índices que nos dio el evento
        st.session_state.informes_df = st.session_state.informes_df.drop(
            st.session_state.informes_df.index[filas_seleccionadas]
        ).reset_index(drop=True)
        
        # B) Guardar el cambio en el Bucket (Sobrescribir el archivo)
        guardar_df_en_bucket(st.session_state.informes_df, bucket, FILE_NAME)
        
        # C) Mensaje de éxito y recarga
        st.success("✅ Filas eliminadas y bucket actualizado.")
        time.sleep(1)  # Pequeña pausa para asegurar que el guardado se complete
        st.rerun()
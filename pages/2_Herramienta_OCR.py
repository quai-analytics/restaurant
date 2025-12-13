import requests
import os
import json

import streamlit as st

from utils import *

apply_sidebar_style()
mostrar_sidebar_con_logo()
mostrar_sidebar_footer()


# --- Configuration ---
# Use Streamlit Secrets! Store your webhook URL and API key (if you set one).
# In .streamlit/secrets.toml:
# N8N_WEBHOOK_URL = "https://your.n8n.instance/webhook/production/your-id"
# N8N_API_KEY = "your-secret-api-key" 
#
# If you didn't set an API key, just comment out the "headers" line below.

if os.environ['USER'] == "appuser":
    # En Streamlit Community Cloud
    N8N_URL = st.secrets["n8n"]["ocr_webhook_url"]
else:
    json_path = os.path.join(os.path.dirname(__file__), "..", "secret_n8n_webhook.json")
    json_path = os.path.abspath(json_path)
    with open(json_path) as f:
        secrets = json.load(f)
    N8N_URL = secrets["dev_server"]
    

N8N_URL = "https://n8n.quaianalytics.com/webhook/15bcbbde-15df-4e36-bd33-7c2a66058169"

# Configuración de página para aprovechar el ancho completo
st.set_page_config(page_title="OCR Dashboard", layout="wide")

st.title("📄 Herramienta de OCR Inteligente")
st.markdown("---")

# 1. Create the file uploader
uploaded_file = st.file_uploader("Sube una imagen para analizar...", 
                                 type=["jpg", "jpeg", "png"],
                                 label_visibility="collapsed")



if uploaded_file is not None:
    # Display the uploaded image
    #st.image(uploaded_file, caption="Image to Analyze")

    # Creamos dos columnas: Izquierda (Imagen) y Derecha (Resultados)
    col_img, col_data = st.columns([1, 1], gap="medium")

    with col_img:
        with st.container(border=True):
            st.subheader("Vista Previa")
            st.subheader("🖼️ Documento Cargado")
            st.image(uploaded_file, use_container_width=True)
            
            # Botón de acción debajo de la imagen (o arriba si prefieres)
            process_btn = st.button("🚀 Procesar e Identificar Datos", type="primary", use_container_width=True)

    # Lógica de procesamiento
    if process_btn:
        with col_data:
            with st.spinner("🤖  IA está analizando el documento..."):
                try:
                    # Preparar payload. Asegúrate que en n8n el Webhook espera la propiedad 'data'
                    # Si tu n8n espera 'file', cambia 'data' por 'file' abajo.
                    files_payload = {
                        'data': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
                    }

                    response = requests.post(N8N_URL, files=files_payload)

                    if response.status_code == 200:
                        data = response.json()
                        
                        # --- DISEÑO DE RESULTADOS ---
                        st.success("✅ ¡Análisis completado!")
                        
                        # Grupo 1: Datos Financieros (Destacados)
                        st.subheader("Resumen Financiero")
                        metric_col1, metric_col2 = st.columns(2)
                        
                        # Extraemos el total y formateamos
                        total_val = data.get("total", "0.00")
                        factura_val = data.get("factura", "S/N")
                        
                        with metric_col1:
                            st.metric(label="Monto Total", value=f"${total_val}")
                        with metric_col2:
                            st.metric(label="N° Factura", value=factura_val)
                        
                        st.divider()
                        
                        # Grupo 2: Datos de la Entidad
                        st.subheader("Información de la Entidad")
                        
                        empresa_val = data.get("empresa", "No detectado")
                        ruc_val = data.get("ruc", "No detectado")

                        # Usamos st.info o st.container para dar estilo de tarjeta
                        with st.container(border=True):
                            st.markdown(f"**🏢 Empresa:** {empresa_val}")
                            st.markdown(f"**🆔 RUC:** {ruc_val}")

                        # Opción para ver el JSON crudo (útil para debug)
                        with st.expander("Ver respuesta técnica (JSON)"):
                            st.json(data)

                    else:
                        st.error(f"Error del servidor: {response.status_code}")
                        st.text(response.text)

                except requests.exceptions.RequestException as e:
                    st.error(f"No se pudo conectar con n8n: {e}")

    # Si no se ha procesado aún, mostramos un mensaje en la derecha
    elif not process_btn:
        with col_data:
            st.info("👈 Haz clic en 'Extraer Datos' para procesar la imagen.")

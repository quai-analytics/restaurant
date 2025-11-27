import streamlit as st
import pandas as pd
import io
from google.cloud.exceptions import NotFound

# 1. Función personalizada para convertir columnas a minúsculas
def to_lowercase(dataframe):
    return dataframe.apply(lambda x: x.str.lower() if x.dtype == "object" else x)

def guardar_df_en_bucket(df, bucket, file_name):
    """Guarda un DataFrame como CSV en el bucket de GCS."""
    csv_string = df.to_csv(index=False)
    blob = bucket.blob(file_name)
    blob.upload_from_string(csv_string, content_type='text/csv')
    # --- AGREGA ESTO PARA VER LA REALIDAD ---
    print(f"--- INICIO DEL TEXTO GUARDADO ({file_name}) ---")
    print(csv_string)
    print("--- FIN DEL TEXTO ---")
    # ----------------------------------------
    print(f"✅ Archivo {file_name} guardado en el bucket.")

def cargar_df_del_bucket(bucket, file_name, columnas_esperadas=None):
    """Carga un DataFrame desde un archivo CSV en GCS. Si no existe, retorna un DataFrame vacío."""
    blob = bucket.blob(file_name)
    
    csv_data = blob.download_as_text()
    # --- AGREGA ESTO PARA VER LA REALIDAD ---
    print(f"--- INICIO DEL TEXTO DESCARGADO ({file_name}) ---")
    print(csv_data)
    print("--- FIN DEL TEXTO ---")
    # ----------------------------------------
    df = pd.read_csv(io.StringIO(csv_data))
    print(df.head())
    print(f"✅ Archivo {file_name} cargado del bucket.")
    return df
    

def mostrar_sidebar_con_logo():
    st.sidebar.image('image/quai_analytics_logo.png')
    st.sidebar.markdown("---")  # Separador visual

def mostrar_sidebar_footer():
    st.sidebar.markdown("""
        <style>
        /* Flex container en sidebar para forzar fondo fijo */
        section[data-testid="stSidebar"] > div:first-child {
            display: flex;
            flex-direction: column;
            height: 100%;
        }

        /* Empuja el footer al fondo */
        .sidebar-spacer {
            flex-grow: 1;
        }

        /* Estilo del footer */
        .sidebar-footer {
            font-size: 0.75em;
            color: white;
            text-align: left;
            padding-top: 1rem;
            padding-bottom: 0.5rem;
            border-top: 0.5px solid rgba(255,255,255,0.2);
            margin-top: 1rem;
        }
        </style>

        <div class="sidebar-spacer"></div>
        <div class="sidebar-footer">
            <small>© 2025 QuAI Analytics</small>
        </div>
    """, unsafe_allow_html=True)

def apply_sidebar_style():
    st.markdown("""
        <style>
        /* Sidebar container */
        section[data-testid="stSidebar"] {
            background-color: #082038;
        }

        /* Forzar texto blanco en todos los elementos del sidebar */
        section[data-testid="stSidebar"] * {
            color: white !important;
        }

        /* Enlaces (a) y listas (li) si quieres más precisión */
        section[data-testid="stSidebar"] a,
        section[data-testid="stSidebar"] li {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
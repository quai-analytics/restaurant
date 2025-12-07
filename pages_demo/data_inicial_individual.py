import pandas as pd
import numpy as np
import random
import os
from datetime import date, timedelta
from google.cloud import storage
from google.oauth2 import service_account

# --- ⚙️ CONFIGURACIÓN ---
BUCKET_NAME = "data_quai_dev"
FILE_NAME = "restaurante_diario.csv"  # El archivo que lee tu Streamlit
CANTIDAD_REGISTROS = 1000               # Cuantas ventas quieres simular
RUTA_SECRETS = "secrets.json"         # ⚠️ Ajusta esto si tu json tiene otro nombre

def generar_y_subir():
    # ---------------------------------------------------------
    # 1. GENERACIÓN DE DATOS
    # ---------------------------------------------------------
    print(f"🔄 Generando {CANTIDAD_REGISTROS} registros ficticios...")
    
    data = []
    opciones_pago = ["VISA", "Cash", "AMEX"]
    opciones_tipo_venta = ["Interna", "Delivery"]
    opciones_sucursal = ["Costa del Este", "San Francisco"]
    opciones_area = ["Restaurante", "Bar", "Paellas"]
    
    fecha_base = date.today()

    for _ in range(CANTIDAD_REGISTROS):
        # Fecha: Aleatoria en los últimos 45 días
        dias_atras = random.randint(0, 365)
        fecha = fecha_base - timedelta(days=dias_atras)
        
        # Selecciones aleatorias
        tipo_pago = random.choice(opciones_pago)
        tipo_venta = random.choice(opciones_tipo_venta)
        sucursal = random.choice(opciones_sucursal)
        area = random.choice(opciones_area)
        
        # Finanzas (Matemática coherente)
        monto = round(random.uniform(25.00, 200.00), 2)  # Venta entre $25 y $200
        impuesto = round(monto * 0.07, 2)                # 7% Tax
        
        # Lógica de Tip: A veces dejan 10%, a veces 15%, a veces nada
        porcentaje_tip = random.choice([0.0, 0.10, 0.15, 0.20])
        tip = round(monto * porcentaje_tip, 2)
        
        # TOTAL EXACTO
        total_calculado = round(monto + impuesto + tip, 2)
        
        fila = {
            "Fecha": fecha,
            "Tipo de Pago": tipo_pago,
            "Tipo de Venta": tipo_venta,
            "Monto": monto,
            "Tip": tip,
            "Impuesto": impuesto,
            "Sucursal": sucursal,
            "Area": area,
            "Total Calculado": total_calculado
        }
        data.append(fila)

    # Crear DataFrame y ordenar por fecha
    df = pd.DataFrame(data)
    df = df.sort_values(by="Fecha", ascending=False)
    
    print("✅ Datos generados en memoria.")
    print(df.head(3)) # Muestra previa

    # ---------------------------------------------------------
    # 2. SUBIDA A GOOGLE CLOUD
    # ---------------------------------------------------------
    print(f"\n☁️ Conectando con Google Cloud Storage...")
    
    try:
        # Autenticación
        if os.path.exists(RUTA_SECRETS):
            credentials = service_account.Credentials.from_service_account_file(RUTA_SECRETS)
        else:
            raise FileNotFoundError(f"❌ No encuentro el archivo '{RUTA_SECRETS}'. Verifica la ruta.")

        client = storage.Client(credentials=credentials, project=credentials.project_id)
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(FILE_NAME)

        # Convertir DF a CSV String
        csv_string = df.to_csv(index=False)

        # Subir
        blob.upload_from_string(csv_string, content_type='text/csv')
        
        print(f"🚀 ¡ÉXITO! Archivo subido correctamente a:")
        print(f"   Bucket: {BUCKET_NAME}")
        print(f"   Archivo: {FILE_NAME}")
        print(f"   Registros: {len(df)}")

    except Exception as e:
        print(f"❌ Error al subir: {e}")

if __name__ == "__main__":
    generar_y_subir()
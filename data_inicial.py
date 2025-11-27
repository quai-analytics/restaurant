import pandas as pd
import numpy as np
import datetime
from google.cloud import storage
import io
import os
import json
from google.oauth2 import service_account

# --- CONFIGURACIÓN DE ACCESO (Igual que en tu app) ---
# Asegúrate de que esto apunte a tus credenciales correctas o usa tu setup existente
BUCKET_NAME = "data_quai_dev"
FILE_NAME = "restaurante_informes.csv" # OJO: Revisa si usas carpeta o no

# Si estás corriendo esto localmente, define tu cliente:
service_account_path = "secrets.json"
credentials = service_account.Credentials.from_service_account_file(service_account_path)
client = storage.Client(credentials=credentials, project=credentials.project_id)
bucket = client.bucket(BUCKET_NAME)

# NOTA: Si ya tienes las variables 'bucket' y 'guardar_df_en_bucket' definidas en tu entorno,
# puedes saltarte la configuración de arriba y usar solo la función de abajo.

def generar_datos_ficticios(dias=30):
    print(f"Generando datos para los últimos {dias} días...")
    
    fechas = []
    data = []
    
    fecha_fin = datetime.date.today()
    
    for i in range(dias):
        # 1. Fecha (vamos hacia atrás)
        fecha_actual = fecha_fin - datetime.timedelta(days=i)
        
        # 2. Ventas (Aleatorios pero realistas)
        venta_interna = round(np.random.uniform(200.0, 1500.0), 2)
        venta_delivery = round(np.random.uniform(50.0, 600.0), 2)
        venta_total = round(venta_interna + venta_delivery, 2)
        
        # 3. Tips (Aproximadamente el 10% de la venta, dividido)
        total_estimado_tips = venta_total * 0.10
        tip_visa = round(total_estimado_tips * 0.50, 2)     # 50% en Visa
        tip_amex = round(total_estimado_tips * 0.20, 2)     # 20% en Amex
        tip_efectivo = round(total_estimado_tips * 0.30, 2) # 30% en Efectivo
        tip_total = round(tip_visa + tip_amex + tip_efectivo, 2)
        
        # 4. Caja y Gastos
        saldo_inicial = 150.00 # Base fija o variable
        otros_ingresos = round(np.random.uniform(0.0, 50.0), 2)
        gastos = round(np.random.uniform(20.0, 300.0), 2)
        
        # 5. Cálculo de Total en Caja (Usando tu fórmula del formulario)
        # Formula: (Saldo Inicial + Venta Total + Tip Efectivo + Otros Ingresos) - Gastos
        # Nota: Ajusta esta fórmula si la Venta Total incluye tarjetas que no entran a caja física.
        # Por ahora uso tu lógica exacta:
        total_en_caja = round((saldo_inicial + venta_total + tip_efectivo + otros_ingresos) - gastos, 2)
        
        fila = {
            "Fecha": fecha_actual,
            "Venta Interna": venta_interna,
            "Venta Delivery": venta_delivery,
            "Venta Total": venta_total,
            "Tip Visa": tip_visa,
            "Tip Amex": tip_amex,
            "Tip Efectivo": tip_efectivo,
            "Tip Total": tip_total,
            "Otros Ingresos": otros_ingresos,
            "Gastos": gastos,
            "Saldo Inicial": saldo_inicial,
            "Total en Caja": total_en_caja
        }
        data.append(fila)

    # Crear DataFrame
    df = pd.DataFrame(data)
    
    # Ordenar por fecha descendente (más reciente arriba)
    df = df.sort_values(by="Fecha", ascending=False)
    
    return df

# --- EJECUCIÓN ---

# 1. Generamos el DataFrame
df_dummy = generar_datos_ficticios(dias=45) # Generamos 45 días de historia

# 2. Subimos al Bucket
# Asegúrate de tener disponible la función 'guardar_df_en_bucket' y la variable 'bucket'
# Si estás copiando esto en tu script principal, ya las tienes.

print("💾 Subiendo archivo masivo al bucket...")

# Usando tu función de guardado
csv_string = df_dummy.to_csv(index=False)
blob = bucket.blob(FILE_NAME) # <--- Asegúrate que FILE_NAME sea correcto (con o sin carpeta)
blob.upload_from_string(csv_string, content_type='text/csv')

print(f"✅ ¡Éxito! Se han creado {len(df_dummy)} registros en {FILE_NAME}")
print(df_dummy.head())
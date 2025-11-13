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

if 'informes_individual_df' not in st.session_state:
    st.session_state.informes_individual_df = pd.DataFrame(columns=[
        "Fecha",
        "Tipo de Pago",
        "Tipo de Venta",
        "Monto",
        "Tip",
        "Impuesto",
        "Sucursal",
        "Area"
    ])

# 'ultimo_calculo' guardará solo los datos del resumen de la derecha
if 'ultimo_calculo' not in st.session_state:
    st.session_state.ultimo_calculo = None

# Calculamos los totales del DataFrame
total_ventas = st.session_state.informes_individual_df['Monto'].sum()
total_impuestos = st.session_state.informes_individual_df['Impuesto'].sum()
total_tips = st.session_state.informes_individual_df['Tip'].sum()

# Mostramos las métricas en columnas
col_met1, col_met2, col_met3 = st.columns(3)

with col_met1:
    st.metric("Ventas Totales (Monto)", f"${total_ventas:.2f}")

with col_met2:
    st.metric("Total Impuestos", f"${total_impuestos:.2f}")

with col_met3:
    st.metric("Total Tips", f"${total_tips:.2f}")

st.divider()

# ----------------------------------------------
# --- El Formulario (Arriba) ---
st.header("Reporte de venta individual")

# Organizamos la pantalla en columnas
col_form, col_data = st.columns([0.7,0.3])
    
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

    with col_data:
        # --- Lógica de Procesamiento ---
        if submitted:

            # 1. Realizamos los cálculos
            total_venta = monto_venta + monto_tax + monto_tip

            # 2. Guardamos los datos para el resumen de la derecha
            st.session_state.ultimo_calculo = {
                "monto": monto_venta,
                "impuesto": monto_tax,
                "tip": monto_tip,
                "total": total_venta
            }

            # 3. Creamos la nueva fila para el DataFrame
            nueva_fila = pd.DataFrame([{
                "Fecha": fecha,
                "Tipo de Pago": modo_pago,
                "Tipo de Venta": tipo_venta,
                "Monto": monto_venta,
                "Tip": monto_tip,
                "Impuesto": monto_tax,
                "Sucursal": sucursal,
                "Area": area_venta
            }])
    
            # 4. Añadimos la nueva fila al historial
            st.session_state.informes_individual_df = pd.concat(
                [st.session_state.informes_individual_df, nueva_fila], 
                ignore_index=True
            )
            
            # Forzamos un 'rerun' para que el resumen se actualice instantáneamente
            st.rerun()

            st.subheader("Resumen de Venta Actual")

        # Botón de Limpiar
        if st.button("Limpiar Resumen"):
            # Esto borra el resumen de la derecha, pero no la tabla de abajo
            st.session_state.ultimo_calculo = None
            st.rerun()

        # Verificamos si hay algo en st.session_state.ultimo_calculo
        if st.session_state.ultimo_calculo:
            # Si hay datos (porque se dio 'Guardar'), los mostramos
            calculo = st.session_state.ultimo_calculo
            
            st.metric("Monto", f"${calculo['monto']:.2f}")
            st.metric("Impuesto", f"${calculo['impuesto']:.2f}")
            st.metric("Tip", f"${calculo['tip']:.2f}")
            st.divider()
            st.metric("GRAN TOTAL", f"${calculo['total']:.2f}")
    
        else:
            # Si no (al inicio, o después de 'Limpiar'), mostramos "---"
            st.metric("Monto", "---")
            st.metric("Impuesto", "---")
            st.metric("Tip", "---")
            st.divider()
            st.metric("GRAN TOTAL", "---")


st.divider()
st.header("Historial de Ventas Guardadas")

# Mostramos el DataFrame completo
st.dataframe(
    st.session_state.informes_individual_df, 
    use_container_width=True,
    hide_index=True
)
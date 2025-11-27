import streamlit as st
from utils import *

# --- CONFIGURACIÓN DE LA PÁGINA ---
# Esto debe ser lo primero que ejecutes.
st.set_page_config(
    page_title="Propuesta de Estrategia de IA",
    page_icon="🤖",
    layout="wide",  # 'wide' usa todo el ancho de la pantalla
    initial_sidebar_state="expanded" # 'expanded' mantiene la barra lateral abierta
)


# --- DATOS DEL CLIENTE (¡PERSONALIZA ESTO!) ---
# Cambia estos valores para cada propuesta que envíes
CLIENTE_NOMBRE = "[Nombre del Cliente]"
CLIENTE_PROBLEMA = "[Problema Principal del Cliente, ej: optimizar su logística]"
CLIENTE_INDUSTRIA = "[Industria del Cliente, ej: E-commerce]"

# --- TU INFORMACIÓN (Barra Lateral) ---
with st.sidebar:
    # Puedes poner tu logo aquí
    # st.image("path/a/tu/logo.png", width=150) 
    st.title("Tu Consultora de IA")
    st.markdown("---")
    st.header("Tu Contacto")
    st.markdown("**[Tu Nombre]**")
    st.markdown("*Consultor Principal de IA*")
    st.write("📧 email@tuconsultora.com")
    st.write("📞 +1 234 567 890")
    st.write("[Tu Sitio Web](https://www.tuconsultora.com)")


# --- SECCIÓN 1: PORTADA Y GANCHO ---
st.title(f"Propuesta de Estrategia de IA para {CLIENTE_NOMBRE}")
st.subheader(f"Cómo transformaremos su desafío de {CLIENTE_PROBLEMA} en una ventaja competitiva.")
st.divider()

# Elemento estrella: Video personalizado
st.markdown("### 🎥 Un mensaje para el equipo de " + CLIENTE_NOMBRE)
st.write("Haz clic para ver un breve resumen (2 min) de nuestra propuesta y por qué estamos emocionados de colaborar.")
# Reemplaza esta URL con un video tuyo (puedes subirlo a YouTube/Vimeo como "no listado")
st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Placeholder


# --- SECCIÓN 2: DIAGNÓSTICO ---
st.header("🔍 1. Nuestro Entendimiento de su Desafío")
st.markdown(f"""
Hemos analizado su situación actual en la industria de **{CLIENTE_INDUSTRIA}** y entendemos que sus principales desafíos son:
* Desafío clave 1 (ej: Tiempos de respuesta lentos en soporte).
* Desafío clave 2 (ej: Dificultad para predecir la demanda de inventario).
* Desafío clave 3 (ej: Procesos manuales que consumen mucho tiempo).
""")

col1, col2 = st.columns(2)
with col1:
    st.warning("El Costo de la Inacción", icon="⚠️")
    st.markdown("""
    * Pérdida de cuota de mercado frente a competidores más ágiles.
    * Incremento de costos operativos por ineficiencia.
    * Oportunidades de personalización perdidas.
    """)
with col2:
    st.success("La Oportunidad de la IA", icon="✨")
    st.markdown("""
    * Automatizar tareas repetitivas para liberar a su equipo.
    * Generar insights predictivos para tomar mejores decisiones.
    * Crear experiencias de cliente hiper-personalizadas.
    """)

st.divider()


# --- SECCIÓN 3: LA SOLUCIÓN (ROADMAP) ---
st.header("🗺️ 2. La Solución: Nuestra Hoja de Ruta (Roadmap)")
st.write("Proponemos un enfoque por fases, asegurando valor en cada etapa y mitigando riesgos.")

# Usamos st.tabs para un roadmap interactivo y limpio
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Fase 1: Descubrimiento", 
    "Fase 2: Estrategia", 
    "Fase 3: Prueba de Concepto (PoC)", 
    "Fase 4: Implementación",
    "Fase 5: Gobernanza"
])

with tab1:
    st.subheader("Fase 1: Descubrimiento y Auditoría de Datos (2 Semanas)")
    st.write("No se puede construir una casa sin cimientos. Aquí auditamos sus datos y procesos.")
    st.markdown("""
    **Entregables:**
    * ✅ **Informe de Madurez de Datos:** ¿Qué datos tienen? ¿Están listos para la IA?
    * ✅ **Taller de Ideación (Workshop):** Alineamos a su equipo con las posibilidades de la IA.
    * ✅ **Mapa de Procesos Actuales:** Identificamos cuellos de botella.
    """)

with tab2:
    st.subheader("Fase 2: Estrategia y Priorización (1 Semana)")
    st.write("Definimos dónde la IA generará el mayor impacto, más rápido (Quick-Wins).")
    st.markdown("""
    **Entregables:**
    * ✅ **Matriz de Priorización de Casos de Uso:** Un ranking claro de proyectos (Impacto vs. Esfuerzo).
    * ✅ **Hoja de Ruta Estratégica de IA:** La visión a 12-24 meses.
    * ✅ **Caso de Negocio para el Piloto:** Definición del primer proyecto (PoC).
    """)

with tab3:
    st.subheader("Fase 3: Prueba de Concepto - PoC (4-6 Semanas)")
    st.write("Demostramos valor real con un proyecto piloto enfocado en su caso de uso prioritario.")
    st.markdown("""
    **Entregables:**
    * ✅ **Piloto de IA Funcional:** Un modelo entrenado y probado (ej: un chatbot de soporte, un modelo de predicción).
    * ✅ **Informe de Resultados del Piloto:** Métricas claras de éxito (ej: precisión del modelo, tiempo ahorrado).
    * ✅ **Plan de Implementación a Escala.**
    """)
    
with tab4:
    st.subheader("Fase 4: Implementación e Integración (Variable)")
    st.write("Llevamos el piloto a producción y lo integramos con sus sistemas existentes (CRM, ERP, etc.)")
    st.markdown("""
    **Entregables:**
    * ✅ **Solución de IA en Producción:** Totalmente operativa y escalable.
    * ✅ **APIs y Conectores:** Integración limpia con su stack tecnológico.
    * ✅ **Dashboards de Monitoreo:** Paneles para ver el rendimiento de la IA en tiempo real.
    """)

with tab5:
    st.subheader("Fase 5: Capacitación y Gobernanza (Continuo)")
    st.write("Aseguramos la adopción y el uso ético y responsable de la IA en su organización.")
    st.markdown("""
    **Entregables:**
    * ✅ **Manual de Gobernanza de IA:** Directrices sobre ética, privacidad y uso responsable.
    * ✅ **Sesiones de Capacitación:** Entrenamos a sus equipos para usar las nuevas herramientas.
    * ✅ **Plan de Mantenimiento y Mejora:** La IA necesita evolucionar; definimos cómo.
    """)

st.divider()

# --- SECCIÓN 4: ¿POR QUÉ NOSOTROS? (PRUEBA SOCIAL) ---
st.header("🏆 3. ¿Por Qué Nosotros?")
st.write(f"Entendemos la industria de **{CLIENTE_INDUSTRIA}**. No solo somos expertos en IA, somos expertos en aplicar IA a sus problemas de negocio.")

st.subheader("Casos de Éxito Relevantes")

col1, col2 = st.columns(2)
with col1:
    st.info("Caso de Éxito: [Cliente Similar 1 - Ej: RetailCo]")
    st.markdown("""
    * **Problema:** Alta tasa de abandono de carrito.
    * **Solución:** Implementamos un motor de recomendación personalizado en tiempo real.
    * **Resultado:**
    """)
    st.metric(label="Aumento en Tasa de Conversión", value="18%", delta="Positivo")

with col2:
    st.info("Caso de Éxito: [Cliente Similar 2 - Ej: LogistiTech]")
    st.markdown("""
    * **Problema:** Rutas de entrega ineficientes.
    * **Solución:** Desarrollamos un modelo de optimización de rutas usando IA.
    * **Resultado:**
    """)
    st.metric(label="Reducción de Costos de Combustible", value="22%", delta="-22% (Reducción)")

# Tu equipo
st.subheader("Su Equipo de Expertos")
col1, col2, col3 = st.columns(3)
with col1:
    # st.image("path/a/foto1.png")
    st.markdown("**Dra. Ana Silva**\n*PhD, Data Science Lead*")
    st.write("Experta en modelos predictivos y NLP.")
with col2:
    # st.image("path/a/foto2.png")
    st.markdown("**Ing. Marco Rojas**\n*IA & Cloud Architect*")
    st.write("Especialista en MLOps y escalado en AWS/GCP.")
with col3:
    # st.image("path/a/foto3.png")
    st.markdown("**[Tu Nombre]**\n*Estratega de IA & Project Lead*")
    st.write("Su punto de contacto directo para el éxito del proyecto.")

st.divider()

# --- SECCIÓN 5: INVERSIÓN Y ROI ---
st.header("💰 4. Inversión y Retorno (ROI)")

# Elemento estrella: Calculadora de ROI
st.subheader("Calculadora de ROI Interactiva")
st.write("Juegue con estas cifras para estimar el impacto potencial. Esta es una herramienta clave para validar la inversión.")

# Inputs del usuario
horas_por_tarea = st.slider("Horas ahorradas por empleado a la semana (gracias a la IA)", 0.5, 10.0, 3.0, 0.5)
num_empleados = st.slider("Número de empleados que usarán la nueva herramienta", 1, 500, 20)
coste_por_hora = st.number_input("Coste promedio por hora de empleado ($)", min_value=10, max_value=200, value=30, step=5)

# Cálculo
ahorro_semanal = horas_por_tarea * num_empleados * coste_por_hora
ahorro_mensual = ahorro_semanal * 4.33
ahorro_anual = ahorro_mensual * 12

st.success(f"**Ahorro Anual Estimado: ${ahorro_anual:,.2f}**")
st.write(f"Este cálculo se basa en un ahorro de {horas_por_tarea} horas semanales por {num_empleados} empleados. "
         f"Nuestra propuesta busca materializar esta cifra.")


# Paquetes de Inversión
st.subheader("Su Inversión")
st.write("Ofrecemos opciones claras y transparentes. Recomendamos el paquete 'Estratégico' para {CLIENTE_NOMBRE}.")

pkg1, pkg2, pkg3 = st.tabs(["Fases 1+2: Descubrimiento y Estrategia", 
                          "Fases 1-3: Paquete Estratégico (Recomendado)", 
                          "Fases 1-5: Proyecto Completo"])

with pkg1:
    st.markdown("""
    Ideal para organizaciones que necesitan claridad antes de una gran inversión.
    * Incluye **Fase 1** (Descubrimiento)
    * Incluye **Fase 2** (Estrategia y Roadmap)
    """)
    st.subheader("Precio: $XX.XXX")

with pkg2:
    st.markdown("""
    **La opción más popular.** Define la estrategia y demuestra el valor con un piloto funcional.
    * Incluye **Fase 1** (Descubrimiento)
    * Incluye **Fase 2** (Estrategia)
    * Incluye **Fase 3** (Prueba de Concepto - PoC)
    """)
    st.subheader("Precio: $XX.XXX")

with pkg3:
    st.markdown("""
    La transformación completa. De la idea a la implementación y gobernanza.
    * Incluye **Todas las Fases (1 a 5)**
    """)
    st.subheader("Precio: $XXX.XXX")

st.divider()

# --- SECCIÓN 6: PRÓXIMOS PASOS (CTA) ---
st.header("🏁 5. Próximos Pasos")
st.write(f"Estamos listos para ayudar a {CLIENTE_NOMBRE} a liderar con IA. "
         "El siguiente paso es una reunión de 30 minutos para discutir esta propuesta y ajustar el alcance.")

col1, col2 = st.columns(2)

with col1:
    # Reemplaza esto con tu enlace real de Calendly, HubSpot, etc.
    st.link_button("Agendar Reunión de Inicio (30 min)", "https://calendly.com/tu-usuario", type="primary")

with col2:
    if st.button("Aprobar Propuesta Digitalmente"):
        st.success("¡Excelente decisión! Hemos sido notificados. Nos pondremos en contacto en breve para formalizar el inicio.")
        # Aquí podrías agregar una lógica para enviar un email
        st.balloons()
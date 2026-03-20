"""
MI ASISTENTE IA - VERSIÓN WEB (CORREGIDA)
Funciona sin google.colab
"""

import streamlit as st
import matplotlib.pyplot as plt
import io
from datetime import datetime

# ============================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================
st.set_page_config(
    page_title="Mi Asistente IA",
    page_icon="🤖",
    layout="wide"
)

# ============================================
# TÍTULO
# ============================================
st.title("🤖 Mi Asistente IA Personal")
st.markdown("---")

# ============================================
# INICIALIZAR VARIABLES
# ============================================
if 'mensajes' not in st.session_state:
    st.session_state.mensajes = []

# ============================================
# BARRA LATERAL
# ============================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/robot-2.png", width=80)
    st.title("⚙️ Configuración")
    
    st.markdown("---")
    st.info("📌 **Cómo usar:**")
    st.write("1. Escribe tu pregunta en el chat")
    st.write("2. Crea gráficas en la pestaña Gráficas")
    st.write("3. Comparte esta URL con otros")
    
    st.markdown("---")
    st.caption(f"🕒 {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    st.caption("👥 Compatible con celular y computador")

# ============================================
# FUNCIÓN PARA CREAR GRÁFICA
# ============================================
def crear_grafica(datos, tipo, titulo):
    plt.figure(figsize=(10, 6))
    
    if tipo == "Barras":
        plt.bar(datos.keys(), datos.values(), color='skyblue', edgecolor='navy')
        plt.grid(True, alpha=0.3, axis='y')
    elif tipo == "Líneas":
        plt.plot(list(datos.keys()), list(datos.values()), marker='o', linewidth=2, markersize=8, color='green')
        plt.grid(True, alpha=0.3)
    elif tipo == "Pastel":
        plt.pie(datos.values(), labels=datos.keys(), autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    
    plt.title(titulo, fontsize=14, fontweight='bold')
    
    # Guardar en memoria
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return buf

# ============================================
# PESTAÑAS
# ============================================
tab1, tab2 = st.tabs(["💬 CHAT", "📊 GRÁFICAS"])

# ============================================
# TAB 1: CHAT
# ============================================
with tab1:
    st.header("💬 Conversa con tu asistente")
    
    # Mostrar mensajes
    for msg in st.session_state.mensajes:
        if msg["rol"] == "usuario":
            st.markdown(f'<div style="background-color:#e3f2fd; padding:10px; border-radius:10px; margin:5px 0;">👤 <strong>Tú:</strong> {msg["texto"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background-color:#f5f5f5; padding:10px; border-radius:10px; margin:5px 0;">🤖 <strong>Asistente:</strong> {msg["texto"]}</div>', unsafe_allow_html=True)
    
    # Input del usuario
    col1, col2 = st.columns([5, 1])
    with col1:
        pregunta = st.text_input("Escribe tu pregunta:", placeholder="Ej: ¿Cómo creo una gráfica? o Dame un consejo...", key="pregunta")
    with col2:
        enviar = st.button("📤 Enviar", use_container_width=True)
    
    if enviar and pregunta:
        # Guardar pregunta
        st.session_state.mensajes.append({"rol": "usuario", "texto": pregunta})
        
        # Respuesta simple (funciona sin API)
        respuesta = f"✅ Recibí tu pregunta: '{pregunta}'\n\n📌 Puedes crear gráficas en la pestaña 'GRÁFICAS'.\n\n💡 Pronto podré responder con más inteligencia cuando conectes una API de IA."
        
        # Guardar respuesta
        st.session_state.mensajes.append({"rol": "asistente", "texto": respuesta})
        
        # Recargar
        st.rerun()

# ============================================
# TAB 2: GRÁFICAS
# ============================================
with tab2:
    st.header("📊 Crea gráficas fácilmente")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Ingresa tus datos")
        
        # Opción de datos
        opcion_datos = st.radio("¿Cómo quieres los datos?", ["Usar ejemplo", "Ingresar manual"])
        
        datos = {}
        
        if opcion_datos == "Usar ejemplo":
            datos = {
                "Enero": 45000,
                "Febrero": 52000,
                "Marzo": 48000,
                "Abril": 61000,
                "Mayo": 58000
            }
            st.success("✅ Datos de ejemplo cargados:")
            for k, v in datos.items():
                st.write(f"• {k}: ${v:,.0f}")
        
        else:
            num_datos = st.number_input("Número de categorías:", 2, 10, 4)
            
            for i in range(num_datos):
                col_a, col_b = st.columns(2)
                with col_a:
                    nombre = st.text_input(f"Nombre {i+1}", f"Item {i+1}", key=f"nom_{i}")
                with col_b:
                    valor = st.number_input(f"Valor {i+1}", 0, 100000, 1000, key=f"val_{i}")
                datos[nombre] = valor
    
    with col2:
        st.subheader("2. Configuración de la gráfica")
        
        tipo_grafica = st.selectbox(
            "Tipo de gráfica:",
            ["Barras", "Líneas", "Pastel"],
            help="Barras: compara valores | Líneas: muestra tendencias | Pastel: muestra porcentajes"
        )
        
        titulo_grafica = st.text_input("Título de la gráfica:", "Mi Gráfica")
        
        if st.button("🎨 GENERAR GRÁFICA", use_container_width=True, type="primary"):
            if datos:
                with st.spinner("Generando gráfica..."):
                    # Crear gráfica
                    imagen = crear_grafica(datos, tipo_grafica, titulo_grafica)
                    
                    # Mostrar
                    st.image(imagen, caption=titulo_grafica, use_container_width=True)
                    
                    # Botón para descargar
                    st.download_button(
                        label="💾 DESCARGAR COMO PNG",
                        data=imagen,
                        file_name=f"{titulo_grafica.replace(' ', '_')}.png",
                        mime="image/png",
                        use_container_width=True
                    )
                    
                    st.success("✅ Gráfica generada exitosamente!")
            else:
                st.warning("⚠️ Ingresa datos primero")

# ============================================
# PIE DE PÁGINA
# ============================================
st.markdown("---")
st.caption("💡 **Tips:** Esta app funciona en celular y computador. Crea gráficas con tus propios datos o usa los ejemplos.")
st.caption("📱 Compatible con todos los dispositivos")

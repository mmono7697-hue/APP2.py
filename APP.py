"""
MI ASISTENTE IA - VERSIÓN WEB
Funciona en celular y computador
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import google.generativeai as genai
from googleapiclient.discovery import build
from google.colab import auth
import io

# ============================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================
st.set_page_config(
    page_title="Mi Asistente IA",
    page_icon="🤖",
    layout="wide"
)

# ============================================
# INICIALIZAR VARIABLES
# ============================================
if 'mensajes' not in st.session_state:
    st.session_state.mensajes = []
if 'drive_conectado' not in st.session_state:
    st.session_state.drive_conectado = False
if 'gemini_listo' not in st.session_state:
    st.session_state.gemini_listo = False

# ============================================
# BARRA LATERAL (donde cada usuario se conecta)
# ============================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/robot-2.png", width=80)
    st.title("⚙️ CONFIGURACIÓN")
    
    st.markdown("---")
    st.subheader("🤖 1. Conectar Gemini (IA)")
    
    # Cada usuario pone su propia API Key
    api_key = st.text_input(
        "Tu API Key de Gemini:",
        type="password",
        placeholder="Ej: AIzaSyD1234567890..."
    )
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.session_state.modelo = genai.GenerativeModel('gemini-1.5-flash')
            st.session_state.gemini_listo = True
            st.success("✅ Gemini conectado")
        except:
            st.error("❌ API Key inválida")
    else:
        st.warning("⚠️ Necesitas una API Key")
        st.caption("📌 Cómo obtenerla: aistudio.google.com → Get API Key")
    
    st.markdown("---")
    st.subheader("📁 2. Conectar Google Drive")
    
    if st.button("🔑 Conectar mi Drive", use_container_width=True):
        try:
            auth.authenticate_user()
            st.session_state.drive = build('drive', 'v3')
            st.session_state.docs = build('docs', 'v1')
            st.session_state.slides = build('slides', 'v1')
            st.session_state.drive_conectado = True
            st.success("✅ Drive conectado")
        except Exception as e:
            st.error(f"Error: {e}")
    
    if st.session_state.drive_conectado:
        st.info("📁 Drive: Conectado")
    else:
        st.warning("📁 Drive: No conectado")
    
    st.markdown("---")
    st.caption("👥 Comparte esta URL con hasta 3 usuarios")
    st.caption("Cada usuario usa sus propias credenciales")

# ============================================
# TÍTULO PRINCIPAL
# ============================================
st.title("🤖 Mi Asistente IA Personal")
st.markdown("---")

# ============================================
# FUNCIÓN PARA RESPONDER
# ============================================
def responder(pregunta):
    if not st.session_state.gemini_listo:
        return "⚠️ Primero conecta Gemini en la barra lateral (pon tu API Key)"
    
    prompt = f"""
    Eres un asistente personal útil y amigable.
    
    Pregunta: {pregunta}
    
    Responde de manera clara y útil.
    """
    
    try:
        respuesta = st.session_state.modelo.generate_content(prompt)
        return respuesta.text
    except Exception as e:
        return f"Error: {e}"

# ============================================
# CREAR GRÁFICA
# ============================================
def crear_grafica(datos, tipo, titulo):
    plt.figure(figsize=(10, 6))
    
    if tipo == "Barras":
        plt.bar(datos.keys(), datos.values(), color='skyblue')
    elif tipo == "Líneas":
        plt.plot(list(datos.keys()), list(datos.values()), marker='o')
    elif tipo == "Pastel":
        plt.pie(datos.values(), labels=datos.keys(), autopct='%1.1f%%')
    
    plt.title(titulo)
    plt.grid(True, alpha=0.3)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return buf

# ============================================
# PESTAÑAS
# ============================================
tab1, tab2, tab3 = st.tabs(["💬 CHAT", "📊 GRÁFICAS", "📁 DRIVE"])

# ============================================
# TAB 1: CHAT
# ============================================
with tab1:
    st.header("💬 Conversa con tu asistente")
    
    # Mostrar mensajes
    for msg in st.session_state.mensajes:
        if msg["rol"] == "usuario":
            st.markdown(f"👤 **Tú:** {msg['texto']}")
        else:
            st.markdown(f"🤖 **Asistente:** {msg['texto']}")
    
    # Input del usuario
    pregunta = st.text_input("Escribe tu pregunta:", key="pregunta")
    
    col1, col2 = st.columns([1, 5])
    with col1:
        enviar = st.button("📤 Enviar", use_container_width=True)
    
    if enviar and pregunta:
        # Guardar pregunta
        st.session_state.mensajes.append({"rol": "usuario", "texto": pregunta})
        
        # Obtener respuesta
        with st.spinner("Pensando..."):
            respuesta_texto = responder(pregunta)
        
        # Guardar respuesta
        st.session_state.mensajes.append({"rol": "asistente", "texto": respuesta_texto})
        
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
        
        num_datos = st.number_input("¿Cuántos datos?", 2, 10, 4)
        
        datos = {}
        for i in range(num_datos):
            col_a, col_b = st.columns(2)
            with col_a:
                nombre = st.text_input(f"Nombre {i+1}", f"Item {i+1}", key=f"nom_{i}")
            with col_b:
                valor = st.number_input(f"Valor {i+1}", 0, 10000, 100, key=f"val_{i}")
            datos[nombre] = valor
        
        # Ejemplo rápido
        if st.button("📋 Usar ejemplo"):
            datos = {"Enero": 45000, "Febrero": 52000, "Marzo": 48000, "Abril": 61000}
            st.rerun()
    
    with col2:
        st.subheader("2. Configuración")
        
        tipo = st.selectbox("Tipo de gráfica:", ["Barras", "Líneas", "Pastel"])
        titulo = st.text_input("Título:", "Mi Gráfica")
        
        if st.button("🎨 GENERAR GRÁFICA", use_container_width=True):
            if datos:
                imagen = crear_grafica(datos, tipo, titulo)
                st.image(imagen, caption=titulo)
                
                # Descargar
                st.download_button(
                    label="💾 DESCARGAR PNG",
                    data=imagen,
                    file_name=f"{titulo}.png",
                    mime="image/png"
                )
            else:
                st.warning("Ingresa datos primero")

# ============================================
# TAB 3: DRIVE
# ============================================
with tab3:
    st.header("📁 Google Drive")
    
    if not st.session_state.drive_conectado:
        st.warning("⚠️ Conecta Google Drive en la barra lateral")
    else:
        st.success("✅ Drive conectado")
        
        if st.button("📂 Ver mis archivos"):
            with st.spinner("Cargando..."):
                try:
                    resultados = st.session_state.drive.files().list(
                        pageSize=10,
                        fields="files(id, name, modifiedTime)"
                    ).execute()
                    
                    archivos = resultados.get('files', [])
                    
                    for archivo in archivos:
                        st.write(f"📄 {archivo['name']}")
                except Exception as e:
                    st.error(f"Error: {e}")

# ============================================
# PIE DE PÁGINA
# ============================================
st.markdown("---")
st.caption("💡 Para usar: 1) Conecta Gemini (API Key) | 2) Conecta Drive | 3) Empieza a chatear")
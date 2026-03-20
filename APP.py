"""
MI ASISTENTE IA - CON GOOGLE DRIVE
Acceso a documentos, gráficas y creación de archivos
"""

import streamlit as st
import matplotlib.pyplot as plt
import io
import pandas as pd
from datetime import datetime
import json

# ============================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================
st.set_page_config(
    page_title="Mi Asistente IA",
    page_icon="🤖",
    layout="wide"
)

# ============================================
# INICIALIZAR VARIABLES DE SESIÓN
# ============================================
if 'mensajes' not in st.session_state:
    st.session_state.mensajes = []
if 'drive_token' not in st.session_state:
    st.session_state.drive_token = None
if 'drive_conectado' not in st.session_state:
    st.session_state.drive_conectado = False

# ============================================
# BARRA LATERAL - CONFIGURACIÓN
# ============================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/robot-2.png", width=80)
    st.title("⚙️ Configuración")
    
    st.markdown("---")
    
    # ========================================
    # SECCIÓN DE GOOGLE DRIVE
    # ========================================
    st.subheader("📁 Google Drive")
    
    st.info("""
    **Para conectar Google Drive:**
    
    1. Necesitas un token de acceso
    2. Cada usuario conecta su propio Drive
    3. Los archivos se guardan en tu Drive personal
    """)
    
    # Opción 1: Token manual (para pruebas)
    token_manual = st.text_input(
        "Token de acceso (opcional):",
        type="password",
        placeholder="Pega tu token aquí..."
    )
    
    if token_manual:
        st.session_state.drive_token = token_manual
        st.session_state.drive_conectado = True
        st.success("✅ Token guardado")
    
    # Opción 2: Simulación de Drive (para pruebas)
    if not st.session_state.drive_conectado:
        if st.button("🔌 Usar modo simulación (pruebas)", use_container_width=True):
            st.session_state.drive_conectado = True
            st.session_state.modo_simulacion = True
            st.success("✅ Modo simulación activado")
            st.rerun()
    
    if st.session_state.drive_conectado:
        st.success("📁 Drive: Conectado")
        
        # Mostrar carpetas simuladas
        if 'modo_simulacion' in st.session_state:
            st.info("📂 Modo simulación - archivos guardados localmente")
        
        if st.button("📂 Ver mis archivos", use_container_width=True):
            st.session_state.mostrar_archivos = True
    
    st.markdown("---")
    st.caption(f"👥 Comparte esta URL con tus usuarios")
    st.caption(f"🕒 {datetime.now().strftime('%d/%m/%Y')}")

# ============================================
# FUNCIONES DE DRIVE (SIMULADAS PARA PRUEBAS)
# ============================================

def guardar_en_drive(nombre_archivo, contenido, tipo="texto"):
    """Guarda un archivo en Drive (simulado)"""
    
    # Inicializar almacenamiento si no existe
    if 'archivos_guardados' not in st.session_state:
        st.session_state.archivos_guardados = []
    
    # Crear archivo simulado
    archivo = {
        "nombre": nombre_archivo,
        "tipo": tipo,
        "contenido": contenido,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "url": f"https://drive.google.com/file/d/simulado_{len(st.session_state.archivos_guardados)}"
    }
    
    st.session_state.archivos_guardados.append(archivo)
    
    return archivo["url"]

def listar_archivos_drive():
    """Lista archivos simulados"""
    if 'archivos_guardados' not in st.session_state:
        return []
    return st.session_state.archivos_guardados

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
        plt.pie(datos.values(), labels=datos.keys(), autopct='%1.1f%%')
    
    plt.title(titulo, fontsize=14, fontweight='bold')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return buf

# ============================================
# FUNCIÓN PARA CREAR DOCUMENTO
# ============================================
def crear_documento(titulo, contenido):
    """Crea un documento de texto"""
    doc = f"""
    📄 DOCUMENTO: {titulo}
    📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}
    {'='*50}
    
    {contenido}
    
    {'='*50}
    Creado con Mi Asistente IA
    """
    return doc

# ============================================
# TÍTULO PRINCIPAL
# ============================================
st.title("🤖 Mi Asistente IA Personal")
st.markdown("---")

# ============================================
# PESTAÑAS
# ============================================
tab1, tab2, tab3, tab4 = st.tabs(["💬 CHAT", "📊 GRÁFICAS", "📝 DOCUMENTOS", "📁 MIS ARCHIVOS"])

# ============================================
# TAB 1: CHAT
# ============================================
with tab1:
    st.header("💬 Conversa con tu asistente")
    
    # Mostrar mensajes
    for msg in st.session_state.mensajes:
        if msg["rol"] == "usuario":
            st.markdown(f'👤 **Tú:** {msg["texto"]}')
        else:
            st.markdown(f'🤖 **Asistente:** {msg["texto"]}')
    
    # Input
    col1, col2 = st.columns([5, 1])
    with col1:
        pregunta = st.text_input("Escribe tu pregunta:", key="pregunta", placeholder="Ej: ¿Cómo creo una gráfica?")
    with col2:
        enviar = st.button("📤 Enviar", use_container_width=True)
    
    if enviar and pregunta:
        st.session_state.mensajes.append({"rol": "usuario", "texto": pregunta})
        
        # Respuesta
        respuesta = f"✅ Recibí tu pregunta.\n\n📌 Puedes crear gráficas en la pestaña 'GRÁFICAS'\n📝 Crear documentos en 'DOCUMENTOS'\n📁 Ver archivos guardados en 'MIS ARCHIVOS'"
        
        st.session_state.mensajes.append({"rol": "asistente", "texto": respuesta})
        st.rerun()

# ============================================
# TAB 2: GRÁFICAS (CON GUARDADO EN DRIVE)
# ============================================
with tab2:
    st.header("📊 Crear gráficas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Datos")
        
        # Datos de ejemplo
        datos_ejemplo = {
            "Enero": 45000,
            "Febrero": 52000,
            "Marzo": 48000,
            "Abril": 61000
        }
        
        usar_ejemplo = st.checkbox("Usar datos de ejemplo", value=True)
        
        if usar_ejemplo:
            datos = datos_ejemplo
            for k, v in datos.items():
                st.write(f"• {k}: ${v:,.0f}")
        else:
            num = st.number_input("Número de categorías:", 2, 10, 4)
            datos = {}
            for i in range(num):
                col_a, col_b = st.columns(2)
                with col_a:
                    nombre = st.text_input(f"Nombre {i+1}", f"Item {i+1}", key=f"nom_{i}")
                with col_b:
                    valor = st.number_input(f"Valor {i+1}", 0, 100000, 1000, key=f"val_{i}")
                datos[nombre] = valor
    
    with col2:
        st.subheader("Configuración")
        
        tipo = st.selectbox("Tipo", ["Barras", "Líneas", "Pastel"])
        titulo = st.text_input("Título", "Mi Gráfica")
        
        if st.button("🎨 GENERAR GRÁFICA", use_container_width=True):
            if datos:
                imagen = crear_grafica(datos, tipo, titulo)
                st.image(imagen, caption=titulo)
                
                # Descargar
                st.download_button("💾 Descargar PNG", imagen, f"{titulo}.png")
                
                # Guardar en Drive
                if st.session_state.drive_conectado:
                    if st.button("☁️ Guardar en Drive", use_container_width=True):
                        url = guardar_en_drive(f"{titulo}.png", imagen, "imagen")
                        st.success(f"✅ Guardado en Drive: [Ver]({url})")
            else:
                st.warning("Ingresa datos")

# ============================================
# TAB 3: DOCUMENTOS
# ============================================
with tab3:
    st.header("📝 Crear documentos")
    
    titulo_doc = st.text_input("Título del documento:", "Mi Documento")
    contenido_doc = st.text_area(
        "Contenido:",
        height=300,
        value="# Título Principal\n\nEscribe aquí tu contenido...\n\n- Punto 1\n- Punto 2"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 CREAR DOCUMENTO", use_container_width=True):
            doc = crear_documento(titulo_doc, contenido_doc)
            
            # Mostrar
            st.text_area("Vista previa:", doc, height=200)
            
            # Guardar en Drive
            if st.session_state.drive_conectado:
                url = guardar_en_drive(f"{titulo_doc}.txt", doc, "documento")
                st.success(f"✅ Documento guardado en Drive")
                st.markdown(f"[Abrir documento]({url})")
            else:
                st.warning("Conecta Drive para guardar")
    
    with col2:
        st.info("💡 **Tips:**\n- Usa # para títulos\n- Usa - para listas\n- El documento se guarda automáticamente en Drive")

# ============================================
# TAB 4: MIS ARCHIVOS
# ============================================
with tab4:
    st.header("📁 Mis archivos en Drive")
    
    if not st.session_state.drive_conectado:
        st.warning("⚠️ Conecta Google Drive en la barra lateral")
        st.info("Haz clic en 'Usar modo simulación' para probar")
    else:
        archivos = listar_archivos_drive()
        
        if not archivos:
            st.info("No tienes archivos guardados aún. Crea gráficas o documentos para guardarlos.")
        else:
            for archivo in archivos:
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.write(f"📄 **{archivo['nombre']}**")
                    with col2:
                        st.write(f"📅 {archivo['fecha']}")
                    with col3:
                        st.write(f"🔗 [Ver]({archivo['url']})")
                st.markdown("---")

# ============================================
# PIE DE PÁGINA
# ============================================
st.markdown("---")
st.caption("💡 **Comparte esta URL con tus usuarios | Cada usuario conecta su propio Drive**")

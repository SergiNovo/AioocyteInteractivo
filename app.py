import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

# Configurar página
st.set_page_config(page_title="Vitrification Viability via Osmotic Response", layout="wide")
st.markdown("<h1 style='text-align: center;'>Vitrification Viability via Osmotic Response</h1>", unsafe_allow_html=True)

# Cargar datos
df = pd.read_csv("AioocyteV1.csv", sep=";")
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace('%', '', regex=False)
        df[col] = df[col].str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Estado inicial
if "second" not in st.session_state:
    st.session_state.second = 0
if "playing" not in st.session_state:
    st.session_state.playing = False
if "speed" not in st.session_state:
    st.session_state.speed = 1

# --- Estructura visual vertical (mobile friendly) ---
slider_placeholder = st.empty()
video_placeholder = st.empty()
supervivencia_placeholder = st.empty()
metrics_placeholder = st.empty()
grafico_placeholder = st.empty()
controles_placeholder = st.empty()
logo_placeholder = st.empty()

def mostrar_contenido():
    frame_path = f"frames/frame_{st.session_state.second}.jpg"
    with video_placeholder:
        if os.path.exists(frame_path):
            image = Image.open(frame_path)
            st.image(image, caption=f"second {st.session_state.second}", use_container_width=True)
        else:
            st.warning("No se encontró imagen.")

    dato = df.iloc[st.session_state.second]
    with supervivencia_placeholder:
        st.markdown(f"""
            <div style='text-align: center; margin-top: 1px;'>
                <div style='font-size: 40px; font-weight: bold; color: #005EA8;'>
                    {dato['Survival']:.1f}%
                </div>
                <div style='font-size: 16px; color: #444;'>Probability of oocyte survival after vitrification</div>
            </div>
            <hr style="margin: 1px 0;">
        """, unsafe_allow_html=True)

    with metrics_placeholder:
        # Métricas una debajo de otra para móvil
        st.markdown(
            f"""
            <div style='display: flex; flex-direction: column; align-items: center; justify-content: center;'>
                <div style='margin-bottom: 4px;'><b>Area %</b>: {dato['Area%']:.3f}</div>
                <div style='margin-bottom: 4px;'><b>Circularity</b>: {dato['Circularity']:.3f}</div>
                <div style='margin-bottom: 4px;'><b>Dehydration rate %/s</b>: {dato['Vdeshidratacion']:.2f}%</div>
                <div><b>Deplasmolysis rate %/s</b>: {dato['Vdeplasmolisi']:.2f}%</div>
            </div>
            """, unsafe_allow_html=True
        )

    with grafico_placeholder:
        st.image("slider_background_final.png", use_container_width=True)

def render_slider():
    with slider_placeholder:
        selected = st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed")
        if selected != st.session_state.second:
            st.session_state.second = selected
            st.session_state.playing = False
            mostrar_contenido()

# Render contenido inicial
render_slider()
mostrar_contenido()

# Controles: 3 por línea para móvil, o todos en una sola línea con saltos
with controles_placeholder:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⏪ Back"):
            st.session_state.second = max(0, st.session_state.second - 1)
            st.session_state.playing = False
            mostrar_contenido()
            render_slider()
    with col2:
        if st.button("▶️ Play 1x"):
            st.session_state.playing = True
            st.session_state.speed = 1
    with col3:
        if st.button("⏩ Forward"):
            st.session_state.second = min(359, st.session_state.second + 1)
            st.session_state.playing = False
            mostrar_contenido()
            render_slider()

    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("⏸️ Pause"):
            st.session_state.playing = False
    with col5:
        if st.button("⏹️ Stop"):
            st.session_state.playing = False
            st.session_state.second = 0
            mostrar_contenido()
            render_slider()
    with col6:
        if st.button("⏩ Play 5x"):
            st.session_state.playing = True
            st.session_state.speed = 5

# Reproducción automática
if st.session_state.playing:
    for _ in range(500):
        if not st.session_state.playing or st.session_state.second >= 359:
            st.session_state.playing = False
            break
        time.sleep(0.5)
        st.session_state.second = min(359, st.session_state.second + st.session_state.speed)
        mostrar_contenido()
        render_slider()

# Logo debajo de todo
with logo_placeholder:
    st.markdown("""
    <div style='text-align: center; margin-top: 10px;'>
        <a href='https://www.fertilab.com' target='_blank'>
            <img src='https://redinfertiles.com/wp-content/uploads/2022/04/logo-Barcelona.png' 
                 alt='Fertilab Barcelona' width='160'/>
        </a>
    </div>
    """, unsafe_allow_html=True)

import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

# Configuración de la página
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

# Estructura
col_video, col_datos = st.columns([2, 3])
video_placeholder = col_video.empty()
supervivencia_placeholder = col_datos.empty()
metrics_placeholder = col_datos.empty()
grafico_placeholder = col_datos.empty()
slider_placeholder = col_datos.empty()
controles_placeholder = col_datos.empty()

# Mostrar contenido
def mostrar_contenido():
    frame_path = f"frames/frame_{st.session_state.second}.jpg"
    with video_placeholder:
        if os.path.exists(frame_path):
            st.image(Image.open(frame_path), caption=f"Second {st.session_state.second}", use_container_width=True)
        else:
            st.warning("No se encontró imagen.")
    
    dato = df.iloc[st.session_state.second]
    with supervivencia_placeholder:
        st.markdown(f"""
            <div style='text-align: center; margin-top: 1px;'>
                <div style='font-size: 64px; font-weight: bold; color: #005EA8;'>
                    {dato['Survival']:.1f}%
                </div>
                <div style='font-size: 20px; color: #444;'>Probability of oocyte survival after vitrification</div>
            </div>
        """, unsafe_allow_html=True)
    
    with metrics_placeholder:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Area %", f"{dato['Area%']:.3f}")
        m2.metric("Circularity", f"{dato['Circularity']:.3f}")
        m3.metric("Dehydration rate %/s", f"{dato['Vdeshidratacion']:.2f}%")
        m4.metric("Deplasmolysis rate %/s", f"{dato['Vdeplasmolisi']:.2f}%")
        st.markdown("</div>", unsafe_allow_html=True)

    with grafico_placeholder:
        st.image("slider_background_final.png", use_container_width=True)

# Slider
def render_slider():
    with slider_placeholder:
        selected = st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed", key="slider_key")
        if selected != st.session_state.second:
            st.session_state.second = selected
            st.session_state.playing = False
            mostrar_contenido()

mostrar_contenido()
render_slider()

# Controles
with controles_placeholder:
    b1, b2, b3, b4, b5, b6 = st.columns(6)
    with b1:
        if st.button("⏪ Back"):
            st.session_state.second = max(0, st.session_state.second - 1)
            st.session_state.playing = False
    with b2:
        if st.button("▶️ Play 1x"):
            st.session_state.playing = True
            st.session_state.speed = 1
    with b3:
        if st.button("⏩ Forward"):
            st.session_state.second = min(359, st.session_state.second + 1)
            st.session_state.playing = False
    with b4:
        if st.button("⏸️ Pause"):
            st.session_state.playing = False
    with b5:
        if st.button("⏹️ Stop"):
            st.session_state.playing = False
            st.session_state.second = 0
    with b6:
        if st.button("⏩ Play 5x"):
            st.session_state.playing = True
            st.session_state.speed = 5

# Reproducción
if st.session_state.playing:
    time.sleep(0.01)
    st.session_state.second = min(359, st.session_state.second + st.session_state.speed)
    if st.session_state.second >= 359:
        st.session_state.playing = False
    st.experimental_rerun()

# Logo
with col_datos:
    st.markdown("""
    <div style='text-align: center; margin-top: 20px;'>
        <a href='https://www.fertilab.com' target='_blank'>
            <img src='https://redinfertiles.com/wp-content/uploads/2022/04/logo-Barcelona.png' 
                 alt='Fertilab Barcelona' width='250'/>
        </a>
    </div>
    """, unsafe_allow_html=True)

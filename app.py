import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

# Configuración de la página
st.set_page_config(page_title="Oocyte Tracker", layout="centered")
st.markdown("<h2 style='text-align: center;'>Vitrification Viability via Osmotic Response</h2>", unsafe_allow_html=True)

# Cargar datos
df = pd.read_csv("AioocyteV1.csv", sep=";")
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace('%', '', regex=False).str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Estado inicial
if "second" not in st.session_state:
    st.session_state.second = 0
if "playing" not in st.session_state:
    st.session_state.playing = False
if "speed" not in st.session_state:
    st.session_state.speed = 1

# Mostrar contenido dinámico
def mostrar_contenido():
    frame_path = f"frames/frame_{st.session_state.second}.jpg"
    if os.path.exists(frame_path):
        st.image(Image.open(frame_path), use_container_width=True)

    dato = df.iloc[st.session_state.second]
    st.markdown(f"""
        <div style='text-align: center; margin-top: 5px;'>
            <div style='font-size: 72px; font-weight: bold; color: #005EA8;'>
                {dato['Survival']:.1f}%
            </div>
            <div style='font-size: 18px; color: #444;'>Probability of oocyte survival after vitrification</div>
        </div>
        <hr style="margin: 5px 0;">
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Area %", f"{dato['Area%']:.3f}")
    c2.metric("Circularity", f"{dato['Circularity']:.3f}")
    c3.metric("Dehydration %/s", f"{dato['Vdeshidratacion']:.2f}")
    c4.metric("Deplasmolysis %/s", f"{dato['Vdeplasmolisi']:.2f}")

# Mostrar contenido actual
mostrar_contenido()

# Slider con key único
slider_val = st.slider("🕒", 0, 359, value=st.session_state.second, key="slider_unique", label_visibility="collapsed")
if slider_val != st.session_state.second:
    st.session_state.second = slider_val
    st.session_state.playing = False
    mostrar_contenido()

# Imagen de fondo
st.image("slider_background_final.png", use_container_width=True)

# Botones
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    if st.button("⏪ Back"):
        st.session_state.second = max(0, st.session_state.second - 1)
        st.session_state.playing = False
with c2:
    if st.button("▶️ Play 1x"):
        st.session_state.playing = True
        st.session_state.speed = 1
with c3:
    if st.button("⏩ Forward"):
        st.session_state.second = min(359, st.session_state.second + 1)
        st.session_state.playing = False
with c4:
    if st.button("⏸️ Pause"):
        st.session_state.playing = False
with c5:
    if st.button("⏹️ Stop"):
        st.session_state.second = 0
        st.session_state.playing = False
with c6:
    if st.button("▶️ Play 5x"):
        st.session_state.playing = True
        st.session_state.speed = 5

# Reproducción automática (fuera del bucle Streamlit)
if st.session_state.playing:
    time.sleep(0.2)
    st.session_state.second = min(359, st.session_state.second + st.session_state.speed)
    st.session_state.playing = True
    st.experimental_rerun()

# Logo
st.markdown("""
    <div style='text-align: center; margin-top: 20px;'>
        <a href='https://www.fertilab.com' target='_blank'>
            <img src='https://redinfertiles.com/wp-content/uploads/2022/04/logo-Barcelona.png' 
                 alt='Fertilab Barcelona' width='250'/>
        </a>
    </div>
""", unsafe_allow_html=True)

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

# Placeholders
image_ph = st.empty()
survival_ph = st.empty()
metrics_ph = st.empty()
slider_ph = st.empty()
graph_ph = st.empty()
controls_ph = st.empty()

def mostrar_contenido():
    # Mostrar imagen
    frame_path = f"frames/frame_{st.session_state.second}.jpg"
    if os.path.exists(frame_path):
        image = Image.open(frame_path)
        image_ph.image(image, caption=None, use_container_width=True)
    else:
        image_ph.warning("No se encontró imagen.")

    # Mostrar datos
    dato = df.iloc[st.session_state.second]
    survival_ph.markdown(f"""
        <div style='text-align: center; margin-top: 5px;'>
            <div style='font-size: 72px; font-weight: bold; color: #005EA8;'>
                {dato['Survival']:.1f}%
            </div>
            <div style='font-size: 18px; color: #444;'>Probability of oocyte survival after vitrification</div>
        </div>
        <hr style="margin: 5px 0;">
    """, unsafe_allow_html=True)

    with metrics_ph.container():
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Area %", f"{dato['Area%']:.3f}")
        col2.metric("Circularity", f"{dato['Circularity']:.3f}")
        col3.metric("Dehydration %/s", f"{dato['Vdeshidratacion']:.2f}")
        col4.metric("Deplasmolysis %/s", f"{dato['Vdeplasmolisi']:.2f}")

mostrar_contenido()

# Slider
with slider_ph.container():
    selected = st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed")
    if selected != st.session_state.second:
        st.session_state.second = selected
        st.session_state.playing = False
        mostrar_contenido()

# Gráfico
graph_ph.image("slider_background_final.png", use_container_width=True)

# Controles
with controls_ph.container():
    colA, colB, colC, colD, colE, colF = st.columns(6)
    with colA:
        if st.button("⏪ Back"):
            st.session_state.second = max(0, st.session_state.second - 1)
            st.session_state.playing = False
            mostrar_contenido()
    with colB:
        if st.button("▶️ Play 1x"):
            st.session_state.playing = True
            st.session_state.speed = 1
    with colC:
        if st.button("⏩ Forward"):
            st.session_state.second = min(359, st.session_state.second + 1)
            st.session_state.playing = False
            mostrar_contenido()
    with colD:
        if st.button("⏸️ Pause"):
            st.session_state.playing = False
    with colE:
        if st.button("⏹️ Stop"):
            st.session_state.playing = False
            st.session_state.second = 0
            mostrar_contenido()
    with colF:
        if st.button("▶️ Play 5x"):
            st.session_state.playing = True
            st.session_state.speed = 5

# Reproducción sin st.experimental_rerun()
while st.session_state.playing and st.session_state.second < 359:
    time.sleep(0.5)
    st.session_state.second = min(359, st.session_state.second + st.session_state.speed)
    mostrar_contenido()
    with slider_ph.container():
        st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed", key="slider_replay", disabled=True)

import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

st.set_page_config(page_title="Oocyte Tracker", layout="centered")
st.title("📸 Frame-by-Frame Oocyte Tracker")

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

# Contenedores
image_placeholder = st.empty()
slider_placeholder = st.empty()
data_placeholder = st.empty()

# Mostrar imagen + datos
def mostrar_contenido():
    with image_placeholder.container():
        frame_path = f"frames/frame_{st.session_state.second}.jpg"
        if os.path.exists(frame_path):
            image = Image.open(frame_path)
            st.image(image, caption=f"Segundo {st.session_state.second}", use_container_width=True)
        else:
            st.warning(f"No se encontró imagen para el segundo {st.session_state.second}")

    with data_placeholder.container():
        dato = df.iloc[st.session_state.second]
        st.markdown(f"""
            <div style='text-align: center; margin-top: 20px;'>
                <div style='font-size: 48px; font-weight: bold; color: #005EA8;'>
                    {dato['Survival']:.1f}%
                </div>
                <div style='font-size: 16px; color: #444;'>Probability of Survival</div>
            </div>
            <hr style="margin: 20px 0;">
        """, unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Area %", f"{dato['Area%']:.3f}")
        col2.metric("Circularity", f"{dato['Circularity']:.3f}")
        col3.metric("V. Deshidratación", f"{dato['Vdeshidratacion']:.2f}%")
        col4.metric("V. Deplasmolisis", f"{dato['Vdeplasmolisi']:.2f}%")

# Mostrar fondo gráfico
st.image("slider_background_final.png", use_container_width=True)

# Mostrar contenido actual
mostrar_contenido()

# Slider siempre visible
with slider_placeholder:
    selected = st.slider("🕒 Segundo del vídeo", 0, 359, value=st.session_state.second)
    if selected != st.session_state.second:
        st.session_state.second = selected
        st.session_state.playing = False
        mostrar_contenido()

# Controles
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    if st.button("⏪ Back"):
        st.session_state.second = max(0, st.session_state.second - 1)
        st.session_state.playing = False
        mostrar_contenido()
with col2:
    if st.button("▶️ Play 1x"):
        st.session_state.playing = True
        st.session_state.speed = 1
with col3:
    if st.button("⏩ Forward"):
        st.session_state.second = min(359, st.session_state.second + 1)
        st.session_state.playing = False
        mostrar_contenido()
with col4:
    if st.button("⏸️ Pause"):
        st.session_state.playing = False
with col5:
    if st.button("⏹️ Stop"):
        st.session_state.playing = False
        st.session_state.second = 0
        mostrar_contenido()
with col6:
    if st.button("⏩ Play 5x"):
        st.session_state.playing = True
        st.session_state.speed = 5

# Reproducción automática
if st.session_state.playing:
    for _ in range(100):
        if not st.session_state.playing or st.session_state.second >= 359:
            st.session_state.playing = False
            break
        time.sleep(0.5)
        st.session_state.second = min(359, st.session_state.second + st.session_state.speed)
        mostrar_contenido()

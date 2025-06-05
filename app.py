import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

# Configurar la página
st.set_page_config(page_title="Oocyte Tracker by Frame", layout="centered")
st.title("📸 Frame-by-Frame Oocyte Tracker")

# Cargar datos
df = pd.read_csv("AioocyteV1.csv", sep=";")
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace('%', '', regex=False)
        df[col] = df[col].str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Inicializar el estado si no existe
if "second" not in st.session_state:
    st.session_state.second = 0
if "playing" not in st.session_state:
    st.session_state.playing = False

# Mostrar imagen correspondiente al segundo actual
frame_path = f"frames/frame_{st.session_state.second}.jpg"
if os.path.exists(frame_path):
    image = Image.open(frame_path)
    st.image(image, caption=f"Segundo {st.session_state.second}", use_container_width=True)
else:
    st.warning(f"No se encontró la imagen para el segundo {st.session_state.second}")

# Slider debajo del video
st.session_state.second = st.slider("🕒 Selecciona segundo del vídeo", 0, min(len(df)-1, 359), st.session_state.second)

# Controles de reproducción
col_play, col_pause, col_back, col_forward = st.columns([1,1,1,1])
with col_play:
    if st.button("▶️ Play"):
        st.session_state.playing = True
with col_pause:
    if st.button("⏸️ Pause"):
        st.session_state.playing = False
with col_back:
    if st.button("⏪ Back"):
        st.session_state.second = max(0, st.session_state.second - 1)
with col_forward:
    if st.button("⏩ Forward"):
        st.session_state.second = min(len(df)-1, st.session_state.second + 1)

# Mostrar datos correspondientes
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

# Si está en modo reproducción, avanzar automáticamente
if st.session_state.playing:
    time.sleep(0.5)
    st.session_state.second = min(st.session_state.second + 1, len(df) - 1)
    st.experimental_rerun()

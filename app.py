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

# Mostrar imagen
frame_path = f"frames/frame_{st.session_state.second}.jpg"
if os.path.exists(frame_path):
    image = Image.open(frame_path)
    st.image(image, caption=None, use_container_width=True)
else:
    st.warning("No se encontró imagen.")

# Probabilidad de supervivencia (grande y centrada)
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

# Estadísticas centradas en una sola fila
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Area %", f"{dato['Area%']:.3f}")
with col2:
    st.metric("Circularity", f"{dato['Circularity']:.3f}")
with col3:
    st.metric("Dehydration %/s", f"{dato['Vdeshidratacion']:.2f}")
with col4:
    st.metric("Deplasmolysis %/s", f"{dato['Vdeplasmolisi']:.2f}")

# Slider
selected = st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed")
if selected != st.session_state.second:
    st.session_state.second = selected
    st.session_state.playing = False

# Imagen de la gráfica justo debajo del slider
st.image("slider_background_final.png", use_container_width=True)

# Botones en una única fila
colA, colB, colC, colD, colE, colF = st.columns(6)
with colA:
    if st.button("⏪ Back"):
        st.session_state.second = max(0, st.session_state.second - 1)
        st.session_state.playing = False
with colB:
    if st.button("▶️ Play 1x"):
        st.session_state.playing = True
        st.session_state.speed = 1
with colC:
    if st.button("⏩ Forward"):
        st.session_state.second = min(359, st.session_state.second + 1)
        st.session_state.playing = False
with colD:
    if st.button("⏸️ Pause"):
        st.session_state.playing = False
with colE:
    if st.button("⏹️ Stop"):
        st.session_state.playing = False
        st.session_state.second = 0
with colF:
    if st.button("▶️ Play 5x"):
        st.session_state.playing = True
        st.session_state.speed = 5

# Reproducción automática sin usar experimental_rerun
if st.session_state.playing:
    if "last_run" not in st.session_state:
        st.session_state.last_run = time.time()
    if time.time() - st.session_state.last_run > 0.5:
        st.session_state.second = min(359, st.session_state.second + st.session_state.speed)
        st.session_state.last_run = time.time()
        st.experimental_rerun()

# Logo final más grande y centrado
st.markdown("""
    <div style='text-align: center; margin-top: 20px;'>
        <a href='https://www.fertilab.com' target='_blank'>
            <img src='https://redinfertiles.com/wp-content/uploads/2022/04/logo-Barcelona.png' 
                 alt='Fertilab Barcelona' width='250'/>
        </a>
    </div>
""", unsafe_allow_html=True)

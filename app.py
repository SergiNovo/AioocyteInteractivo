import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

# Configurar página
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
    st.image(image, use_container_width=True)

# Supervivencia centrada y grande
dato = df.iloc[st.session_state.second]
st.markdown(f"""
    <div style='text-align: center;'>
        <div style='font-size: 64px; font-weight: bold; color: #005EA8;'>
            {dato['Survival']:.1f}%
        </div>
        <div style='font-size: 16px;'>Probability of oocyte survival after vitrification</div>
    </div>
""", unsafe_allow_html=True)

# Métricas centradas
cols = st.columns(4)
cols[0].metric("Area %", f"{dato['Area%']:.3f}")
cols[1].metric("Circularity", f"{dato['Circularity']:.3f}")
cols[2].metric("Dehydration %/s", f"{dato['Vdeshidratacion']:.2f}")
cols[3].metric("Deplasmolysis %/s", f"{dato['Vdeplasmolisi']:.2f}")

# Slider sin clave
selected = st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed")
if selected != st.session_state.second:
    st.session_state.second = selected
    st.session_state.playing = False

# Imagen gráfica
st.image("slider_background_final.png", use_container_width=True)

# Botones
buttons = st.columns(6)
if buttons[0].button("⏪ Back"):
    st.session_state.second = max(0, st.session_state.second - 1)
    st.session_state.playing = False
if buttons[1].button("▶️ Play 1x"):
    st.session_state.playing = True
    st.session_state.speed = 1
if buttons[2].button("⏩ Forward"):
    st.session_state.second = min(359, st.session_state.second + 1)
    st.session_state.playing = False
if buttons[3].button("⏸️ Pause"):
    st.session_state.playing = False
if buttons[4].button("⏹️ Stop"):
    st.session_state.second = 0
    st.session_state.playing = False
if buttons[5].button("▶️ Play 5x"):
    st.session_state.playing = True
    st.session_state.speed = 5

# Reproducción automática controlada
if st.session_state.playing:
    time.sleep(0.3)
    if st.session_state.second < 359:
        st.session_state.second += st.session_state.speed
        st.experimental_rerun()
    else:
        st.session_state.playing = False

# Logo centrado
st.markdown("""
    <div style='text-align: center; margin-top: 20px;'>
        <a href='https://www.fertilab.com' target='_blank'>
            <img src='https://redinfertiles.com/wp-content/uploads/2022/04/logo-Barcelona.png' 
                 alt='Fertilab Barcelona' width='250'/>
        </a>
    </div>
""", unsafe_allow_html=True)

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
else:
    st.warning("No se encontró imagen.")

# Probabilidad de supervivencia
dato = df.iloc[st.session_state.second]
st.markdown(f"""
    <div style='text-align: center; margin-top: 5px;'>
        <div style='font-size: 72px; font-weight: bold; color: #005EA8;'>
            {dato['Survival']:.1f}%
        </div>
        <div style='font-size: 16px; color: #444;'>Probability of oocyte survival after vitrification</div>
    </div>
""", unsafe_allow_html=True)

# Métricas centradas
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Area %", f"{dato['Area%']:.3f}")
with col2:
    st.metric("Circularity", f"{dato['Circularity']:.3f}")
with col3:
    st.metric("Dehydration %/s", f"{dato['Vdeshidratacion']:.2f}")
with col4:
    st.metric("Deplasmolysis %/s", f"{dato['Vdeplasmolisi']:.2f}")
st.markdown("</div>", unsafe_allow_html=True)

# Slider con fondo
st.image("slider_background_final.png", use_container_width=True)
slider_value = st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed")
if slider_value != st.session_state.second:
    st.session_state.second = slider_value
    st.session_state.playing = False

# Botones
btn1, btn2, btn3, btn4, btn5, btn6 = st.columns(6)
with btn1:
    if st.button("⏪"):
        st.session_state.second = max(0, st.session_state.second - 1)
        st.session_state.playing = False
with btn2:
    if st.button("▶️ 1x"):
        st.session_state.playing = True
        st.session_state.speed = 1
with btn3:
    if st.button("⏩"):
        st.session_state.second = min(359, st.session_state.second + 1)
        st.session_state.playing = False
with btn4:
    if st.button("⏸️"):
        st.session_state.playing = False
with btn5:
    if st.button("⏹️"):
        st.session_state.playing = False
        st.session_state.second = 0
with btn6:
    if st.button("▶️ 5x"):
        st.session_state.playing = True
        st.session_state.speed = 5

# Reproducción automática (sin rerun)
if st.session_state.playing:
    time.sleep(0.5)
    st.session_state.second = min(359, st.session_state.second + st.session_state.speed)
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

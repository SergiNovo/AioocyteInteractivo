import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

# Configurar la página para móviles
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

# Mostrar imagen
def mostrar_contenido():
    frame_path = f"frames/frame_{st.session_state.second}.jpg"
    if os.path.exists(frame_path):
        image = Image.open(frame_path)
        st.image(image, use_container_width=True)
    else:
        st.warning("No se encontró imagen.")

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
    with c1: st.metric("Area %", f"{dato['Area%']:.3f}")
    with c2: st.metric("Circularity", f"{dato['Circularity']:.3f}")
    with c3: st.metric("Dehydration %/s", f"{dato['Vdeshidratacion']:.2f}")
    with c4: st.metric("Deplasmolysis %/s", f"{dato['Vdeplasmolisi']:.2f}")

# Mostrar todo
mostrar_contenido()

# Slider
selected = st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed", key="slider_unique")
if selected != st.session_state.second:
    st.session_state.second = selected
    st.session_state.playing = False
    mostrar_contenido()

# Gráfico
st.image("slider_background_final.png", use_container_width=True)

# Botones en una sola fila
b1, b2, b3, b4, b5, b6 = st.columns(6)
with b1:
    if st.button("⏪"):
        st.session_state.second = max(0, st.session_state.second - 1)
        st.session_state.playing = False
with b2:
    if st.button("▶️ 1x"):
        st.session_state.playing = True
        st.session_state.speed = 1
with b3:
    if st.button("⏩"):
        st.session_state.second = min(359, st.session_state.second + 1)
        st.session_state.playing = False
with b4:
    if st.button("⏸️"):
        st.session_state.playing = False
with b5:
    if st.button("⏹️"):
        st.session_state.playing = False
        st.session_state.second = 0
with b6:
    if st.button("▶️ 5x"):
        st.session_state.playing = True
        st.session_state.speed = 5

# Reproducción automática sin usar experimental_rerun
if st.session_state.playing:
    for _ in range(500):
        if not st.session_state.playing or st.session_state.second >= 359:
            st.session_state.playing = False
            break
        time.sleep(0.3)
        st.session_state.second = min(359, st.session_state.second + st.session_state.speed)
        mostrar_contenido()
        st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed", key="slider_unique", disabled=True)

# Logo
st.markdown("""
    <div style='text-align: center; margin-top: 20px;'>
        <a href='https://www.fertilab.com' target='_blank'>
            <img src='https://redinfertiles.com/wp-content/uploads/2022/04/logo-Barcelona.png' width='250'/>
        </a>
    </div>
""", unsafe_allow_html=True)

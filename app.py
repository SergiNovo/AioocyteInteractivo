import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

# Configurar página
st.set_page_config(page_title="Oocyte Tracker", layout="wide")
st.markdown("<h1 style='text-align: center; font-size: 32px;'>Vitrification Viability via Osmotic Response</h1>", unsafe_allow_html=True)

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
col1, col2 = st.columns([1, 1])
video_placeholder = col1.empty()
content_container = col2.container()

# Mostrar contenido
def mostrar_contenido():
    frame_path = f"frames/frame_{st.session_state.second}.jpg"
    with video_placeholder:
        if os.path.exists(frame_path):
            img = Image.open(frame_path)
            st.image(img, caption=f"Second {st.session_state.second}", use_container_width=True)

    dato = df.iloc[st.session_state.second]

    with content_container:
        st.markdown(f"""
        <div style='text-align: center; margin-top: -10px;'>
            <div style='font-size: 60px; font-weight: bold; color: #005EA8;'>
                {dato['Survival']:.1f}%
            </div>
            <div style='font-size: 18px; color: #444;'>Probability of oocyte survival after vitrification</div>
        </div>
        <hr style="margin: 10px 0;">
        """, unsafe_allow_html=True)

        with st.container():
            a, b, c, d = st.columns(4)
            a.metric("Area %", f"{dato['Area%']:.3f}")
            b.metric("Circularity", f"{dato['Circularity']:.3f}")
            c.metric("Dehydration %/s", f"{dato['Vdeshidratacion']:.2f}%")
            d.metric("Deplasmolysis %/s", f"{dato['Vdeplasmolisi']:.2f}%")

        st.image("slider_background_final.png", use_container_width=True)

# Slider
def render_slider():
    selected = st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed", key="slider_key")
    if selected != st.session_state.second:
        st.session_state.second = selected
        st.session_state.playing = False
        mostrar_contenido()

# Mostrar contenido inicial
mostrar_contenido()
render_slider()

# Controles
with st.container():
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        if st.button("⏪ Back"):
            st.session_state.second = max(0, st.session_state.second - 1)
            st.session_state.playing = False
            mostrar_contenido()
            render_slider()
    with c2:
        if st.button("▶️ Play 1x"):
            st.session_state.playing = True
            st.session_state.speed = 1
    with c3:
        if st.button("⏩ Forward"):
            st.session_state.second = min(359, st.session_state.second + 1)
            st.session_state.playing = False
            mostrar_contenido()
            render_slider()
    with c4:
        if st.button("⏸️ Pause"):
            st.session_state.playing = False
    with c5:
        if st.button("⏹️ Stop"):
            st.session_state.playing = False
            st.session_state.second = 0
            mostrar_contenido()
            render_slider()
    with c6:
        if st.button("⏩ Play 5x"):
            st.session_state.playing = True
            st.session_state.speed = 5

# Reproducción automática controlada
if st.session_state.playing:
    while st.session_state.playing and st.session_state.second < 359:
        time.sleep(0.5)
        st.session_state.second = min(359, st.session_state.second + st.session_state.speed)
        mostrar_contenido()
        render_slider()

# Logo centrado más grande
st.markdown("""
<div style='text-align: center; margin-top: 20px;'>
    <a href='https://www.fertilab.com' target='_blank'>
        <img src='https://redinfertiles.com/wp-content/uploads/2022/04/logo-Barcelona.png' 
             alt='Fertilab Barcelona' width='250'/>
    </a>
</div>
""", unsafe_allow_html=True)

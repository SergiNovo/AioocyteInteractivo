import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

# Configuración general
st.set_page_config(page_title="Oocyte Tracker", layout="centered")
st.markdown("<h3 style='text-align: center;'>Vitrification Viability via Osmotic Response</h3>", unsafe_allow_html=True)

# Cargar datos
df = pd.read_csv("AioocyteV1.csv", sep=";")
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace('%', '', regex=False)
        df[col] = df[col].str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Estados iniciales
if "second" not in st.session_state:
    st.session_state.second = 0
if "playing" not in st.session_state:
    st.session_state.playing = False
if "speed" not in st.session_state:
    st.session_state.speed = 1

# Contenedores
image_placeholder = st.empty()
survival_placeholder = st.empty()
metrics_placeholder = st.empty()
chart_placeholder = st.empty()
slider_placeholder = st.empty()
buttons_placeholder = st.empty()

# Mostrar contenido
def mostrar_contenido():
    frame_path = f"frames/frame_{st.session_state.second}.jpg"
    with image_placeholder:
        if os.path.exists(frame_path):
            image = Image.open(frame_path)
            st.image(image, use_container_width=True)
        else:
            st.warning("Frame not found.")

    dato = df.iloc[st.session_state.second]
    with survival_placeholder:
        st.markdown(f"""
            <div style='text-align: center; margin-top: 4px;'>
                <div style='font-size: 40px; font-weight: bold; color: #005EA8;'>{dato['Survival']:.1f}%</div>
                <div style='font-size: 14px; color: #444;'>Probability of oocyte survival after vitrification</div>
            </div>
        """, unsafe_allow_html=True)

    with metrics_placeholder:
        st.write("")
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Area %", f"{dato['Area%']:.2f}")
            st.metric("Dehydration rate", f"{dato['Vdeshidratacion']:.2f}%/s")
        with m2:
            st.metric("Circularity", f"{dato['Circularity']:.2f}")
            st.metric("Deplasmolysis rate", f"{dato['Vdeplasmolisi']:.2f}%/s")

    with chart_placeholder:
        st.image("slider_background_final.png", use_container_width=True)

# Slider
def render_slider():
    with slider_placeholder:
        selected = st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed")
        if selected != st.session_state.second:
            st.session_state.second = selected
            st.session_state.playing = False
            mostrar_contenido()

# Mostrar contenido inicial
mostrar_contenido()
render_slider()

# Controles
with buttons_placeholder:
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⏪ Back"):
            st.session_state.second = max(0, st.session_state.second - 1)
            st.session_state.playing = False
            mostrar_contenido()
            render_slider()
    with c2:
        if st.button("▶️ Play"):
            st.session_state.playing = True
            st.session_state.speed = 1
    with c3:
        if st.button("⏩ Forward"):
            st.session_state.second = min(359, st.session_state.second + 1)
            st.session_state.playing = False
            mostrar_contenido()
            render_slider()

# Reproducción automática
if st.session_state.playing:
    for _ in range(500):
        if not st.session_state.playing or st.session_state.second >= 359:
            st.session_state.playing = False
            break
        time.sleep(0.4)
        st.session_state.second = min(359, st.session_state.second + st.session_state.speed)
        mostrar_contenido()
        render_slider()

# Logo final
st.markdown("""
<div style='text-align: center; margin-top: 20px;'>
    <a href='https://www.fertilab.com' target='_blank'>
        <img src='https://redinfertiles.com/wp-content/uploads/2022/04/logo-Barcelona.png' width='120'/>
    </a>
</div>
""", unsafe_allow_html=True)

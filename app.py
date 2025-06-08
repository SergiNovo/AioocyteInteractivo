import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

# Configurar página para móvil
st.set_page_config(page_title="Vitrification Viability", layout="centered")
st.markdown("<h3 style='text-align: center;'>Vitrification Viability via Osmotic Response</h3>", unsafe_allow_html=True)

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

# Mostrar contenido
def mostrar_contenido():
    frame_path = f"frames/frame_{st.session_state.second}.jpg"
    if os.path.exists(frame_path):
        image = Image.open(frame_path)
        st.image(image, caption=f"Second {st.session_state.second}", use_container_width=True)
    else:
        st.warning("Image not found.")

    dato = df.iloc[st.session_state.second]

    # Supervivencia
    st.markdown(f"""
        <div style='text-align: center; margin-top: 1px;'>
            <div style='font-size: 36px; font-weight: bold; color: #005EA8;'>
                {dato['Survival']:.1f}%
            </div>
            <div style='font-size: 14px; color: #444;'>Oocyte survival probability</div>
        </div>
        <hr style="margin: 5px 0;">
    """, unsafe_allow_html=True)

    # Métricas
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Area %", f"{dato['Area%']:.3f}")
        st.metric("Dehydration %/s", f"{dato['Vdeshidratacion']:.2f}")
    with col2:
        st.metric("Circularity", f"{dato['Circularity']:.3f}")
        st.metric("Deplasmolysis %/s", f"{dato['Vdeplasmolisi']:.2f}")

    # Imagen slider
    st.image("slider_background_final.png", use_container_width=True)

# Slider
def render_slider():
    selected = st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed")
    if selected != st.session_state.second:
        st.session_state.second = selected
        st.session_state.playing = False
        mostrar_contenido()

# Mostrar contenido inicial
mostrar_contenido()
render_slider()

# Controles en dos filas de tres botones
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("⏪"):
        st.session_state.second = max(0, st.session_state.second - 1)
        st.session_state.playing = False
        mostrar_contenido()
        render_slider()
with c2:
    if st.button("▶️ 1x"):
        st.session_state.playing = True
        st.session_state.speed = 1
with c3:
    if st.button("⏩"):
        st.session_state.second = min(359, st.session_state.second + 1)
        st.session_state.playing = False
        mostrar_contenido()
        render_slider()

c4, c5, c6 = st.columns(3)
with c4:
    if st.button("⏸️"):
        st.session_state.playing = False
with c5:
    if st.button("⏹️"):
        st.session_state.playing = False
        st.session_state.second = 0
        mostrar_contenido()
        render_slider()
with c6:
    if st.button("▶️ 5x"):
        st.session_state.playing = True
        st.session_state.speed = 5

# Reproducción automática
if st.session_state.playing:
    for _ in range(500):
        if not st.session_state.playing or st.session_state.second >= 359:
            st.session_state.playing = False
            break
        time.sleep(0.5)
        st.session_state.second = min(359, st.session_state.second + st.session_state.speed)
        mostrar_contenido()
        render_slider()

# Logo final
st.markdown("""
<div style='text-align: center; margin-top: 15px;'>
    <a href='https://www.fertilab.com' target='_blank'>
        <img src='https://redinfertiles.com/wp-content/uploads/2022/04/logo-Barcelona.png' 
             alt='Fertilab Barcelona' width='150'/>
    </a>
</div>
""", unsafe_allow_html=True)

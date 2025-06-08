import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

# Configurar página
st.set_page_config(page_title="Vitrification Viability via Osmotic Response", layout="centered")
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

# Contenedores en una sola columna
video_placeholder = st.container()
supervivencia_placeholder = st.container()
metrics_placeholder = st.container()
grafico_placeholder = st.container()
slider_placeholder = st.container()
controles_placeholder = st.container()

# Mostrar contenido
def mostrar_contenido():
    frame_path = f"frames/frame_{st.session_state.second}.jpg"
    with video_placeholder:
        if os.path.exists(frame_path):
            image = Image.open(frame_path)
            st.image(image, caption=f"Second {st.session_state.second}", width=300)
        else:
            st.warning("No se encontró imagen.")

    dato = df.iloc[st.session_state.second]
    with supervivencia_placeholder:
        st.markdown(f"""
            <div style='text-align: center; margin-top: 5px;'>
                <div style='font-size: 30px; font-weight: bold; color: #005EA8;'>
                    {dato['Survival']:.1f}%
                </div>
                <div style='font-size: 16px; color: #444;'>Probability of oocyte survival after vitrification</div>
            </div>
            <hr style="margin: 4px 0;">
        """, unsafe_allow_html=True)

    with metrics_placeholder:
        st.markdown(f"""
            <div style='display: flex; justify-content: space-around; font-size: 14px;'>
                <div><b>Area %</b><br>{dato['Area%']:.3f}</div>
                <div><b>Circularity</b><br>{dato['Circularity']:.3f}</div>
                <div><b>Dehyd. rate</b><br>{dato['Vdeshidratacion']:.2f}%</div>
                <div><b>Depl. rate</b><br>{dato['Vdeplasmolisi']:.2f}%</div>
            </div>
        """, unsafe_allow_html=True)

    with grafico_placeholder:
        st.image("slider_background_final.png", use_container_width=True)

# Slider
def render_slider():
    with slider_placeholder:
        selected = st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed")
        if selected != st.session_state.second:
            st.session_state.second = selected
            st.session_state.playing = False
            mostrar_contenido()

# Contenido inicial
mostrar_contenido()
render_slider()

# Controles
with controles_placeholder:
    st.markdown("<hr style='margin: 5px 0;'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⏪ Back"):
            st.session_state.second = max(0, st.session_state.second - 1)
            st.session_state.playing = False
            mostrar_contenido()
            render_slider()
    with col2:
        if st.button("▶️ Play"):
            st.session_state.playing = True
            st.session_state.speed = 1
    with col3:
        if st.button("⏩ Forward"):
            st.session_state.second = min(359, st.session_state.second + 1)
            st.session_state.playing = False
            mostrar_contenido()
            render_slider()
    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("⏸️ Pause"):
            st.session_state.playing = False
    with col5:
        if st.button("⏹️ Stop"):
            st.session_state.playing = False
            st.session_state.second = 0
            mostrar_contenido()
            render_slider()
    with col6:
        if st.button("⏩ Play 5x"):
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

# Logo al final
st.markdown("""
<div style='text-align: center; margin-top: 10px;'>
    <a href='https://www.fertilab.com' target='_blank'>
        <img src='https://redinfertiles.com/wp-content/uploads/2022/04/logo-Barcelona.png' 
             alt='Fertilab Barcelona' width='120'/>
    </a>
</div>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

# Configuración de la página
st.set_page_config(page_title="Vitrification Viability via Osmotic Response", layout="wide")

# Título principal
st.markdown("<h1 style='text-align: center;'>Vitrification Viability via Osmotic Response</h1>", unsafe_allow_html=True)

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

# Layout en columnas
col_video, col_datos = st.columns([1.5, 2])

video_placeholder = col_video.empty()
supervivencia_placeholder = col_datos.empty()
metricas_placeholder = col_datos.container()
grafico_placeholder = col_datos.empty()
slider_placeholder = col_datos.empty()
controles_placeholder = col_datos.empty()

# Mostrar contenido dinámico
def mostrar_contenido():
    frame_path = f"frames/frame_{st.session_state.second}.jpg"
    with video_placeholder:
        if os.path.exists(frame_path):
            image = Image.open(frame_path)
            st.image(image, caption=f"Second {st.session_state.second}", use_container_width=True)
        else:
            st.warning("No se encontró la imagen.")

    dato = df.iloc[st.session_state.second]
    with supervivencia_placeholder:
        st.markdown(f"""
            <div style='text-align: center; margin-top: 1px;'>
                <div style='font-size: 60px; font-weight: bold; color: #005EA8;'>
                    {dato['Survival']:.1f}%
                </div>
                <div style='font-size: 20px; color: #444;'>Probability of oocyte survival after vitrification</div>
            </div>
            <hr style="margin: 2px 0;">
        """, unsafe_allow_html=True)

    with metricas_placeholder:
        st.markdown("""
        <div style='display: flex; justify-content: space-around; text-align: center; font-size: 16px;'>
            <div><strong>Area %</strong><br>{:.3f}</div>
            <div><strong>Circularity</strong><br>{:.3f}</div>
            <div><strong>Dehydration rate %/s</strong><br>{:.2f}%</div>
            <div><strong>Deplasmolysis rate %/s</strong><br>{:.2f}%</div>
        </div>
        """.format(dato['Area%'], dato['Circularity'], dato['Vdeshidratacion'], dato['Vdeplasmolisi']), unsafe_allow_html=True)

    with grafico_placeholder:
        st.image("slider_background_final.png", use_container_width=True)

# Slider
def render_slider():
    with slider_placeholder:
        selected = st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed", key="slider_control")
        if selected != st.session_state.second:
            st.session_state.second = selected
            st.session_state.playing = False
            mostrar_contenido()

# Mostrar contenido inicial
mostrar_contenido()
render_slider()

# Controles
with controles_placeholder:
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
             alt='Fertilab Barcelona' width='250'/>
    </a>
</div>
""", unsafe_allow_html=True)

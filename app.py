import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

# Configurar página
st.set_page_config(page_title="Vitrification Viability via Osmotic Response", layout="wide")
st.markdown("<h4 style='text-align: center;'>Vitrification Viability via Osmotic Response</h4>", unsafe_allow_html=True)

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

# Estructura visual
col_video, col_datos = st.columns([2, 3])
video_placeholder = col_video.empty()
supervivencia_placeholder = col_datos.empty()
metrics_placeholder = col_datos.empty()
grafico_placeholder = col_datos.empty()
slider_placeholder = col_datos.empty()
controles_placeholder = col_datos.empty()

# Mostrar contenido
def mostrar_contenido():
    frame_path = f"frames/frame_{st.session_state.second}.jpg"
    with video_placeholder:
        if os.path.exists(frame_path):
            image = Image.open(frame_path)
            st.image(image, caption=f"second {st.session_state.second}", use_container_width=True)
        else:
            st.warning("No se encontró imagen.")

    dato = df.iloc[st.session_state.second]
    with supervivencia_placeholder:
        st.markdown(f"""
            <div style='text-align: center; margin-top: 2px;'>
                <div style='font-size: 30px; font-weight: bold; color: #005EA8;'>
                    {dato['Survival']:.1f}%
                </div>
                <div style='font-size: 14px; color: #444;'>Probability of oocyte survival after vitrification</div>
            </div>
            <hr style="margin: 2px 0;">
        """, unsafe_allow_html=True)

    with metrics_placeholder:
        col1, col2 = col_datos.columns(2)
        with col1:
            st.metric("Area %", f"{dato['Area%']:.3f}")
            st.metric("Dehydration rate %/s", f"{dato['Vdeshidratacion']:.2f}%")
        with col2:
            st.metric("Circularity", f"{dato['Circularity']:.3f}")
            st.metric("Deplasmolysis rate %/s", f"{dato['Vdeplasmolisi']:.2f}%")

    with grafico_placeholder:
        st.image("slider_background_final.png", use_container_width=True)

# Renderizar slider sin key duplicado
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
with controles_placeholder:
    c1, c2,

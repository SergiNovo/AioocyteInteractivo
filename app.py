import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

st.set_page_config(page_title="Oocyte Tracker", layout="wide")

# Título centrado
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

# Layout apaisado: video izquierda, resto derecha
col_video, col_datos = st.columns([2, 3])

# Función para mostrar contenido
def mostrar_contenido():
    with col_video:
        frame_path = f"frames/frame_{st.session_state.second}.jpg"
        if os.path.exists(frame_path):
            image = Image.open(frame_path)
            st.image(image, caption=f"Segundo {st.session_state.second}", use_container_width=True)
        else:
            st.warning("No se encontró imagen.")

    with col_datos:
        dato = df.iloc[st.session_state.second]

        # Probabilidad de supervivencia muy grande
        st.markdown(f"""
            <div style='text-align: center; margin-top: 5px; margin-bottom: 30px; height: 45vh; display: flex; flex-direction: column; justify-content: center;'>
                <div style='font-size: 12vh; font-weight: bold; color: #005EA8; line-height: 1;'>
                    {dato['Survival']:.1f}%
                </div>
                <div style='font-size: 2.5vh; color: #444; margin-top: 0.5vh;'>Probability of oocyte survival after vitrification</div>
            </div>
        """, unsafe_allow_html=True)

        # Métricas distribuidas uniformemente
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Area %", f"{dato['Area%']:.3f}")
        m2.metric("Circularity", f"{dato['Circularity']:.3f}")
        m3.metric("Dehydration rate %/s", f"{dato['Vdeshidratacion']:.2f}%")
        m4.metric("Deplasmolysis rate %/s", f"{dato['Vdeplasmolisi']:.2f}%")

        # Slider con fondo de gráfica
        st.image("slider_background_final.png", use_container_width=True)
        render_slider()

        # Controles justo debajo del slider
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1:
            if st.button("⏪ Back"):
                st.session_state.second = max(0, st.session_state.second - 1)
                st.session_state.playing = False
        with c2:
            if st.button("▶️ Play 1x"):
                st.session_state.playing = True
                st.session_state.speed = 1
        with c3:
            if st.button("⏩ Forward"):
                st.session_state.second = min(359, st.session_state.second + 1)
                st.session_state.playing = False
        with c4:
            if st.button("⏸️ Pause"):
                st.session_state.playing = False
        with c5:
            if st.button("⏹️ Stop"):
                st.session_state.playing = False
                st.session_state.second = 0
        with c6:
            if st.button("⏩ Play 5x"):
                st.session_state.playing = True
                st.session_state.speed = 5

# Slider que actualiza segundo
def render_slider():
    st.slider("🕒", 0, 359, value=st.session_state.second,
              key="slider_key", label_visibility="collapsed",
              on_change=slider_changed)

# Callback del slider
def slider_changed():
    st.session_state.playing = False

# Mostrar contenido inicial
mostrar_contenido()

# Reproducción automática
if st.session_state.playing:
    for _ in range(100):
        if not st.session_state.playing or st.session_state.second >= 359:
            st.session_state.playing = False
            break
        time.sleep(0.5)
        st.session_state.second = min(359, st.session_state.second + st.session_state.speed)
        mostrar_contenido()

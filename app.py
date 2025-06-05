
import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

st.set_page_config(page_title="Oocyte Tracker", layout="centered")
st.title("📸 Frame-by-Frame Oocyte Tracker")

# Leer datos
df = pd.read_csv("AioocyteV1.csv", sep=";")
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace('%', '', regex=False)
        df[col] = df[col].str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Inicializar estado
if "second" not in st.session_state:
    st.session_state.second = 0
if "playing" not in st.session_state:
    st.session_state.playing = False
if "speed" not in st.session_state:
    st.session_state.speed = 1.0  # velocidad normal

# Contenedor principal
main_placeholder = st.empty()

def render_frame():
    with main_placeholder.container():
        frame_path = f"frames/frame_{st.session_state.second}.jpg"
        if os.path.exists(frame_path):
            image = Image.open(frame_path)
            st.image(image, caption=f"Segundo {st.session_state.second}", use_container_width=True)
        else:
            st.warning(f"No se encontró imagen para el segundo {st.session_state.second}")

        selected = st.slider("🕒 Segundo del vídeo", 0, min(len(df)-1, 359), value=st.session_state.second)
        if selected != st.session_state.second:
            st.session_state.second = selected
            st.session_state.playing = False

        dato = df.iloc[st.session_state.second]
        st.markdown(f"""
            <div style='text-align: center; margin-top: 20px;'>
                <div style='font-size: 48px; font-weight: bold; color: #005EA8;'>
                    {dato['Survival']:.1f}%
                </div>
                <div style='font-size: 16px; color: #444;'>Probability of Survival</div>
            </div>
            <hr style="margin: 20px 0;">
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Area %", f"{dato['Area%']:.3f}")
        col2.metric("Circularity", f"{dato['Circularity']:.3f}")
        col3.metric("V. Deshidratación", f"{dato['Vdeshidratacion']:.2f}%")
        col4.metric("V. Deplasmolisis", f"{dato['Vdeplasmolisi']:.2f}%")

        col_play, col_pause, col_back, col_forward = st.columns(4)
        with col_play:
            if st.button("▶️ Play"):
                st.session_state.playing = True
                st.session_state.speed = 0.5
        with col_pause:
            if st.button("⏸️ Pause"):
                st.session_state.playing = False
        with col_back:
            if st.button("⏪ Back"):
                st.session_state.second = max(0, st.session_state.second - 1)
        with col_forward:
            if st.button("⏩ Forward"):
                st.session_state.second = min(len(df)-1, st.session_state.second + 1)

        col_stop, col_fast = st.columns(2)
        with col_stop:
            if st.button("⏹️ Stop"):
                st.session_state.second = 0
                st.session_state.playing = False
                st.session_state.speed = 0.5
        with col_fast:
            if st.button("⏩ 5x Speed"):
                st.session_state.playing = True
                st.session_state.speed = 0.1

render_frame()

# Bucle de reproducción sincronizado
if st.session_state.playing:
    for _ in range(500):
        if not st.session_state.playing or st.session_state.second >= len(df) - 1:
            break
        time.sleep(st.session_state.speed)
        st.session_state.second += 1
        render_frame()


import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

# Configuración general
st.set_page_config(page_title="Oocyte Tracker", layout="wide")

# Estilos generales
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

# Estructura principal horizontal
col_video, col_info = st.columns([3, 4])

with col_video:
    frame_path = f"frames/frame_{st.session_state.second}.jpg"
    if os.path.exists(frame_path):
        image = Image.open(frame_path)
        st.image(image, caption=f"Second {st.session_state.second}", use_container_width=True)
    else:
        st.warning("No se encontró imagen.")

with col_info:
    dato = df.iloc[st.session_state.second]

    st.markdown(f"""
        <div style='text-align: center; margin-top: 5px;'>
            <div style='font-size: 48px; font-weight: bold; color: #005EA8;'>
                {dato['Survival']:.1f}%
            </div>
            <div style='font-size: 14px; color: #444;'>Probability of oocyte survival after vitrification</div>
        </div>
    """, unsafe_allow_html=True)

    # Métricas en 2 columnas para espacio compacto
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Area %", f"{dato['Area%']:.3f}")
        st.metric("Dehydration %/s", f"{dato['Vdeshidratacion']:.2f}%")
    with m2:
        st.metric("Circularity", f"{dato['Circularity']:.3f}")
        st.metric("Deplasmolysis %/s", f"{dato['Vdeplasmolisi']:.2f}%")

    # Slider y gráfico
    st.image("slider_background_final.png", use_container_width=True)
    selected = st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed")
    if selected != st.session_state.second:
        st.session_state.second = selected
        st.session_state.playing = False
        st.experimental_rerun()

    # Controles
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⏪ Back"):
            st.session_state.second = max(0, st.session_state.second - 1)
            st.session_state.playing = False
            st.experimental_rerun()
    with c2:
        if st.button("▶️ Play 1x"):
            st.session_state.playing = True
            st.session_state.speed = 1
    with c3:
        if st.button("⏩ Forward"):
            st.session_state.second = min(359, st.session_state.second + 1)
            st.session_state.playing = False
            st.experimental_rerun()

    c4, c5, c6 = st.columns(3)
    with c4:
        if st.button("⏸️ Pause"):
            st.session_state.playing = False
    with c5:
        if st.button("⏹️ Stop"):
            st.session_state.playing = False
            st.session_state.second = 0
            st.experimental_rerun()
    with c6:
        if st.button("⏩ Play 5x"):
            st.session_state.playing = True
            st.session_state.speed = 5

    # Logo al final
    st.markdown("""
    <div style='text-align: center; margin-top: 5px;'>
        <a href='https://www.fertilab.com' target='_blank'>
            <img src='https://redinfertiles.com/wp-content/uploads/2022/04/logo-Barcelona.png' 
                 alt='Fertilab Barcelona' width='150'/>
        </a>
    </div>
    """, unsafe_allow_html=True)

# Reproducción automática
if st.session_state.playing:
    for _ in range(500):
        if not st.session_state.playing or st.session_state.second >= 359:
            st.session_state.playing = False
            break
        time.sleep(0.5)
        st.session_state.second = min(359, st.session_state.second + st.session_state.speed)
        st.experimental_rerun()

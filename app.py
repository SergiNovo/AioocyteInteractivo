import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

# Configurar la app
st.set_page_config(page_title="Oocyte Tracker", layout="wide")

# Estilo compacto para móvil
st.markdown("""
<style>
h1, h2, h3, h4, h5, h6, .css-10trblm, .css-1v0mbdj, .stMetric label {
    font-size: 14px !important;
}
.stMetric > div > div {
    font-size: 16px !important;
}
button[kind="secondary"] {
    padding: 2px 4px !important;
    font-size: 12px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h5 style='text-align: center;'>Vitrification Viability via Osmotic Response</h5>", unsafe_allow_html=True)

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

# Distribución horizontal
col_video, col_info = st.columns([1, 1])

with col_video:
    frame_path = f"frames/frame_{st.session_state.second}.jpg"
    if os.path.exists(frame_path):
        image = Image.open(frame_path)
        st.image(image, caption=None, use_container_width=True)
    else:
        st.warning("No se encontró imagen.")

with col_info:
    dato = df.iloc[st.session_state.second]

    st.markdown(f"""
    <div style='text-align: center; margin-top: 2px;'>
        <div style='font-size: 28px; font-weight: bold; color: #005EA8;'>
            {dato['Survival']:.1f}%
        </div>
        <div style='font-size: 12px; color: #444;'>Survival probability</div>
    </div>
    """, unsafe_allow_html=True)

    m1, m2 = st.columns(2)
    with m1:
        st.metric("Area %", f"{dato['Area%']:.3f}")
        st.metric("Dehydr. %/s", f"{dato['Vdeshidratacion']:.2f}%")
    with m2:
        st.metric("Circ.", f"{dato['Circularity']:.3f}")
        st.metric("Deplasm. %/s", f"{dato['Vdeplasmolisi']:.2f}%")

    st.image("slider_background_final.png", use_container_width=True)
    selected = st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed")
    if selected != st.session_state.second:
        st.session_state.second = selected
        st.session_state.playing = False
        st.experimental_rerun()

    # Botones en dos filas compactas
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⏪"):
            st.session_state.second = max(0, st.session_state.second - 1)
            st.session_state.playing = False
            st.experimental_rerun()
    with c2:
        if st.button("▶️ 1x"):
            st.session_state.playing = True
            st.session_state.speed = 1
    with c3:
        if st.button("⏩"):
            st.session_state.second = min(359, st.session_state.second + 1)
            st.session_state.playing = False
            st.experimental_rerun()

    c4, c5, c6 = st.columns(3)
    with c4:
        if st.button("⏸️"):
            st.session_state.playing = False
    with c5:
        if st.button("⏹️"):
            st.session_state.playing = False
            st.session_state.second = 0
            st.experimental_rerun()
    with c6:
        if st.button("▶️ 5x"):
            st.session_state.playing = True
            st.session_state.speed = 5

    # Logo compacto
    st.markdown("""
    <div style='text-align: center; margin-top: 5px;'>
        <a href='https://www.fertilab.com' target='_blank'>
            <img src='https://redinfertiles.com/wp-content/uploads/2022/04/logo-Barcelona.png' 
                 alt='Fertilab Barcelona' width='100'/>
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

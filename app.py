import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

# Configurar página
st.set_page_config(page_title="Oocyte Tracker", layout="wide")
st.markdown("""
    <h1 style='text-align: center; font-size: 28px;'>Vitrification Viability via Osmotic Response</h1>
""", unsafe_allow_html=True)

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
frame_path = f"frames/frame_{st.session_state.second}.jpg"
if os.path.exists(frame_path):
    image = Image.open(frame_path)
    st.image(image, caption=f"second {st.session_state.second}", use_container_width=True)
else:
    st.warning("No se encontró imagen.")

dato = df.iloc[st.session_state.second]
st.markdown(f"""
    <div style='text-align: center; margin-top: 1px;'>
        <div style='font-size: 60px; font-weight: bold; color: #005EA8;'>
            {dato['Survival']:.1f}%
        </div>
        <div style='font-size: 18px; color: #444;'>Probability of oocyte survival after vitrification</div>
    </div>
    <hr style="margin: 1px 0;">
""", unsafe_allow_html=True)

# Métricas centradas
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.markdown("<div style='text-align: center;'>Area %</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; font-size:18px'>{dato['Area%']:.3f}</div>", unsafe_allow_html=True)
with m_col2:
    st.markdown("<div style='text-align: center;'>Circularity</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; font-size:18px'>{dato['Circularity']:.3f}</div>", unsafe_allow_html=True)
with m_col3:
    st.markdown("<div style='text-align: center;'>Dehydration rate %/s</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; font-size:18px'>{dato['Vdeshidratacion']:.2f}%</div>", unsafe_allow_html=True)
with m_col4:
    st.markdown("<div style='text-align: center;'>Deplasmolysis rate %/s</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; font-size:18px'>{dato['Vdeplasmolisi']:.2f}%</div>", unsafe_allow_html=True)

# Slider
selected = st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed")
if selected != st.session_state.second:
    st.session_state.second = selected
    st.session_state.playing = False

# Botones en una línea
cols = st.columns(6)
if cols[0].button("⏪ Back"):
    st.session_state.second = max(0, st.session_state.second - 1)
    st.session_state.playing = False
if cols[1].button("▶️ Play 1x"):
    st.session_state.playing = True
    st.session_state.speed = 1
if cols[2].button("⏩ Forward"):
    st.session_state.second = min(359, st.session_state.second + 1)
    st.session_state.playing = False
if cols[3].button("⏸️ Pause"):
    st.session_state.playing = False
if cols[4].button("⏹️ Stop"):
    st.session_state.playing = False
    st.session_state.second = 0
if cols[5].button("▶️ Play 5x"):
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
        st.experimental_rerun()

# Logo más grande al final
st.markdown("""
    <div style='text-align: center; margin-top: 10px;'>
        <a href='https://www.fertilab.com' target='_blank'>
            <img src='https://redinfertiles.com/wp-content/uploads/2022/04/logo-Barcelona.png' 
                 alt='Fertilab Barcelona' width='250'/>
        </a>
    </div>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

st.set_page_config(page_title="Oocyte Tracker", layout="centered")
st.title("📸 Frame-by-Frame Oocyte Tracker")

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

# Contenedores visuales
image_placeholder = st.empty()
slider_placeholder = st.empty()
data_placeholder = st.empty()

# Mostrar contenido: imagen y datos
def mostrar_contenido():
    with image_placeholder.container():
        frame_path = f"frames/frame_{st.session_state.second}.jpg"
        if os.path.exists(frame_path):
            image = Image.open(frame_path)
            st.image(image, caption=f"Segundo {st.session_state.second}", use_container_width=True)
        else:
            st.warning(f"No se encontró imagen para el segundo {st.session_state.second}")
    with data_placeholder.container():
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

# Mostrar fondo del slider (gráfico)
st.image("slider_background_final.png", use_container_width=True)

# Mostrar contenido actual
mostrar_contenido()

# Slider si


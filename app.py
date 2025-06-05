import streamlit as st
import pandas as pd
from PIL import Image
import os

# Configurar la página
st.set_page_config(page_title="Oocyte Tracker by Frame", layout="centered")
st.title("📸 Frame-by-Frame Oocyte Tracker")

# Cargar datos
df = pd.read_csv("AioocyteV1.csv", sep=";")
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace('%', '', regex=False)
        df[col] = df[col].str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Slider para seleccionar el segundo
second = st.slider("🕒 Elige segundo del vídeo", 0, min(len(df)-1, 359), 0)

# Mostrar imagen correspondiente al segundo
frame_path = f"frames/frame_{second}.jpg"
if os.path.exists(frame_path):
    image = Image.open(frame_path)
    st.image(image, caption=f"Segundo {second}", use_container_width=True)
else:
    st.warning(f"No se encontró la imagen para el segundo {second}")

# Mostrar datos
dato = df.iloc[second]
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


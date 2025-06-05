
import streamlit as st
import pandas as pd
from streamlit_javascript import st_javascript
import base64

st.set_page_config(page_title="Oocyte Vitrification Tracker", layout="centered")
st.title("🧬 Video-Time Synced Oocyte Tracker")

# Cargar los datos
df = pd.read_csv("AioocyteV1.csv", sep=";")
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace('%', '', regex=False)
        df[col] = df[col].str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Codificar video en base64 para incrustarlo
with open("Oocyte osmotic behavior.mp4", "rb") as f:
    video_bytes = f.read()
    video_b64 = base64.b64encode(video_bytes).decode()

# Mostrar video con ID específico para capturar currentTime desde JS
st.markdown(f"""
    <video id="myvideo" width="100%" autoplay muted controls>
        <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
""", unsafe_allow_html=True)

# Ejecutar JS para obtener el tiempo actual del video
current_time = st_javascript("Math.floor(document.getElementById('myvideo')?.currentTime || 0)")

# Mostrar datos correspondientes al segundo actual
if current_time is not None and 0 <= current_time < len(df):
    dato = df.iloc[int(current_time)]
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
else:
    st.info("Waiting for video playback...")

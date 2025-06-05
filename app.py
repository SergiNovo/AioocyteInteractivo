import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="Oocyte Vitrification Tracker", layout="centered")
st.title("🧬 Oocyte Behavior Viewer (Slider Controlled)")

# Cargar datos
df = pd.read_csv("AioocyteV1.csv", sep=";")
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace('%', '', regex=False)
        df[col] = df[col].str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Cargar y mostrar el video en base64
with open("Oocyte osmotic behavior.mp4", "rb") as f:
    video_bytes = f.read()
    video_b64 = base64.b64encode(video_bytes).decode()

st.markdown(f"""
    <video width="100%" controls>
        <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
""", unsafe_allow_html=True)

# Slider para seleccionar segundo
second = st.slider("🕒 Selecciona el segundo del video", min_value=0, max_value=min(len(df)-1, 359), value=0)

# Mostrar datos correspondientes al segundo
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

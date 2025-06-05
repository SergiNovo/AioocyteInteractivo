import streamlit as st
import pandas as pd
import time

# Título
st.set_page_config(page_title="Oocyte Vitrification Tracking", layout="centered")
st.title("🧪 Oocyte Osmotic Behavior During Vitrification")

# Cargar video y datos
video_file = open("Oocyte osmotic behavior.mp4", "rb")
video_bytes = video_file.read()
df = pd.read_csv("AioocyteV1.csv", sep=";")

# Convertir columnas numéricas
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace('%', '', regex=False)
        df[col] = df[col].str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Mostrar video
st.video(video_bytes)

# Botón de inicio
if st.button("▶️ Start Playback"):
    # Zona para los datos dinámicos
    data_placeholder = st.empty()
    for t in range(0, min(len(df), 360)):
        dato = df.iloc[t]

        with data_placeholder.container():
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

        time.sleep(1)  # Esperar 1 segundo para simular la reproducción

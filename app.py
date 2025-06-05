
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="Oocyte Vitrification Tracker", layout="centered")
st.title("🧬 Interactive Video Tracking: Oocyte Behavior")

# Leer los datos
df = pd.read_csv("AioocyteV1.csv", sep=";")
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace('%', '', regex=False)
        df[col] = df[col].str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Crear componente HTML con video y JavaScript que manda el tiempo actual
components.html("""
    <video id="video" width="100%" controls autoplay muted ontimeupdate="sendTime()">
        <source src="Oocyte osmotic behavior.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    <script>
        const streamlitSend = window.parent.postMessage || (() => {});
        function sendTime() {
            const video = document.getElementById("video");
            const currentTime = Math.floor(video.currentTime);
            streamlitSend({ isStreamlitMessage: true, type: "streamlit:setComponentValue", value: currentTime }, "*");
        }
    </script>
""", height=360)

# Obtener valor del segundo actual enviado desde JS (requiere usar st.experimental_get_query_params solo como placeholder)
second = st.experimental_get_query_params().get("value", [0])[0]
try:
    second = int(second)
except:
    second = 0

# Mostrar datos si el segundo está en rango
if 0 <= second < len(df):
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
else:
    st.info("Waiting for video interaction...")

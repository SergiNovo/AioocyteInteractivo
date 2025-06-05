import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Configurar página
st.set_page_config(page_title="Oocyte Vitrification Tracker", layout="centered")
st.title("🧬 Interactive Video Tracking: Oocyte Behavior")

# Leer datos
df = pd.read_csv("AioocyteV1.csv", sep=";")
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace('%', '', regex=False)
        df[col] = df[col].str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Crear componente de video con JS que devuelve currentTime
components.html("""
    <script>
        const streamlitSend = window.parent.postMessage || (() => {});
        let sentTime = -1;
        function init() {
            const video = document.getElementById("video");
            video.addEventListener("timeupdate", () => {
                const t = Math.floor(video.currentTime);
                if (t !== sentTime) {
                    sentTime = t;
                    const data = {{ "isStreamlitMessage": true, "type": "streamlit:setComponentValue", "value": t }};
                    window.parent.postMessage(data, "*");
                }
            });
        }
    </script>
    <video id="video" width="100%" controls autoplay muted oncanplay="init()">
        <source src="Oocyte osmotic behavior.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
""", height=360)

# Componente "falso" para recibir el valor actual del tiempo desde JS (desde postMessage)
video_second = components.declare_component("video_timer", default=0)

# Mostrar datos correspondientes
if 0 <= video_second < len(df):
    dato = df.iloc[video_second]
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

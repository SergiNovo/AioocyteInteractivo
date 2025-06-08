ximport streamlit as st
import pandas as pd
from PIL import Image
import os
import time

st.set_page_config(page_title="Vitrification Viability via Osmotic Response", layout="wide")
st.markdown("<h1 style='text-align: center;'>Vitrification Viability via Osmotic Response</h1>", unsafe_allow_html=True)

# Cargar datos
df = pd.read_csv("AioocyteV1.csv", sep=";")
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace('%', '', regex=False)
        df[col] = df[col].str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

if "second" not in st.session_state:
    st.session_state.second = 0
if "playing" not in st.session_state:
    st.session_state.playing = False
if "speed" not in st.session_state:
    st.session_state.speed = 1

# Bloques secuenciales (uno debajo de otro)
video_placeholder = st.empty()
supervivencia_placeholder = st.empty()
metrics_placeholder = st.empty()
grafico_placeholder = st.empty()
slider_placeholder = st.empty()
controles_placeholder = st.empty()
logo_placeholder = st.empty()

def mostrar_contenido():
    # 1. Video/frame arriba del todo
    frame_path = f"frames/frame_{st.session_state.second}.jpg"
    with video_placeholder:
        if os.path.exists(frame_path):
            image = Image.open(frame_path)
            st.image(image, caption=f"second {st.session_state.second}", use_container_width=True)
        else:
            st.warning("No se encontró imagen.")

    # 2. Supervivencia (MUY GRANDE)
    dato = df.iloc[st.session_state.second]
    with supervivencia_placeholder:
        st.markdown(f"""
            <div style='text-align: center; margin-top: 6px; margin-bottom: 0px;'>
                <div style='font-size: 64px; font-weight: bold; color: #005EA8; line-height: 0.9;'>
                    {dato['Survival']:.1f}%
                </div>
                <div style='font-size: 18px; color: #444;'>Probability of oocyte survival after vitrification</div>
            </div>
            <hr style="margin: 1px 0;">
        """, unsafe_allow_html=True)
    # 3. Métricas: en una sola línea, cada una con título encima, número debajo, todo ancho
    with metrics_placeholder:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(
                f"""
                <div style='text-align:center;'>
                    <div style='font-size:16px; color:#888;'>Area %</div>
                    <div style='font-size:26px; font-weight:bold; color:#222'>{dato['Area%']:.3f}</div>
                </div>
                """, unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f"""
                <div style='text-align:center;'>
                    <div style='font-size:16px; color:#888;'>Circularity</div>
                    <div style='font-size:26px; font-weight:bold; color:#222'>{dato['Circularity']:.3f}</div>
                </div>
                """, unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                f"""
                <div style='text-align:center;'>
                    <div style='font-size:16px; color:#888;'>Dehyd. rate<br>%/s</div>
                    <div style='font-size:26px; font-weight:bold; color:#222'>{dato['Vdeshidratacion']:.2f}%</div>
                </div>
                """, unsafe_allow_html=True
            )
        with col4:
            st.markdown(
                f"""
                <div style='text-align:center;'>
                    <div style='font-size:16px; color:#888;'>Deplasmo. rate<br>%/s</div>
                    <div style='font-size:26px; font-weight:bold; color:#222'>{dato['Vdeplasmolisi']:.2f}%</div>
                </div>
                """, unsafe_allow_html=True
            )
    # 4. Gráfico
    with grafico_placeholder:
        st.image("slider_background_final.png", use_container_width=True)

def render_slider():
    # 5. Slider
    with slider_placeholder:
        selected = st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed")
        if selected != st.session_state.second:
            st.session_state.second = selected
            st.session_state.playing = False
            mostrar_contenido()
            mostrar_logo()  # <- Para que el logo no desaparezca

def mostrar_logo():
    with logo_placeholder:
        st.markdown("""
        <div style='text-align: center; margin-top: 10px;'>
            <a href='https://www.fertilab.com' target='_blank'>
                <img src='https://redinfertiles.com/wp-content/uploads/2022/04/logo-Barcelona.png' 
                     alt='Fertilab Barcelona' width='160'/>
            </a>
        </div>
        """, unsafe_allow_html=True)

# Mostramos todo en el orden definido
mostrar_contenido()
render_slider()
mostrar_logo()

# 6. Controles (todos visibles)
with controles_placeholder:
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        if st.button("⏪ Back"):
            st.session_state.second = max(0, st.session_state.second - 1)
            st.session_state.playing = False
            mostrar_contenido()
            render_slider()
            mostrar_logo()
    with col2:
        if st.button("▶️ Play 1x"):
            st.session_state.playing = True
            st.session_state.speed = 1
    with col3:
        if st.button("⏩ Forward"):
            st.session_state.second = min(359, st.session_state.second + 1)
            st.session_state.playing = False
            mostrar_contenido()
            render_slider()
            mostrar_logo()
    with col4:
        if st.button("⏸️ Pause"):
            st.session_state.playing = False
    with col5:
        if st.button("⏹️ Stop"):
            st.session_state.playing = False
            st.session_state.second = 0
            mostrar_contenido()
            render_slider()
            mostrar_logo()
    with col6:
        if st.button("⏩ Play 5x"):
            st.session_state.playing = True
            st.session_state.speed = 5

# Auto-reproducción (el logo siempre se mantiene)
if st.session_state.playing:
    for _ in range(500):
        if not st.session_state.playing or st.session_state.second >= 359:
            st.session_state.playing = False
            break
        time.sleep(0.5)
        st.session_state.second = min(359, st.session_state.second + st.session_state.speed)
        mostrar_contenido()
        render_slider()
        mostrar_logo()


import streamlit as st
import pandas as pd
from PIL import Image
import os
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Google Sheets Setup ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("oocyteapp-466eb887b9c6.json", scope)
client = gspread.authorize(creds)

# Replace with your actual sheet URL or name
SHEET_URL = "https://docs.google.com/spreadsheets/d/1qFG0rtDvhixp-fo4gKnYUYpM37DoLNjwqqkJVT-IZiw/edit"
worksheet = client.open_by_url(SHEET_URL).sheet1

# --- Login/Register Interface ---
st.set_page_config(page_title="Oocyte Tracker", layout="wide")
st.markdown("<h1 style='text-align: center;'>Vitrification Viability via Osmotic Response</h1>", unsafe_allow_html=True)

with st.form("login_form"):
    st.markdown("#### Please register to access the app:")
    full_name = st.text_input("Full name")
    profession = st.text_input("Profession")
    country = st.text_input("Country of practice")
    email = st.text_input("Email")
    submitted = st.form_submit_button("Submit and Enter App")

if not submitted:
    st.stop()

# Save user to Google Sheet
try:
    worksheet.append_row([full_name, profession, country, email, time.strftime("%Y-%m-%d %H:%M:%S")])
except Exception as e:
    st.error(f"⚠️ Error saving to Google Sheets: {e}")
    st.stop()

# --- Load Data ---
df = pd.read_csv("AioocyteV1.csv", sep=";")
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace('%', '', regex=False)
        df[col] = df[col].str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# --- Session State ---
if "second" not in st.session_state:
    st.session_state.second = 0
if "playing" not in st.session_state:
    st.session_state.playing = False
if "speed" not in st.session_state:
    st.session_state.speed = 1

# --- Layout ---
col_video, col_data = st.columns([2, 3])
video_placeholder = col_video.empty()
survival_placeholder = col_data.empty()
metrics_placeholder = col_data.empty()
graph_placeholder = col_data.empty()
slider_placeholder = col_data.empty()
controls_placeholder = col_data.empty()

# --- Display Content ---
def show_content():
    frame_path = f"frames/frame_{st.session_state.second}.jpg"
    with video_placeholder:
        if os.path.exists(frame_path):
            image = Image.open(frame_path)
            st.image(image, caption=f"Second {st.session_state.second}", use_container_width=True)
        else:
            st.warning("Image not found.")

    data = df.iloc[st.session_state.second]
    with survival_placeholder:
        st.markdown(f"""
            <div style='text-align: center; margin-top: 1px;'>
                <div style='font-size: 50px; font-weight: bold; color: #005EA8;'>
                    {data['Survival']:.1f}%
                </div>
                <div style='font-size: 20px; color: #444;'>Probability of oocyte survival after vitrification</div>
            </div>
            <hr style="margin: 1px 0;">
        """, unsafe_allow_html=True)

    with metrics_placeholder:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Area %", f"{data['Area%']:.3f}")
        m2.metric("Circularity", f"{data['Circularity']:.3f}")
        m3.metric("Dehydration rate %/s", f"{data['Vdeshidratacion']:.2f}%")
        m4.metric("Deplasmolysis rate %/s", f"{data['Vdeplasmolisi']:.2f}%")

    with graph_placeholder:
        st.image("slider_background_final.png", use_container_width=True)

# --- Slider ---
def render_slider():
    with slider_placeholder:
        selected = st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed")
        if selected != st.session_state.second:
            st.session_state.second = selected
            st.session_state.playing = False
            show_content()

# --- Initial content ---
show_content()
render_slider()

# --- Controls ---
with controls_placeholder:
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        if st.button("⏪ Back"):
            st.session_state.second = max(0, st.session_state.second - 1)
            st.session_state.playing = False
            show_content()
            render_slider()
    with c2:
        if st.button("▶️ Play 1x"):
            st.session_state.playing = True
            st.session_state.speed = 1
    with c3:
        if st.button("⏩ Forward"):
            st.session_state.second = min(359, st.session_state.second + 1)
            st.session_state.playing = False
            show_content()
            render_slider()
    with c4:
        if st.button("⏸️ Pause"):
            st.session_state.playing = False
    with c5:
        if st.button("⏹️ Stop"):
            st.session_state.playing = False
            st.session_state.second = 0
            show_content()
            render_slider()
    with c6:
        if st.button("⏩ Play 5x"):
            st.session_state.playing = True
            st.session_state.speed = 5

# --- Autoplay ---
if st.session_state.playing:
    for _ in range(500):
        if not st.session_state.playing or st.session_state.second >= 359:
            st.session_state.playing = False
            break
        time.sleep(0.5)
        st.session_state.second = min(359, st.session_state.second + st.session_state.speed)
        show_content()
        render_slider()

# --- Logo ---
with col_data:
    st.markdown("""
    <div style='text-align: center; margin-top: 10px;'>
        <a href='https://www.fertilab.com' target='_blank'>
            <img src='https://redinfertiles.com/wp-content/uploads/2022/04/logo-Barcelona.png' 
                 alt='Fertilab Barcelona' width='200'/>
        </a>
    </div>
    """, unsafe_allow_html=True)

import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

st.set_page_config(page_title="Vitrification Viability via Osmotic Response", layout="wide")

# SESSION STATE: check login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# USER LOGIN FORM
if not st.session_state.logged_in:
    st.title("Access the App")

    with st.form("user_form"):
        name = st.text_input("Full Name")
        profession = st.text_input("Profession")
        country = st.text_input("Country")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Enter App")

    if submitted and all([name, profession, country, email]):
        user_data = {
            "Name": name,
            "Profession": profession,
            "Country": country,
            "Email": email
        }

        if os.path.exists("users.csv"):
            df_users = pd.read_csv("users.csv")
            df_users = pd.concat([df_users, pd.DataFrame([user_data])], ignore_index=True)
        else:
            df_users = pd.DataFrame([user_data])

        df_users.to_csv("users.csv", index=False)
        st.session_state.logged_in = True
        st.rerun()

# --- APP CONTENT START ---
if st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>Vitrification Viability via Osmotic Response</h1>", unsafe_allow_html=True)

    # Load data
    df = pd.read_csv("AioocyteV1.csv", sep=";")
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.replace('%', '', regex=False)
            df[col] = df[col].str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Initial state
    if "second" not in st.session_state:
        st.session_state.second = 0
    if "playing" not in st.session_state:
        st.session_state.playing = False
    if "speed" not in st.session_state:
        st.session_state.speed = 1

    # Layout
    col_video, col_data = st.columns([2, 3])
    video_placeholder = col_video.empty()
    survival_placeholder = col_data.empty()
    metrics_placeholder = col_data.empty()
    graph_placeholder = col_data.empty()
    slider_placeholder = col_data.empty()
    controls_placeholder = col_data.empty()

    def show_content():
        frame_path = f"frames/frame_{st.session_state.second}.jpg"
        with video_placeholder:
            if os.path.exists(frame_path):
                image = Image.open(frame_path)
                st.image(image, caption=f"Second {st.session_state.second}", use_container_width=True)
            else:
                st.warning("Frame not found.")

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

    def render_slider():
        with slider_placeholder:
            selected = st.slider("🕒", 0, 359, value=st.session_state.second, label_visibility="collapsed", key="slider")
            if selected != st.session_state.second:
                st.session_state.second = selected
                st.session_state.playing = False
                show_content()

    # Initial display
    show_content()
    render_slider()

    # Controls
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

    # Auto-play loop
    if st.session_state.playing:
        for _ in range(500):
            if not st.session_state.playing or st.session_state.second >= 359:
                st.session_state.playing = False
                break
            time.sleep(0.5)
            st.session_state.second = min(359, st.session_state.second + st.session_state.speed)
            show_content()
            render_slider()

    # Logo below buttons
    with col_data:
        st.markdown("""
        <div style='text-align: center; margin-top: 10px;'>
            <a href='https://www.fertilab.com' target='_blank'>
                <img src='https://redinfertiles.com/wp-content/uploads/2022/04/logo-Barcelona.png' 
                     alt='Fertilab Barcelona' width='200'/>
            </a>
        </div>
        """, unsafe_allow_html=True)

import streamlit as st


st.set_page_config(
  page_title="Soccer Stats - Détection des passes",
  page_icon="📸",
  layout="centered"
)

# Title
st.title("📸 Détections des passes")

video_url = "src/top_view/full_game_2D_passe.mp4"
st.video(video_url, start_time=0, format='video/mp4')
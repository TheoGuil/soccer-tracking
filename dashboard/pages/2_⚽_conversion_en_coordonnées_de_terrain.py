import streamlit as st


st.set_page_config(
  page_title="Soccer Stats - Conversion en coordonnées de terrain",
  page_icon="⚽",
  layout="wide"
)

# Title
st.title("⚽ Conversion en coordonnées de terrain")

pitch_coordinates_url = "src/top_view/pitch_coordinate_D_20220220_1_0000_0030.csv"
video_url = "src/top_view/D_20220220_1_0000_0030.mp4"
two_dim_video_url = "src/top_view/2D_short_video.mp4"

col1, col2 = st.columns(2)

with col1:
    st.subheader("Vidéo annotée")
    st.video(video_url, start_time=0, format='video/mp4')

with col2:
    st.subheader("Vidéo 2D")
    st.video(two_dim_video_url, start_time=0, format='video/mp4')
    
    
st.subheader("Explication")
st.markdown('''
    Pour obtenir les coordonnées de terrain, nous avons besoin de connaitre
    les coordonnées de la caméra et les coordonnées du terrains, ce qui nous permet de 
    calculer la matrice de projection (3x3). Celle-ci permet de transformer un plan en 
    8 degrés de liberté.
''')
st.markdown('''
    <center> 
        <span class="mw-default-size" typeof="mw:File">
            <img src="//upload.wikimedia.org/wikipedia/commons/a/a2/France1.gif" decoding="async" width="212" height="231" class="mw-file-element" data-file-width="212" data-file-height="231">
        </span> 
        ➪ 
        <span class="mw-default-size" typeof="mw:File">
            <img src="//upload.wikimedia.org/wikipedia/commons/0/02/France_homographie_%281%29.gif" decoding="async" width="285" height="202" class="mw-file-element" data-file-width="285" data-file-height="202">
        </span>
    </center>
''', unsafe_allow_html=True)

st.text("Source de l'image : https://fr.wikipedia.org/wiki/Application_projective")

st.link_button("Plus d'informations", "https://docs.opencv.org/4.x/d9/dab/tutorial_homography.html")
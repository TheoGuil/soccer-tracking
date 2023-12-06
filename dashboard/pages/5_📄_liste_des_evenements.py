import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import json

st.set_page_config(
  page_title="Soccer Stats - Liste des événements",
  page_icon="📄",
  layout="wide"
)

# Title
st.title("📄 Liste des événements")

passes_url = "src/stats/passes.json"
video_url = "src/top_view/full_game_2D_passe.mp4"

# load the data
@st.cache_data(show_spinner="Chargement des données")
def load_datas():
    file = open(passes_url, "r")
    data = json.load(file)
    df = pd.json_normalize(data, "actions")
    return df
  
datas = load_datas()

# select the columns you want the users to see
gb = GridOptionsBuilder.from_dataframe(datas)
# configure selection
gb.configure_selection(selection_mode="single", use_checkbox=True)
gb.configure_side_bar()
gridOptions = gb.build()

grid = AgGrid(datas,
       gridOptions=gridOptions)

selected_row = grid["selected_rows"]

if (selected_row):
  start_time = int(selected_row[0]["start"] / 30) - 2
  if (start_time < 0):
    start_time = 0
    
  col1, col2 = st.columns(2, gap="large")
  with col1:
    st.video(video_url, start_time=start_time, format='video/mp4')
    
  with col2:
    st.subheader("Détails de l'événement")
    st.write(f"Début : {round(selected_row[0]['start'] / 30, 2)} secondes")
    st.write(f"Durée : {round((selected_row[0]['end'] - selected_row[0]['start']) / 30, 2)} secondes")
    st.write(f"Type : {selected_row[0]['type']}")
    st.write(f"Joueur : n°{selected_row[0]['passeur']} {'🔵' if selected_row[0]['team_passeur'] == 0 else '🔴'}")
    
    
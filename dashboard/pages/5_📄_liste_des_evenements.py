import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
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
    df["team_passeur"] = df["team_passeur"].apply(lambda x: "🔵" if x == 0 else "🔴")
    df["team_receveur"] = df["team_receveur"].apply(lambda x: "🔵" if x == 0 else "🔴")
    df["succeed"] = df["succeed"].apply(lambda x: "🗹" if x == 1 else "☐")
    df["second_start"] = df["start"].apply(lambda x: round(x / 30, 2))
    df["second_duration"] = df.apply(lambda x: round((x["end"] - x["start"]) / 30, 2), axis=1)
    return df
  
datas = load_datas()

# select the columns you want the users to see
gb = GridOptionsBuilder.from_dataframe(datas[['id', 'second_start', 'second_duration', 'type', 'passeur', 'team_passeur', 'receveur', 'team_receveur', 'succeed']])
# configure selection
gb.configure_selection(selection_mode="single", use_checkbox=True)
gb.configure_side_bar()
gridOptions = gb.build()

grid = AgGrid(datas,
       gridOptions=gridOptions,
       height=332,
       columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
       theme="alpine")

selected_row = grid["selected_rows"]

if (selected_row):
  start_time = int(selected_row[0]["second_start"]) - 1
  if (start_time < 0):
    start_time = 0
    
  col1, col2 = st.columns(2, gap="large")
  with col1:
    st.video(video_url, start_time=start_time, format='video/mp4')
    
  with col2:
    st.subheader("Détails de l'événement")
    st.write(f"Début : {selected_row[0]['second_start']} secondes")
    st.write(f"Durée : {selected_row[0]['second_duration']} secondes")
    st.write(f"Type : {selected_row[0]['type']}")
    st.write(f"Joueur : n°{selected_row[0]['passeur']} {selected_row[0]['team_passeur']} {'⟶ n°' + str(selected_row[0]['receveur']) + ' ' + selected_row[0]['team_receveur'] if selected_row[0]['succeed'] == '🗹' else ''}")
    if (selected_row[0]["succeed"] == "🗹"):
      st.write(f"<span style='background:green; color:white; padding:5px; border-radius:10px;'>Réussi<span>", unsafe_allow_html = True)
    else:
      st.write(f"<span style='background:red; color:white; padding:5px; border-radius:10px;'>Echec<span>", unsafe_allow_html = True)
    
    
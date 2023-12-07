import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from scripts.soccer_graph import *


st.set_page_config(
  page_title="Soccer Stats - Statistiques",
  page_icon="📈",
  layout="wide"
)

PASSES_URL = 'src/stats/all_passe_with_coordinates.csv'
POSITIONS_URL = 'src/stats/mean_position.csv'
PASSES_RELATION_URL = 'src/stats/pass_relation.csv'
TEAM_STATS_URL = 'src/stats/stats_team.json'

@st.cache_data(show_spinner="Chargement des données")
def load_pass():
    data = pd.read_csv(PASSES_URL, index_col=0)
    return data
  
@st.cache_data(show_spinner="Chargement des données")
def load_position():
    data = pd.read_csv(POSITIONS_URL, index_col=0)
    data = data.rename({'pass_count': 'count'}, axis=1)
    return data
  
@st.cache_data(show_spinner="Chargement des données")
def load_pass_relation():
    data = pd.read_csv(PASSES_RELATION_URL, index_col=0)
    return data
  
@st.cache_data(show_spinner="Chargement des données")
def load_team_stats():
    data = pd.read_json(TEAM_STATS_URL)
    data = data.transpose()
    stats_key = data.columns
    for key in stats_key:
        data[key+"_per"] = data[key]/data[key].sum()
    return data, stats_key, [key+"_per" for key in stats_key], [key.replace('_', ' ').title() for key in stats_key]

# Title
st.title("📈 Statistiques")

# comparaison de stats équipes
team_stats, stats, stats_per, stats_label = load_team_stats()
team_list = ["Équipe 1", "Équipe 2"]
team_color = ['rgba(0, 0, 255, 0.8)', 'rgba(255, 0, 0, 0.8)']

fig = get_performance_chart(team_stats, stats, stats_per, stats_label, team_list, team_color)
st.plotly_chart(fig)

# Choix de l'équipe
team = st.radio("Choix de l'équipe", team_list, horizontal=True)

team_id = 0 if team == "Équipe 1" else 1

col1, col2 = st.columns(2)

# Toutes les passes
with col1 :
  pass_df = load_pass()
  fig = get_pass_graph(pass_df.loc[pass_df['team_start'] == team_id], 
                        pass_df["successful"] == True, 
                        f"Passes de l'{team.lower()}")
  st.pyplot(fig)

# Réseau de passes
with col2 :
  positions = load_position()
  pass_relation = load_pass_relation()
  
  network_fig = get_pass_network(positions.loc[positions['TeamID'] == team_id],
                                  pass_relation.loc[pass_relation['team'] == team_id],
                                  f"Réseau de passes de l'{team.lower()}",)
  st.pyplot(network_fig)

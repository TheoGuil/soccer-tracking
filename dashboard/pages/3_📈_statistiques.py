import streamlit as st
from scripts.soccer_graph import *
from mplsoccer import Sbopen

st.set_page_config(
  page_title="Soccer Stats - Statistiques",
  page_icon="📈",
  layout="centered"
)

# Title
st.title("📈 Statistiques")

# temporaire le temps que l'on collecte les données de la vidéo
statsBomb = Sbopen()
df, _, _, _ = statsBomb.event(7478)
team1, team2 = df.team_name.unique()
mask_team1 = (df.type_name == 'Pass') & (df.team_name == team1)
df_pass = df.loc[mask_team1, ['x', 'y', 'end_x', 'end_y', 'outcome_name']]

fig = get_pass_graph(df_pass, df_pass.outcome_name.isnull(), f'{team1} passes vs {team2}')
st.pyplot(fig)
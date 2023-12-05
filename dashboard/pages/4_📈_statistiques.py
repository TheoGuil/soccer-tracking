import streamlit as st
from scripts.soccer_graph import *
from mplsoccer import Sbopen

import pandas as pd

st.set_page_config(
  page_title="Soccer Stats - Statistiques",
  page_icon="📈",
  layout="wide"
)

PASSES_URL = 'src/stats/all_passe_with_coordinates.csv'
POSITIONS_URL = 'src/stats/mean_position.csv'
PASSES_RELATION_URL = 'src/stats/pass_relation.csv'

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

# Title
st.title("📈 Statistiques")

# tab1, tab2 = st.tabs(["Open data par StatsBomb", "Données calculées"])



# Données calculées
# with tab2:
team = st.radio("Choix de l'équipe", 
          ["Équipe 1", "Équipe 2"],
          horizontal=True)

team_id = 0 if team == "Équipe 1" else 1

col1, col2 = st.columns(2)

with col1 :
  pass_df = load_pass()
  fig = get_pass_graph(pass_df.loc[pass_df['team_start'] == team_id], 
                        pass_df["successful"] == True, 
                        f"Passes de l'{team.lower()}")
  st.pyplot(fig)
  
with col2 :
  positions = load_position()
  pass_relation = load_pass_relation()
  
  network_fig = get_pass_network(positions.loc[positions['TeamID'] == team_id],
                                  pass_relation.loc[pass_relation['team'] == team_id],
                                  f"Réseau de passes de l'{team.lower()}",)
  st.pyplot(network_fig)
    
    
    
# Open data
# with tab1:
#   col1, col2 = st.columns(2)

#   # temporaire le temps que l'on collecte les données de la vidéo
#   statsBomb = Sbopen()
#   df, _, _, players = statsBomb.event(15946)
#   team1, team2 = df.team_name.unique()
#   mask_team1 = (df.type_name == 'Pass') & (df.team_name == team1)
#   df_pass = df.loc[mask_team1, ['x', 'y', 'end_x', 'end_y', 'outcome_name']]

#   # Display the pass graph
#   with col1:
#       fig = get_pass_graph(df_pass, df_pass.outcome_name.isnull(), f'{team1} passes vs {team2}', 'statsbomb')
#       st.pyplot(fig)

#   # temporaire le temps que l'on collecte les données de la vidéo
#   df.loc[df.tactics_formation.notnull(), 'tactics_id'] = df.loc[
#       df.tactics_formation.notnull(), 'id']
#   df[['tactics_id', 'tactics_formation']] = df.groupby('team_name')[[
#       'tactics_id', 'tactics_formation']].ffill()

#   formation_dict = {1: 'GK', 2: 'RB', 3: 'RCB', 4: 'CB', 5: 'LCB', 6: 'LB', 7: 'RWB',
#                     8: 'LWB', 9: 'RDM', 10: 'CDM', 11: 'LDM', 12: 'RM', 13: 'RCM',
#                     14: 'CM', 15: 'LCM', 16: 'LM', 17: 'RW', 18: 'RAM', 19: 'CAM',
#                     20: 'LAM', 21: 'LW', 22: 'RCF', 23: 'ST', 24: 'LCF', 25: 'SS'}
#   players['position_abbreviation'] = players.position_id.map(formation_dict)

#   sub = df.loc[df.type_name == 'Substitution',
#                   ['tactics_id', 'player_id', 'substitution_replacement_id',
#                     'substitution_replacement_name']]
#   players_sub = players.merge(sub.rename({'tactics_id': 'id'}, axis='columns'),
#                               on=['id', 'player_id'], how='inner', validate='1:1')
#   players_sub = (players_sub[['id', 'substitution_replacement_id', 'position_abbreviation']]
#                 .rename({'substitution_replacement_id': 'player_id'}, axis='columns'))
#   players = pd.concat([players, players_sub])
#   players.rename({'id': 'tactics_id'}, axis='columns', inplace=True)
#   players = players[['tactics_id', 'player_id', 'position_abbreviation']]

#   # add on the position the player was playing in the formation to the events dataframe
#   df = df.merge(players, on=['tactics_id', 'player_id'], how='left', validate='m:1')
#   # add on the position the receipient was playing in the formation to the events dataframe
#   df = df.merge(players.rename({'player_id': 'pass_recipient_id'},
#                                       axis='columns'), on=['tactics_id', 'pass_recipient_id'],
#                         how='left', validate='m:1', suffixes=['', '_receipt'])

#   FORMATION = '433'
#   pass_cols = ['id', 'position_abbreviation', 'position_abbreviation_receipt']
#   passes_formation = df.loc[(df.team_name == team1) & (df.type_name == 'Pass') &
#                                 (df.tactics_formation == FORMATION) &
#                                 (df.position_abbreviation_receipt.notnull()), pass_cols].copy()
#   location_cols = ['position_abbreviation', 'x', 'y']
#   location_formation = df.loc[(df.team_name == team1) &
#                                   (df.type_name.isin(['Pass', 'Ball Receipt'])) &
#                                   (df.tactics_formation == FORMATION), location_cols].copy()

#   # average locations
#   average_locs_and_count = (location_formation.groupby('position_abbreviation')
#                             .agg({'x': ['mean'], 'y': ['mean', 'count']}))
#   average_locs_and_count.columns = ['x', 'y', 'count']
#   average_locs_and_count["PlayerID"] = average_locs_and_count.index

#   # calculate the number of passes between each position (using min/ max so we get passes both ways)
#   passes_formation['pos_max'] = (passes_formation[['position_abbreviation',
#                                                   'position_abbreviation_receipt']]
#                                 .max(axis='columns'))
#   passes_formation['pos_min'] = (passes_formation[['position_abbreviation',
#                                                   'position_abbreviation_receipt']]
#                                 .min(axis='columns'))
#   passes_between = passes_formation.groupby(['pos_min', 'pos_max']).id.count().reset_index()
#   passes_between.rename({'id': 'pass_count'}, axis='columns', inplace=True)

#   # add on the location of each player so we have the start and end positions of the lines
#   passes_between = passes_between.merge(average_locs_and_count, left_on='pos_min', right_index=True)
#   passes_between = passes_between.merge(average_locs_and_count, left_on='pos_max', right_index=True,
#                                         suffixes=['', '_end'])


#   # Display the pass network
#   with col2:
#     network_fig = get_pass_network(average_locs_and_count, passes_between, f'{team1} passes network vs {team2}', 'statsbomb')
#     st.pyplot(network_fig)
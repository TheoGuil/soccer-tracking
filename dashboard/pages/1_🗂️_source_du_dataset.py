import streamlit as st
import pandas as pd
import json

st.set_page_config(
  page_title="Soccer Stats - Source du dataset",
  page_icon="⚽",
  layout="centered"
)

# Title
st.title("🗂️ Source du dataset")


# Define the urls
orginal_dataset_url = "src/top_view/original_D_20220220_1_0000_0030.csv"
gnss_url = "src/top_view/gnss_G_20200220_1_0000_0030.csv"
key_point_url = "src/top_view/drone_keypoints.json"


# load the data
@st.cache_data(show_spinner="Chargement des données")
def load_datas():
    original_data = pd.read_csv(orginal_dataset_url, nrows=10, header=None)
    gnss_data = pd.read_csv(gnss_url, nrows=10, header=None)
    key_point_data = json.load(open(key_point_url))
    return original_data, gnss_data, key_point_data

original_data, gnss_data, key_point_data = load_datas()


st.header("Dataset originel")
st.dataframe(original_data, hide_index=True)


st.header("GNSS Dataset")
st.dataframe(gnss_data, hide_index=True)


st.header("Drone Keypoint")
st.json(key_point_data, expanded=True)

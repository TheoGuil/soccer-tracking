import streamlit as st

st.set_page_config(
  page_title="Soccer Stats - Home",
  page_icon="⚽",
  layout="centered"
)

# Title
st.title("Obtention de statistiques via la retransmission d'un match")

st.markdown('''
        Ce projet a pour but de récupérer des statistiques sur un match de football à partir de la retransmission de celui-ci.
        
        A partir de la position des joueurs et du ballon, nous allons calculer des statistiques sur le match.
        
        A ce stade, nous nous sommes concentrés sur les passes.
''')
st.empty()

st.markdown('''<hr/>''', unsafe_allow_html=True)

st.markdown('''
    Les données proviennent d'un projet d'étudiant à l'universite de Tsukuba au Japon :
''')

st.markdown('''
    <div style="border: 1px solid grey; padding: 10px; border-radius: 5px;">      
    <p>
        <b>SoccerTrack:</b><br>
        A Dataset and Tracking Algorithm for Soccer with Fish-eye and Drone Videos
    </p>
    <p>
        Atom Scott*, Ikuma Uchida*, Masaki Onishi, Yoshinari Kameda, Kazuhiro Fukui, Keisuke Fujii
    </p>
    <p>
        <i> Presented at CVPR Workshop on Computer Vision for Sports (CVSports'22). *Authors contributed equally. </i>
    </p>
    <div>
        <a rel="noreferrer nofollow" href="https://openaccess.thecvf.com/content/CVPR2022W/CVSports/papers/Scott_SoccerTrack_A_Dataset_and_Tracking_Algorithm_for_Soccer_With_Fish-Eye_CVPRW_2022_paper.pdf">
        <img src="https://img.shields.io/badge/Paper-PDF-red?style=for-the-badge&amp;logo=adobe-acrobat-reader">
        </a>
        <a rel="noreferrer nofollow" href="https://github.com/AtomScott/SoccerTrack">
        <img src="https://img.shields.io/badge/Code-Page-blue?style=for-the-badge&amp;logo=github">
        </a>
        <a rel="noreferrer nofollow" href="https://soccertrack.readthedocs.io/">
        <img src="https://img.shields.io/badge/Documentation-Page-blue?style=for-the-badge&amp;logo=read-the-docs">
        </a>
    </div>
    
    <p style="margin-top:20px; font-style: italic; color: grey;">
    All data in SoccerTrack was obtained from 11-vs-11 soccer games between college-aged athletes. 
    Measurements were conducted after we received the approval of Tsukuba university’s ethics committee, 
    and all participants provided signed informed permission. After recording several soccer matches, 
    the videos were semi-automatically annotated based on the GNSS coordinates of each player.
    </p>
''', unsafe_allow_html=True)
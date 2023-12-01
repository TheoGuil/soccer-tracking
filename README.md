# Soccer Tracker Stats

https://soccer-tracker-stats-de9791626434.herokuapp.com/

## Introduction

Ce projet a pour but de récupérer des statistiques sur un match de football à partir de la retransmission de celui-ci.

A partir de la position des joueurs et du ballon, nous allons calculer des statistiques sur le match.
        
A ce stade, nous nous sommes concentrés sur les passes.

## Dataset preparation

Download the dataset from https://www.kaggle.com/datasets/atomscott/soccertrack

And put the unzip to the root of the folder


## Open dahsboard in dev env

Open Docker container and run the following commands :

``` shell
cd dashboard/
```
puis 
``` shell
streamlit run --server.port 80 ./🏠_home.py
```


## External sources
Datas from : https://www.kaggle.com/datasets/atomscott/soccertrack

Useful library : https://sportslabkit.readthedocs.io/

<hr>

## Dataset Details

<table>
    <thead>
        <tr>
            <th>****</th>
            <th><strong>Wide-View Camera</strong></th>
            <th><strong>Top-View Camera</strong></th>
            <th><strong>GNSS</strong></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Device</td>
            <td>Z CAM E2-F8</td>
            <td>DJI Mavic 3</td>
            <td>STATSPORTS APEX 10 Hz</td>
        </tr>
        <tr>
            <td>Resolution</td>
            <td>8K (7,680 × 4,320 pixel)</td>
            <td>4K (3,840 × 2,160 pixesl)</td>
            <td>Abs. err. in 20-m run: 0.22 ± 0.20 m</td>
        </tr>
        <tr>
            <td>FPS</td>
            <td>30</td>
            <td>30</td>
            <td>10</td>
        </tr>
        <tr>
            <td>Player tracking</td>
            <td>✅</td>
            <td>✅</td>
            <td>✅</td>
        </tr>
        <tr>
            <td>Ball tracking</td>
            <td>✅</td>
            <td>✅</td>
            <td>-</td>
        </tr>
        <tr>
            <td>Bounding box</td>
            <td>✅</td>
            <td>✅</td>
            <td>-</td>
        </tr>
        <tr>
            <td>Location data</td>
            <td>✅</td>
            <td>✅</td>
            <td>✅</td>
        </tr>
        <tr>
            <td>Player ID</td>
            <td>✅</td>
            <td>✅</td>
            <td>✅</td>
        </tr>
    </tbody>
</table>
All data in SoccerTrack was obtained from 11-vs-11 soccer games between college-aged athletes. Measurements were conducted after we received the approval of Tsukuba university’s ethics committee, and all participants provided signed informed permission. After recording several soccer matches, the videos were semi-automatically annotated based on the GNSS coordinates of each player.

<br/>

<table>
    <tbody>
        <tr>
        <td>
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
        </td>
        </tr>
    </tbody>
</table>

  

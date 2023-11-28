import json
import pandas as pd
import os
import argparse
from math import *
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--label', type=str, required=True)
parser.add_argument('--annotations_dir', type=str, required=True)
args = parser.parse_args()


def get_possession(df_ball, df_team0, df_team1):
    list_index0 = [i for i in range(0, len(df_team0), 5)]
    list_index1 = [i for i in range(0, len(df_team1), 5)]
    possession_team = []
    possession_player = []

    for index, row in df_ball.iterrows():
        distance0 = list(map(lambda v: calcul_distance(df_ball.loc[index, "bb_left"],
                                                       df_ball.loc[index, "bb_top"], df_team0.iloc[index, v],
                                                       df_team0.iloc[index, v + 1],25), list_index0))
        distance1 = list(map(lambda v: calcul_distance(df_ball.loc[index, "bb_left"],
                                                       df_ball.loc[index, "bb_top"], df_team1.iloc[index, v],
                                                       df_team1.iloc[index, v + 1],25), list_index1))
        argmin0 = np.argmin(np.array(distance0))
        argmin1 = np.argmin(np.array(distance1))
        min_team = np.array([distance0[argmin0], distance1[argmin1]])
        id_team_possession = np.argmin(min_team)
        if float(row["speed_25"]) < 9:
            possession_team.append(id_team_possession)
            possession_player.append(min_team[id_team_possession])
        else:
            possession_team.append("passe or shot")
            possession_player.append("passe or shot")

    df_ball[" possession_team"] = possession_team
    df_ball[" possession_player"] = possession_player
    return df_ball

def calcul_distance(x1, y1, x2, y2, p_m):
    distance = ((float(x2) - float(x1)) / p_m) ** 2 + ((float(y2) - float(y1)) / p_m) ** 2
    return sqrt(distance)


def calcul_ball_speed(df, pixel_to_meter):
    df_return = df.iloc[30:, :].copy()
    speed_25, speed_50, speed_75, speed_1 = [], [], [], []
    for index, row in df_return.iterrows():
        speed_25.append(
            calcul_distance(df.loc[index, "bb_left"], df.loc[index, "bb_top"], df.loc[index - 7, "bb_left"],
                            df.loc[index - 7, "bb_top"], int(25)) / 0.25)
        speed_50.append(
            calcul_distance(df.loc[index, "bb_left"], df.loc[index, "bb_top"], df.loc[index - 15, "bb_left"],
                            df.loc[index - 15, "bb_top"], int(25)) / 0.5)
        speed_75.append(
            calcul_distance(df.loc[index, "bb_left"], df.loc[index, "bb_top"], df.loc[index - 22, "bb_left"],
                            df.loc[index - 22, "bb_top"], int(25)) / 0.75)
        speed_1.append(
            calcul_distance(df.loc[index, "bb_left"], df.loc[index, "bb_top"], df.loc[index - 30, "bb_left"],
                            df.loc[index - 30, "bb_top"], int(25)))
    df_return["speed_25"] = speed_25
    df_return["speed_50"] = speed_50
    df_return["speed_75"] = speed_75
    df_return["speed_1"] = speed_1
    return df_return


def calcul_player_speed(df, pixel_to_meter):
    df_return = df.iloc[150:, :].copy()
    speed_0_5, speed_1, speed_2, speed_3, speed_4, speed_5 = [], [], [], [], [], []
    for index, row in df_return.iterrows():
        speed_0_5.append(
            calcul_distance(df.loc[index, "bb_left"], df.loc[index, "bb_top"], df.loc[index - 15, "bb_left"],
                            df.loc[index - 15, "bb_top"], int(25)) / 0.5)
        speed_1.append(
            calcul_distance(df.loc[index, "bb_left"], df.loc[index, "bb_top"], df.loc[index - 30, "bb_left"],
                            df.loc[index - 30, "bb_top"], int(25)))
        speed_2.append(
            calcul_distance(df.loc[index, "bb_left"], df.loc[index, "bb_top"], df.loc[index - 60, "bb_left"],
                            df.loc[index - 60, "bb_top"], int(25)) / 2)
        speed_3.append(
            calcul_distance(df.loc[index, "bb_left"], df.loc[index, "bb_top"], df.loc[index - 90, "bb_left"],
                            df.loc[index - 90, "bb_top"], int(25)) / 3)
        speed_4.append(
            calcul_distance(df.loc[index, "bb_left"], df.loc[index, "bb_top"], df.loc[index - 120, "bb_left"],
                            df.loc[index - 120, "bb_top"], int(25)) / 4)
        speed_5.append(
            calcul_distance(df.loc[index, "bb_left"], df.loc[index, "bb_top"], df.loc[index - 150, "bb_left"],
                            df.loc[index - 150, "bb_top"], int(25)) / 5)
    df_return["speed_0_5"] = speed_0_5
    df_return["speed_1"] = speed_1
    df_return["speed_2"] = speed_2
    df_return["speed_3"] = speed_3
    df_return["speed_4"] = speed_4
    df_return["speed_5"] = speed_5
    return df_return


def create_ball_KPI(df_ball, df_team0, df_team1):
    df_ball = calcul_ball_speed(df_ball, 25)
    get_possession(df_ball, df_team0, df_team1)
    return df_ball


def create_player_KPI(df_team, team_dict):
    #  return a dict containing all player in the field and their positions at each frame
    players_df_list = []
    for i in range(0, len(df_team.columns), 5):
        id_player = set(list(df_team.iloc[1, i:i + 5]))
        if len(id_player) > 1:
            print("error")
            break
        pl = df_team.iloc[4:, i:i + 5]
        pl.columns = ["bb_left", "bb_top", "bb_width", "bb_height", "conf"]
        df_pl = calcul_player_speed(pl, 25)
        players_df_list.append(df_pl)
    return players_df_list


def detect_team(df):
    # separate player of same team
    team_index = df.iloc[0, :]
    end_team1 = min(team_index[team_index == '1'].index)
    end_team2 = min(team_index[team_index == '3'].index)
    teams0 = df.iloc[:, 1:end_team1]
    teams1 = df.iloc[:, end_team1:end_team2]
    ball = df.iloc[4:, end_team2:]
    return teams0, teams1, ball


label_folder = args.label
annotations_dir = args.annotations_dir
list_label = os.listdir(label_folder)
start = 1
end = 5

init = 0

for lab in list_label:
    dict_team0 = []
    dict_team1 = []
    # get the folder where labels are contained
    label = pd.read_csv(os.path.join(label_folder, lab), header=None)
    team0, team1, ball = detect_team(label)
    # create a dictionnary for both of the team and the ball
    list_team0 = create_player_KPI(team0, dict_team0)
    list_team1 = create_player_KPI(team1, dict_team1)
    ball.columns = ["bb_left", "bb_top", "bb_width", "bb_height", "conf"]
    ball_df = create_ball_KPI(ball, team0, team1)
    # save df in csv
    path_annotations = os.path.join(annotations_dir, lab[:-4])
    ball_df.to_csv()
    count = 0
    if not os.path.isdir(path_annotations):
        os.makedirs(path_annotations)
    ball_df.to_csv(os.path.join(path_annotations, "ball.csv"))
    for df0, df1 in zip(list_team0, list_team1):
        if not os.path.isdir(os.path.join(path_annotations, "team0")):
            os.makedirs(os.path.join(path_annotations, "team0"))
        if not os.path.isdir(os.path.join(path_annotations, "team1")):
            os.makedirs(os.path.join(path_annotations, "team1"))
        df0.to_csv(os.path.join(path_annotations, "team0", "player_" + str(count) + ".csv"))
        df0.to_csv(os.path.join(path_annotations, "team1", "player_" + str(count) + ".csv"))
        count += 1

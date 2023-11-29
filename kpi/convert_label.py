# import json
import pandas as pd
import time
import os
import argparse
from kpi.tracker import Game

# from math import *

parser = argparse.ArgumentParser()
parser.add_argument('--all_player', type=str, required=True)
parser.add_argument('--output_dir', type=str, required=True)
args = parser.parse_args()

"""def create_ball(df):
    # return a dict containing as key the frame and as value the ball's positions
    df = df.T.reset_index(drop=True).T
    positions = []
    for index, row in df.iterrows():
        frame_id = "frame_" + str(index) + ".jpg"
        if not pd.isnull(row[0]):
            # positions.append({frame_id: {"x": float(row[0]) + float(row[2]) / 2, "y": float(row[1]) + float(row[3]) / 2,
            #                             "w": float(row[2]),
            #                             "h": float(row[3])}})
            positions.append([int(float(row[0])), int(float(row[1])), int(float(row[2])), int(float(row[3]))])

        else:
            positions.append(None)

    return positions


def create_player(df, id, start, end):
    #  return a dict containing as key the frame and as value the player's positions
    df = df.T.reset_index(drop=True).T
    positions = []
    for index, row in df.iterrows():
        frame_id = "frame_" + str(index) + ".jpg"
        if not pd.isnull(row[0]):
            # positions.append({frame_id: {"x": float(row[0]) + float(row[2]) / 2, "y": float(row[1]) + float(row[3]) / 2,
            #                             "w": float(row[2]),
            #                             "h": float(row[3])}})
            positions.append([int(float(row[0])), int(float(row[1])), int(float(row[2])), int(float(row[3]))])

        else:
            positions.append(None)
            print("players {} out at frame {} columns {}:{}".format(id, frame_id, start, end))
    player = {"id": int(id), "positions": positions}
    return player


def create_team(df_team):
    #  return a dict containing all player in the field and their positions at each frame
    team_dict = []
    for i in range(0, len(df_team.columns), 4):
        id_player = list(set(list(df_team.iloc[1, i:i + 4])))
        if len(id_player) > 1:
            print("error")
            break
        else:
            id_player = int(id_player[0])
        pl = df_team.iloc[4:, i:i + 4]
        team_dict.append(create_player(pl, id_player, i, i + 5))
    return team_dict


def detect_team(df):
    # separate player of same team
    team_index = df.iloc[0, :]
    end_team1 = min(team_index[team_index == '1'].index)
    end_team2 = min(team_index[team_index == 'BALL'].index)
    teams0 = df.iloc[:, 1:end_team1]
    teams1 = df.iloc[:, end_team1:end_team2]
    ball = df.iloc[4:, end_team2:]
    return teams0, teams1, ball"""

if __name__ == "__main__":
    csv_path = args.all_player
    annotations_dir = args.output_dir

    final_dict_team0 = []
    final_dict_team1 = []
    final_dict_ball = []
    game = Game()

    #start = time.time()

    label = pd.read_csv(os.path.join(csv_path), header=None)
    team0, team1, ball = game.detect_team(label)
    # create a dictionnary for both of the team and the ball
    game.create_team(team0, team1)
    game.create_ball(ball)
    # save dict in josn file
    for player in game.team0["players"]:
        player.add_speed_acc()
    for player in game.team1["players"]:
        player.add_speed_acc()
    game.ball.add_speed_acc()
    game.ball.get_possession(game.team0['players'], game.team1['players'])
    print('ok')

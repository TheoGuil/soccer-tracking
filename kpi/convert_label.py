# import json
import json

import pandas as pd
import time
import os
import argparse
from kpi.tracker import Game, Passe

# from math import *

parser = argparse.ArgumentParser()
parser.add_argument('--all_player_bbox', type=str, required=True)
parser.add_argument('--all_player_2D', type=str, required=True)
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
    csv_path_bbox = args.all_player_bbox
    csv_path_2D = args.all_player_2D
    annotations_dir = args.output_dir

    final_dict_team0 = []
    final_dict_team1 = []
    final_dict_ball = []
    game = Game()

    # start = time.time()

    label_bbox = pd.read_csv(os.path.join(csv_path_bbox), header=None)
    label_2D = pd.read_csv(os.path.join(csv_path_2D), header=None)
    df_passe = pd.read_csv("passe_predicted.csv", header=0)
    team0_bbox, team1_bbox, ball_bbox = game.detect_team(label_bbox)
    team0_2D, team1_2D, ball_2D = game.detect_team(label_2D)
    # create a dictionnary for both of the team and the ball
    game.create_team(team0_bbox, team1_bbox, team0_2D, team1_2D)
    game.create_ball(ball_bbox, ball_2D)
    # save dict in josn file
    for player in game.team0["players"]:
        player.add_speed_acc()
    for player in game.team1["players"]:
        player.add_speed_acc()
    game.ball.add_speed_acc()
    game.ball.calculate_angles()
    game.ball.get_possession(game.team0['players'], game.team1['players'])
    game.ball.get_passe_from_model(df_passe)
    game.actions.extend(Passe(passe[2], passe[3], index, 'passe', passe[0], passe[1], passe[4], passe[5]) for index, passe in
                        enumerate(game.ball.passe))
    for passe in game.actions:
        passe.get_succeed()
    actions_dict = game.transform_actions_to_dict()
    #[ action.get_player_eliminated(game.team0['player'], game.team1['player']) for action in game.actions]
    with open("passes.json", "w") as outfile:
        json.dump(actions_dict, outfile)
    # game.ball.calculate_angles()
    # game.ball.draw_passe()
    for player in game.team0['players']:
        player.get_stats_player(game.ball, game.actions)
    for player in game.team1['players']:
        player.get_stats_player(game.ball, game.actions)
    game.get_stats_per_team()
    player_stats = game.write_player_stats_json()
    team_stats = game.write_team_stats_json()
    print('ok')
    with open("stats_player.json", "w") as outfile:
        json.dump(player_stats, outfile)
    with open("stats_team.json", "w") as outfile:
        json.dump(team_stats, outfile)


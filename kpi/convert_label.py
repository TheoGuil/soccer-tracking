# import json
import json

import pandas as pd
import time
import os
import argparse
from kpi.tracker import Game, Passe, Centre, Tir

# from math import *

parser = argparse.ArgumentParser()
parser.add_argument('--all_player_bbox', type=str, required=True)
parser.add_argument('--all_player_2D', type=str, required=True)
parser.add_argument('--output_dir', type=str, required=True)
args = parser.parse_args()

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
    game.ball.get_possession(game.team0['players'], game.team1['players'], game.id_to_index_team0,
                             game.id_to_index_team1)
    game.ball.get_passe_tir_centre_from_model(df_passe)

    game.actions.extend(
        Passe(passe[2], passe[3], index+game.nb_action, 'passe', passe[0], passe[1], passe[4], passe[5]) for index, passe in
        enumerate(game.ball.passe))
    game.nb_action = len(game.actions)
    game.actions.extend(
        Centre(passe[2], passe[3], index+game.nb_action, 'centre', passe[0], passe[1], passe[4], passe[5]) for index, passe in
        enumerate(game.ball.centre))
    game.nb_action = len(game.actions)
    game.actions.extend(
        Tir(passe[2], passe[3], index+game.nb_action, 'tir', passe[0], passe[4]) for index, passe in
        enumerate(game.ball.tir))
    game.nb_action = len(game.actions)

    for action in game.actions:
        if action.type == 'passe':
            action.get_stats_passe(game.ball, game.team0['players'], game.team1['players'])
    actions_dict = game.transform_actions_to_dict()
    # [ action.get_player_eliminated(game.team0['player'], game.team1['player']) for action in game.actions]
    with open("dashboard/src/stats/passes.json", "w") as outfile:
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
    with open("dashboard/src/stats/stats_player.json", "w") as outfile:
        json.dump(player_stats, outfile)
    with open("dashboard/src/stats/stats_team.json", "w") as outfile:
        json.dump(team_stats, outfile)

import pandas as pd
import json
import numpy as np
import math


class Moving_object:
    def calcul_distance(self, point_a, point_b):
        x1, y1 = point_a
        x2, y2 = point_b
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance

    def get_center(self, pos):
        return pos[1], pos[2] + pos[3]

    def add_speed_acc(self):
        distance_list = [
            self.calcul_distance((self.get_center(self.positions[i])),
                                 (self.get_center(self.positions[i - 1]))) if None not in self.positions[
                i] or None not in
                                                                              self.position[i - 1] else None for i
            in range(1, len(self.positions))]
        acc_list = [
            distance_list[i] - distance_list[i - 1] if distance_list[i] is not None or distance_list[i - 1] is not None else None
            for i in range(1, len(distance_list))]
        self.speed = [0] + distance_list
        self.acceleration = [0, 0] + acc_list


class Game:
    def __init__(self):
        self.team0 = []
        self.team1 = []
        self.ball = None

    def create_ball(self, df, init):
        if init:
            self.ball = Ball()
        self.ball.positions = self.ball.positions + self.ball.append_ball_pos(df)

    def create_team(self, df_team0, df_team1, init=None):
        #  return a dict containing all player in the field and their positions at each frame
        team_dict = []
        for i in range(0, len(df_team0.columns), 4):
            id_player0 = list(set(list(df_team0.iloc[1, i:i + 4])))
            id_player1 = list(set(list(df_team1.iloc[1, i:i + 4])))
            if len(id_player0) > 1 or len(id_player1) > 1:
                print("error")
                break
            else:
                id_player0 = int(id_player0[0])
                id_player1 = int(id_player1[0])
            pl_team0 = df_team0.iloc[4:, i:i + 4]
            pl_team1 = df_team0.iloc[4:, i:i + 4]
            if init:
                self.team0.append(Player(id_player0, pl_team0))
                self.team1.append(Player(id_player1, pl_team1))
                self.id_to_index_team0 = {obj.id_player: index for index, obj in enumerate(self.team0)}
                self.id_to_index_team1 = {obj.id_player: index for index, obj in enumerate(self.team1)}

            self.team0[self.id_to_index_team0[id_player0]].positions = self.team0[self.id_to_index_team0[
                id_player0]].positions + self.team0[self.id_to_index_team0[id_player0]].add_position_player(pl_team0,
                                                                                                            id_player0,
                                                                                                            i, i + 4, 0)
            self.team1[self.id_to_index_team1[id_player1]].positions = self.team1[self.id_to_index_team1[
                id_player1]].positions + self.team0[self.id_to_index_team0[id_player0]].add_position_player(pl_team1,
                                                                                                            id_player1,
                                                                                                            i, i + 4, 0)

    def detect_team(self, df):
        # separate player of same team
        team_index = df.iloc[0, :]
        end_team1 = min(team_index[team_index == '1'].index)
        end_team2 = min(team_index[team_index == 'BALL'].index)
        teams0 = df.iloc[:, 1:end_team1]
        teams1 = df.iloc[:, end_team1:end_team2]
        ball = df.iloc[4:, end_team2:]
        return teams0, teams1, ball


class Player(Moving_object):
    positions = []
    speed = []
    acceleration = []

    def __init__(self, id_player, team):
        self.id_player = id_player

        self.teams = team

    def add_position_player(self, df, id, start, end, team):
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

        return positions


class Ball(Moving_object):
    positions = []
    speed = []
    team_possesion = []
    state = []
    acceleration = []

    def append_ball_pos(self, df):
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

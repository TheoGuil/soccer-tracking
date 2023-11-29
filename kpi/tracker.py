import pandas as pd
import json
import numpy as np
import math


class Moving_object:
    positions = []
    speed = []
    acceleration = []

    def calculate_distances(self, points_a, points_b):
        # Convert the lists of coordinates to NumPy arrays
        points_a = np.array(points_a, dtype=float)
        points_b = np.array(points_b, dtype=float)

        # Replace None values with np.nan
        points_a[np.equal(points_a, None)] = np.nan
        points_b[np.equal(points_b, None)] = np.nan

        # Extract x and y coordinates
        x1, y1 = points_a[:, 0], points_a[:, 1]
        x2, y2 = points_b[:, 0], points_b[:, 1]

        # Use vectorized distance calculation
        distances = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distances

    # def get_center_list(self):
    #    self.center = [self.get_center(pos) if None not in pos else None for pos in self.positions]

    def get_centers(self):
        # Convert the list of positions to a NumPy array
        positions = np.array(self.positions, dtype=float)
        positions[np.equal(positions, None)] = np.nan

        # Calculate the center coordinates for each position
        centers_x = positions[:, 1] + positions[:, 3] / 2
        centers_y = positions[:, 2] + positions[:, 0] / 2

        # Initialize the result list with Nones

        # Replace non-None positions with calculated centers
        centers = np.column_stack((centers_x, centers_y))

        self.center = centers

    # def get_center(self, pos):
    #    return (pos[1] + (pos[3] / 2), pos[2] + (pos[0] / 2))

    def add_speed_acc(self):
        self.get_centers()

        distance_list = self.calculate_distances(self.center[1:], self.center[:-1])
        # distance_list = [self.calculate_distance(self.center[1:], self.center[:-1])
        #                 if self.center[i] is not None and self.center[i - 1] is not None
        #                 else None for i in range(1, len(self.center))]

        acc_list = [distance_list[i] - distance_list[i - 1] if distance_list[i] is not None
                    and distance_list[i - 1] is not None else None for i in range(1, len(distance_list))]

        self.speed = [0] + distance_list
        self.acceleration = [0, 0] + acc_list

    def add_position(self, df):
        #  return a dict containing as key the frame and as value the player's positions
        df = df.T.reset_index(drop=True).T
        df = df.astype(float)
        positions = df.values
        positions = [pos if None not in pos else None for pos in positions]
        self.positions = self.positions + positions


class Game:
    def __init__(self):
        self.team0 = {"players": [], "stats": {}}
        self.team1 = {"players": [], "stats": {}}
        self.ball = None
        self.nb_players = 0

    def create_ball(self, df):

        self.ball = Ball()
        self.ball.add_position(df)

    def create_team(self, df_team0, df_team1):
        #  return a dict containing all player in the field and their positions at each frame
        team_dict = []
        for i in range(0, len(df_team0.columns), 4):

            id_player0 = self.nb_players
            id_player1 = self.nb_players + 1
            if len(list(set(list(df_team0.iloc[1, i:i + 4])))) > 1 or len(
                    list(set(list(df_team1.iloc[1, i:i + 4])))) > 1:
                print("error")
                break
            pl_team0 = df_team0.iloc[4:, i:i + 4]
            pl_team1 = df_team0.iloc[4:, i:i + 4]

            self.team0["players"].append(Player(id_player0, pl_team0))
            self.team1["players"].append(Player(id_player1, pl_team1))
            self.id_to_index_team0 = {obj.id_player: index for index, obj in enumerate(self.team0["players"])}
            self.id_to_index_team1 = {obj.id_player: index for index, obj in enumerate(self.team1["players"])}

            self.team0["players"][self.id_to_index_team0[id_player0]].add_position(pl_team0)
            self.team1["players"][self.id_to_index_team1[id_player1]].add_position(pl_team1)
            self.nb_players += 2

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

    def __init__(self, id_player, team):
        self.id_player = id_player

        self.teams = team

    """def add_position_player(self, df, id, start, end, team):
        #  return a dict containing as key the frame and as value the player's positions
        df = df.T.reset_index(drop=True).T
        df = df.astype(float).astype(int)
        positions = df.values
        positions = [ pos if None not in pos else None for pos in positions ]

        return positions"""


class Ball(Moving_object):
    team_possesion = []
    state = []

    """def append_ball_pos(self, df):
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

        return positions"""

    def get_possession(self, team0, team1):
        all_players = team0 + team1
        distance_player_ball = [self.calculate_distances(self.center, player.center) for player in all_players]

    def detect_passes(self):
        print("ok")
class Actions:

    def __init__(self, start, end, id, team_id, player_id, type):
        self.start = start
        self.end = end
        self.id = id
        self.team = team_id
        self.player = player_id
        self.type = type


class Passe(Actions):

    def get_distance_passe(self):
        print('todo')

    def get_receveur_passeur(self):
        print('todo')

    def get_speed(self):
        print('todo')

    def get_player_eliminated(self):
        print('todo')

    def succeed(self):
        print('todo')

    def get_(self):
        print('todo')

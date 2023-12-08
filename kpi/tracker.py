import pandas as pd
import json
import numpy as np
import math
from itertools import groupby


class Game:
    """Class Game that reprsents a football game, the class will contains:
    - A list for each team , the lists will contain instances of class Player().
    - Attribute ball: instance od class Ball()
    - Attribute actions: will contain a list of actions instances such as Passe(), Shot() Cross() ect..."""

    def __init__(self):
        self.team0 = {"players": [], "stats": {}}
        self.team1 = {"players": [], "stats": {}}
        self.ball = None
        self.nb_players = 0
        self.actions = []
        self.nb_action = 0

    def transform_to_dict(self):
        """
        Return as a dict all info calculated about the game.
        :return: Dictionnary of the game attribute.
        """
        return {"team0": {'players': [player.__dict__ for player in self.team0['players']]},
                "team1": {'players': [player.__dict__ for player in self.team1['players']]},
                "ball": self.ball.__dict__,
                "actions": [act.__dict__ for act in self.actions]}

    def transform_actions_to_dict(self):
        """
        Return the info about all actions during the game.
        :return: A dict of all actions
        """
        return {"actions": [act.__dict__ for act in self.actions]}

    def write_player_stats_json(self):
        stats_player_dict = {}
        for player in self.team0['players'] + self.team1['players']:
            stats_player_dict[player.id_player] = player.stats
        return stats_player_dict

    def write_team_stats_json(self):
        return {'team0': self.team0['stats'], "team1": self.team1['stats']}

    def create_ball(self, df_box, df_2D):
        """
        Create Class Ball and add BBOX and 2D position center.
        :param df_box: Dataframe of bbox position
        :param df_2D: Dataframe of 2D center position
        """

        self.ball = Ball()
        self.ball.add_position(df_box)
        self.ball.add_center_2D(df_2D)

    def create_team(self, df_team0_box, df_team1_box, df_team0_2D, df_team1_2D):
        """
        Create a list of Instances player for both team. And add position bbox and 2D.
        :param df_team0_box: Dataframe of bbox position for team0.
        :param df_team1_box: Dataframe of bbox position for team1.
        :param df_team0_2D: Dataframe of 2D position for team0.
        :param df_team1_2D: Dataframe of 2D position for team1.
        """
        team_dict = []
        for i in range(0, len(df_team0_box.columns), 4):
            j = int(i / 2)
            id_player0 = self.nb_players
            id_player1 = self.nb_players + 1
            if len(list(set(list(df_team0_box.iloc[1, i:i + 4])))) > 1 or len(
                    list(set(list(df_team1_box.iloc[1, i:i + 4])))) > 1:
                print("error")
                break
            pl_team0_box = df_team0_box.iloc[4:, i:i + 4]
            pl_team1_box = df_team0_box.iloc[4:, i:i + 4]
            pl_team0_2D = df_team0_2D.iloc[4:, j:j + 2]
            pl_team1_2D = df_team1_2D.iloc[4:, j:j + 2]

            self.team0["players"].append(Player(id_player0, 0))
            self.team1["players"].append(Player(id_player1, 1))
            self.id_to_index_team0 = {obj.id_player: index for index, obj in enumerate(self.team0["players"])}
            self.id_to_index_team1 = {obj.id_player: index for index, obj in enumerate(self.team1["players"])}

            self.team0["players"][self.id_to_index_team0[id_player0]].add_position(pl_team0_box)
            self.team1["players"][self.id_to_index_team1[id_player1]].add_position(pl_team1_box)
            self.team0["players"][self.id_to_index_team0[id_player0]].add_center_2D(pl_team0_2D)
            self.team1["players"][self.id_to_index_team1[id_player1]].add_center_2D(pl_team1_2D)
            self.nb_players += 2

    def detect_team(self, df):
        """
        Separate original dataframe that contains all position of all player into 3 Dataframe one for the ball 2 for each team.
        :param df: Dataframe  positions of ball and all players.
        :return: 3 Dataframe
        """
        team_index = df.iloc[0, :]
        end_team1 = min(team_index[team_index == '1'].index)
        end_team2 = min(team_index[team_index == 'BALL'].index)
        teams0 = df.iloc[:, 1:end_team1]
        teams1 = df.iloc[:, end_team1:end_team2]
        ball = df.iloc[4:, end_team2:]
        return teams0, teams1, ball

    def get_stats_per_team(self):
        """
        Get statistics about teams.
        """
        count_passe_team0, count_passe_team1, count_passe_succes_team0, count_passe_succes_team1, pourcentage_0, pourcentage_1 = self.count_passe()
        pourcentage_possession_team0, pourcentage_possession_team1 = self.count_possession()
        count_tir_team0, count_tir_team1 = self.count_tir()
        count_centre_team0, count_centre_team1 = self.count_centre()

        self.team0['stats'] = {'total_passe': count_passe_team0, 'pourcentage_passe_reussis': pourcentage_0,
                               'possession': pourcentage_possession_team0, "total_tir": int(count_tir_team0),
                               "total_centre": int(count_centre_team0)}
        self.team1['stats'] = {'total_passe': count_passe_team1, 'pourcentage_passe_reussis': pourcentage_1,
                               'possession': pourcentage_possession_team1, "total_tir": int(count_tir_team1),
                               "total_centre": int(count_centre_team0)}

    def count_centre(self):
        actions_centre = [act for act in self.actions if act.type == 'centre']
        count_centre_team0 = len([centre for centre in actions_centre if centre.team_passeur == 0])
        count_centre_team1 = len([centre for centre in actions_centre if centre.team_passeur == 1])
        return count_centre_team0, count_centre_team1

    def count_tir(self):
        actions_tir = [act for act in self.actions if act.type == 'tir']
        count_tir_team0 = len([tir for tir in actions_tir if tir.team == 0])
        count_tir_team1 = len([tir for tir in actions_tir if tir.team == 1])
        return count_tir_team0, count_tir_team1

    def count_passe(self):
        """
        Count passes for each team.
        :return:
        """

        actions_passe = [act for act in self.actions if act.type == 'passe']
        count_passe_team0 = len([passe for passe in actions_passe if passe.team_passeur == 0])
        count_passe_team1 = len([passe for passe in actions_passe if passe.team_passeur == 1])
        count_passe_succes_team0 = len([passe for passe in actions_passe if passe.team_passeur == 0 and passe.succeed])
        count_passe_succes_team1 = len([passe for passe in actions_passe if passe.team_passeur == 1 and passe.succeed])
        pourcentage_0 = count_passe_succes_team0 / count_passe_team0 * 100
        pourcentage_1 = count_passe_succes_team1 / count_passe_team1 * 100
        return count_passe_team0, count_passe_team1, count_passe_succes_team0, count_passe_succes_team1, pourcentage_0, pourcentage_1

    def count_possession(self):
        """
        Count possession for each team.
        :return:
        """

        actions_passe = [act for act in self.actions if act.type == 'passe']
        count_possession_team0 = len([team for team in self.ball.team_possession if team == 0])
        count_possession_team1 = len([team for team in self.ball.team_possession if team == 1])
        len_passe_team0 = np.sum([passe.end - passe.start for passe in actions_passe if passe.team_passeur == 0])
        len_passe_team1 = np.sum([passe.end - passe.start for passe in actions_passe if passe.team_passeur == 1])

        total_possession_team0 = (count_possession_team0 + len_passe_team0) / len(self.ball.team_possession) * 100
        total_possession_team1 = (count_possession_team1 + len_passe_team1) / len(self.ball.team_possession) * 100
        return total_possession_team0, total_possession_team1


class Moving_object:
    positions = []
    center_2D = []
    speed = []
    acceleration = []

    def calculate_distances(self, points_a, points_b):
        """
        Calculate distance between points from list points_a and list of points_b.
        :param points_a: List of points A
        :param points_b: List of points B
        :return:
        """
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
        """
        Convert bbox position into 2d center position.
        :return:
        """
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
        """
        Add speed and acceleration.
        """
        self.get_centers()

        distance_list = self.calculate_distances(self.center_2D[1:], self.center_2D[:-1])
        # distance_list = [self.calculate_distance(self.center[1:], self.center[:-1])
        #                 if self.center[i] is not None and self.center[i - 1] is not None
        #                 else None for i in range(1, len(self.center))]

        acc_list = [distance_list[i] - distance_list[i - 1] if distance_list[i] is not None
                                                               and distance_list[i - 1] is not None else None for i in
                    range(1, len(distance_list))]

        self.speed = [0] + distance_list
        self.acceleration = [0] + acc_list + [0]

    def add_position(self, df):
        """
        Add bbox position.
        :param df: Dataframe of positions.
        :return:
        """
        #  return a dict containing as key the frame and as value the player's positions
        df = df.T.reset_index(drop=True).T
        df = df.astype(float)
        positions = df.values
        positions = [pos if None not in pos else None for pos in positions]
        self.positions = self.positions + positions

    def add_center_2D(self, df):
        """
        Add position center 2D.
        :param df: Dataframe of positions.
        :return:
        """
        df = df.T.reset_index(drop=True).T
        df = df.astype(float)
        positions = df.values
        positions = [pos if None not in pos else None for pos in positions]
        self.center_2D = self.center_2D + positions


class Player(Moving_object):

    def __init__(self, id_player, team):
        self.id_player = id_player
        self.id_team = team
        self.stats = {}

    def get_stats_player(self, ball, actions):
        self.get_max_speed_acc()
        self.get_distance_runned()
        self.get_nb_passes(actions)
        self.get_nb_shot(actions)
        self.get_nb_centre(actions)
        self.get_nb_ball_touched(ball)

    def get_max_speed_acc(self):
        # [ind for ind, sp in enumerate(self.speed) if sp > 3]
        self.stats["max_speed"] = float(max(self.speed))
        self.stats["max_acceleration"] = float(max(self.acceleration))

    def get_distance_runned(self):
        self.stats["distance_run"] = float(np.sum(self.speed))

    def get_nb_passes(self, actions):
        actions_passe = [act for act in actions if act.type == 'passe']
        nb_passe = len([passe for passe in actions_passe if passe.passeur == self.id_player])
        self.stats["nb_passe"] = nb_passe
        self.stats["pourcentage_passe_reussis"] = len(
            [passe for passe in actions_passe if passe.passeur == self.id_player and passe.succeed]) / nb_passe

    def get_nb_shot(self, actions):
        actions_tir = [act for act in actions if act.type == 'tir']
        nb_tir = len([tir for tir in actions_tir if tir.tireur == self.id_player])
        self.stats["nb_tir"] = nb_tir

    def get_nb_centre(self, actions):
        actions_centre = [act for act in actions if act.type == 'centre']
        nb_centre = len([centre for centre in actions_centre if centre.passeur == self.id_player])
        self.stats["nb_centre"] = nb_centre

    def get_nb_ball_touched(self, ball):
        possession_state = ball.state
        df_poss = pd.DataFrame(data=possession_state)
        df_poss[1] = (df_poss[0] != df_poss[0].shift(1)).cumsum()
        self.stats["nb_ballon_touche"] = len(set(df_poss[df_poss[0] == self.id_player][1].values))

    """def add_position_player(self, df, id, start, end, team):
        #  return a dict containing as key the frame and as value the player's positions
        df = df.T.reset_index(drop=True).T
        df = df.astype(float).astype(int)
        positions = df.values
        positions = [ pos if None not in pos else None for pos in positions ]

        return positions"""


class Ball(Moving_object):
    team_possession = []
    state = []

    def get_possession(self, team0, team1, index0, index1):
        """
        Get the closest player from the ball at each frame and his team.
        :param team0: List of player instances team0.
        :param team1: List of player instances team1.
        :return:
        """
        all_players = team0 + team1
        distance_player_ball = [self.calculate_distances(self.center_2D, player.center_2D) for player in all_players]
        distance_player_ball = np.array(distance_player_ball)

        # Use np.argmin(axis=0) to get the indices of the minimum value along each column
        list_argmin = list(np.argmin(distance_player_ball, axis=0))
        self.state = [all_players[argmin].id_player for argmin in list_argmin]
        self.team_possession = [all_players[argmin].id_team for argmin in list_argmin]

    def get_passe_tir_centre_from_model(self, df):
        """
        Get results of passes prediction and create a list passe with
        the id of the passeur, id of the receveur, start , end, team passeur, team receveur.
        Correct the attribute state to replace closest player by None when the ball is in phase passe.
        :param df:
        :return:
        """

        df = self.correct_possession_error(df)
        df = self.correct_passe_error(df)
        df = self.correct_deviation(df)
        df = self.detect_shot_cross(df)

        df['change'] = (df['predicted'] != df['predicted'].shift(1)).cumsum()
        val_passe = df[df['predicted'] == 1]['change'].unique()
        list_intervall_passe = [(df[df['change'] == v].index[0], df[df['change'] == v].index[-1]) for v in val_passe]

        val_centre = df[df['predicted'] == 3]['change'].unique()
        list_intervall_centre = [(df[df['change'] == v].index[0], df[df['change'] == v].index[-1]) for v in val_centre]

        val_tir = df[df['predicted'] == 2]['change'].unique()
        list_intervall_tir = [(df[df['change'] == v].index[0], df[df['change'] == v].index[-1]) for v in val_tir]

        all_passe = [[self.state[intervall[0] - 1], self.state[intervall[1] + 1]] + list(intervall) + [
            self.team_possession[intervall[0] - 1], self.team_possession[intervall[1] + 1]] for intervall in
                     list_intervall_passe[:-1]]
        all_centre = [[self.state[intervall[0] - 1], self.state[intervall[1] + 1]] + list(intervall) + [
            self.team_possession[intervall[0] - 1], self.team_possession[intervall[1] + 1]] for intervall in
                      list_intervall_centre]

        all_tir = [[self.state[intervall[0] - 1], self.state[intervall[0] - 1]] + list(intervall) + [
            self.team_possession[intervall[0] - 1]] for intervall in
                   list_intervall_tir]
        for action in all_passe + all_tir + all_centre:
            self.state[action[2]:action[3]] = [None] * (action[3] - action[2])
            self.team_possession[action[2]:action[3]] = [None] * (action[3] - action[2])

        self.passe = all_passe
        self.centre = all_centre
        self.tir = all_tir

        # Création de masques pour les types

    def correct_deviation(self, df):
        df_dev = df[(df['predicted'] == 1) & (df['angle'].abs() > 50) & (df['speed'] > 0.10)]
        index_dev = df_dev.index
        for dev in index_dev:
            df.loc[dev, 'predicted'] = 0
        return df

    def correct_passe_error(self, df):
        df['change'] = (df['predicted'] != df['predicted'].shift(1)).cumsum()

        val_passe = df[df['predicted'] == 1]['change'].unique()
        list_intervall_passe = [(df[df['change'] == v].index[0], df[df['change'] == v].index[-1]) for v in val_passe]
        for intervall in list_intervall_passe[:-1]:
            if self.state[intervall[0] - 1] == self.state[intervall[1] + 1]:
                if intervall[0] == intervall[1]:
                    df.loc[intervall[0], 'predicted'] = 0
                else:
                    df.loc[intervall[0]:intervall[1], 'predicted'] = 0
        return df

    def correct_possession_error(self, df):
        df['change'] = (df['predicted'] != df['predicted'].shift(1)).cumsum()
        val_possession = df[df['predicted'] == 0]['change'].unique()
        list_intervall_possession = [(df[df['change'] == v].index[0], df[df['change'] == v].index[-1]) for v in
                                     val_possession]
        for inter_poss in list_intervall_possession:
            if inter_poss[0] == inter_poss[1]:
                df.loc[inter_poss, 'predicted'] = 1
        return df

    def detect_shot_cross(self, df):
        df['change'] = (df['predicted'] != df['predicted'].shift(1)).cumsum()

        val_passe = df[df['predicted'] == 1]['change'].unique()
        list_intervall_passe = [(df[df['change'] == v].index[0], df[df['change'] == v].index[-1]) for v in val_passe]
        for inter in list_intervall_passe:
            pos_start = self.center_2D[inter[0]]
            pos_end = self.center_2D[inter[1]]
            # start surface 14, 54, 16.5
            if self.team_possession[inter[0] - 1] == 0:
                if (pos_start[0] < 26 and (pos_start[1] > 44 or pos_start[1] < 24)
                        and pos_end[0] < 16.5 and pos_end[1] > 14 and pos_end[1] < 54):
                    df.loc[inter[0]:inter[1], 'predicted'] = 3
                if pos_end[0] < 5 and pos_start[0] < 26 and pos_end[1] < 44 and pos_end[1] > 24 and not (
                        pos_start[1] > 54 or pos_start[1] < 14):
                    df.loc[inter[0]:inter[1], 'predicted'] = 2

            elif self.team_possession[inter[0] - 1] == 1:
                if (pos_start[0] > 78 and (pos_start[1] > 44 or pos_start[1] < 24)
                        and pos_end[0] > 88.5 and pos_end[1] > 14 and pos_end[1] < 54):
                    df.loc[inter[0]:inter[1], 'predicted'] = 3
                if pos_end[0] > 100 and pos_start[0] > 78 and pos_end[1] < 44 and pos_end[1] > 24 and not (
                        pos_start[1] > 54 or pos_start[1] < 14):
                    df.loc[inter[0]:inter[1], 'predicted'] = 2
        return df

    def detect_passes(self):
        """
        Detect all passes with thresholding.
        :return:
        """
        print("ok")
        index_passe = np.where(np.array(self.acceleration) > 0.10)
        all_passe = []
        for ind in np.array(index_passe)[0]:
            start_passe = ind
            end_passe = ind
            while self.speed[end_passe] > 0.2:
                end_passe = end_passe + 1
                print(self.speed[end_passe])
            all_passe.append([start_passe, end_passe])
        for passe in all_passe:
            self.state[passe[0]:passe[1]] = [None] * (passe[1] - passe[0])
        self.passe = all_passe

    def draw_passe(self):
        """
        Draw all passes on video
        :return:
        """
        import cv2
        cap = cv2.VideoCapture('full_game_2D.mp4')
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        outvid = cv2.VideoWriter('full_game_2D_passe.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
        success, frame = cap.read()
        count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if np.any([start <= count <= end for start, end in self.passe]):
                frame = cv2.putText(frame, 'passe', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (255, 0, 0), 1, cv2.LINE_AA)
            count += 1
            outvid.write(frame)

    def calculate_angles(self):
        """
        Calculate angles of trajectory at each frame.
        :return:
        """
        # Calculate vectors between consecutive points
        positions = np.array(self.center_2D)
        vectors = np.diff(positions, axis=0)

        # Calculate angles between consecutive vectors
        angles_radians = np.arctan2(vectors[:, 1], vectors[:, 0])
        angles_degrees = np.degrees(angles_radians)
        angles_diff = np.diff(angles_degrees)
        angles_degree_180 = (angles_diff + 180) % 360 - 180
        # Calculate differences in angles
        sine_values = np.sin(np.radians(angles_degree_180))

        self.angles = [0] + list(angles_degree_180) + [0]
        self.angles_sinus = [0] + list(sine_values) + [0]


class Actions:

    def __init__(self, start, end, id, type):
        self.start = int(start)
        self.end = int(end)
        self.id = int(id)
        self.type = type

    def calculate_distances(self, points_a, points_b):
        """
        Calculate distance between points from list points_a and list of points_b.
        :param points_a: List of points A
        :param points_b: List of points B
        :return:
        """
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


class Passe(Actions):
    def __init__(self, start, end, id, type, passeur_id, receveur_id, team_passeur, team_receveur):
        # Appel de l'__init__ de la classe parente
        super().__init__(start, end, id, type)

        # Initialisation propre à la classe Passe
        self.passeur = passeur_id
        self.receveur = receveur_id
        self.team_passeur = team_passeur
        self.team_receveur = team_receveur

    def get_stats_passe(self, ball, team0, team1):
        self.get_distance_passe(ball)
        self.get_player_eliminated(team0, team1, ball)
        self.get_in_30_m(ball)
        self.get_in_surface(ball)
        self.get_succeed()

    def get_distance_passe(self, ball):
        distance_passe = self.calculate_distances([ball.center_2D[self.end]], [ball.center_2D[self.start]])[0]
        if distance_passe < 25:
            self.longueur = 'courte'
        elif distance_passe < 50:
            self.longueur = 'moyenne'
        else:
            self.longueur = 'longue'
        self.speed = distance_passe / (self.end - self.start)

    def get_in_surface(self, ball):
        # start surface 14, 54, 16.5
        self.in_surface_reparation = False
        position_ball = ball.center_2D[self.end]
        if self.team_passeur == 0:
            if position_ball[0] < 16.5 and position_ball[1] > 14 and position_ball[1] < 54:
                self.in_surface_reparation = True
        elif self.team_passeur == 1:
            if position_ball[0] > 88.5 and position_ball[1] > 14 and position_ball[1] < 54:
                self.in_surface_reparation = True

    def get_in_30_m(self, ball):
        position_ball = ball.center_2D[self.end]
        self.passe_in_last_30m = False
        if self.team_passeur == 0:
            if position_ball[0] < 26:
                self.passe_in_last_30m = True
        elif self.team_passeur == 1:
            if position_ball[0] > 78:
                self.passe_in_last_30m = True

    def get_player_eliminated(self, team0, team1, ball):
        position_start = ball.center_2D[self.start]
        position_end = ball.center_2D[self.end]
        x_inf = min(position_start[0], position_end[0])
        x_sup = max(position_start[0], position_end[0])
        team_adverse = abs(self.team_passeur - 1)
        if team_adverse == 0:
            self.nb_player_elminated = len(
                [player for player in team0 if
                 player.center_2D[int(self.start + (self.end - self.start) / 2)][0] > x_inf and
                 player.center_2D[int(self.start + (self.end - self.start) / 2)][0] < x_sup])
        elif team_adverse == 1:
            self.nb_player_elminated = len(
                [player for player in team1 if
                 player.center_2D[int(self.start + (self.end - self.start) / 2)][0] > x_inf and
                 player.center_2D[int(self.start + (self.end - self.start) / 2)][0] < x_sup])

    def get_succeed(self):
        if self.team_receveur == self.team_passeur:
            self.succeed = True
        else:
            self.succeed = False


class Centre(Actions):
    def __init__(self, start, end, id, type, passeur_id, receveur_id, team_passeur, team_receveur):
        # Appel de l'__init__ de la classe parente
        super().__init__(start, end, id, type)

        # Initialisation propre à la classe Passe
        self.passeur = passeur_id
        self.receveur = receveur_id
        self.team_passeur = team_passeur
        self.team_receveur = team_receveur


class Tir(Actions):

    def __init__(self, start, end, id, type, tireur_id, tireur_team):
        # Appel de l'__init__ de la classe parente
        super().__init__(start, end, id, type)

        self.tireur = tireur_id
        self.team = tireur_team

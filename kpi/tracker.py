import pandas as pd
import json
import numpy as np
import math


class Moving_object:
    positions = []
    center_2D = []
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
        #  return a dict containing as key the frame and as value the player's positions
        df = df.T.reset_index(drop=True).T
        df = df.astype(float)
        positions = df.values
        positions = [pos if None not in pos else None for pos in positions]
        self.positions = self.positions + positions

    def add_center_2D(self, df):
        df = df.T.reset_index(drop=True).T
        df = df.astype(float)
        positions = df.values
        positions = [pos if None not in pos else None for pos in positions]
        self.center_2D = self.center_2D + positions


class Game:
    def __init__(self):
        self.team0 = {"players": [], "stats": {}}
        self.team1 = {"players": [], "stats": {}}
        self.ball = None
        self.nb_players = 0
        self.actions = []

    def transform_to_dict(self):
        return {"team0": {'players': [player.__dict__ for player in self.team0['players']]},
                "team1": {'players': [player.__dict__ for player in self.team1['players']]},
                "ball": self.ball.__dict__,
                "actions": [act.__dict__ for act in self.actions]}

    def transform_actions_to_dict(self):
        return {"actions": [act.__dict__ for act in self.actions]}

    def create_ball(self, df_box, df_2D):

        self.ball = Ball()
        self.ball.add_position(df_box)
        self.ball.add_center_2D(df_2D)

    def create_team(self, df_team0_box, df_team1_box, df_team0_2D, df_team1_2D):
        #  return a dict containing all player in the field and their positions at each frame
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

        self.id_team = team

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
        distance_player_ball = [self.calculate_distances(self.center_2D, player.center_2D) for player in all_players]
        distance_player_ball = np.array(distance_player_ball)

        # Use np.argmin(axis=0) to get the indices of the minimum value along each column
        list_argmin = list(np.argmin(distance_player_ball, axis=0))
        self.state = [all_players[argmin].id_player for argmin in list_argmin]
        self.team_possession = [all_players[argmin].id_team for argmin in list_argmin]

    def get_passe_from_model(self, df):

        df['change'] = (df['label'] != df['label'].shift(1)).cumsum()
        val_possession = df[df['label'] == 0]['change'].unique()
        val_passe = df[df['label'] == 1]['change'].unique()
        list_intervall_possession = [(df[df['change'] == v].index[0], df[df['change'] == v].index[-1]) for v in
                                     val_possession]
        list_intervall_passe = [(df[df['change'] == v].index[0], df[df['change'] == v].index[-2]) for v in val_passe]

        all_passe = [[self.state[intervall[0] - 1], self.state[intervall[1] + 1]] + list(intervall) + [
            self.team_possession[intervall[0] - 1], self.team_possession[intervall[0] + 1]] for intervall in
                     list_intervall_passe]
        all_passe_corrected = [passe for passe in all_passe if passe[0] != passe[1]]
        for passe in all_passe_corrected:
            self.state[passe[2]:passe[3]] = [None] * (passe[3] - passe[2])
            self.team_possession[passe[2]:passe[3]] = [None] * (passe[3] - passe[2])
        self.passe = all_passe_corrected

        # Création de masques pour les types

    def detect_passes(self):
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

    """def calculate_angles(self):
        # Convert input lists to NumPy arrays
        points_t = np.array(self.center_2D)[:-2]
        points_t1 = np.array(self.center_2D)[1:-1]
        points_t2 = np.array(self.center_2D)[2:]

        # Calculate vectors between points
        vectors_ab = points_t1 - points_t
        vectors_bc = points_t2 - points_t1

        # Calculate dot products and magnitudes
        dot_products = np.sum(vectors_ab * vectors_bc, axis=1)
        magnitudes_ab = np.linalg.norm(vectors_ab, axis=1)
        magnitudes_bc = np.linalg.norm(vectors_bc, axis=1)

        # Calculate angles in radians
        angles_radians = np.arccos(dot_products / (magnitudes_ab * magnitudes_bc))

        # Convert angles to degrees
        angles_degrees = np.degrees(angles_radians)
        self.angle = angles_degrees
        #return angles_degrees"""


class Actions:

    def __init__(self, start, end, id, type):
        self.start = int(start)
        self.end = int(end)
        self.id = int(id)
        self.type = type


class Passe(Actions):
    def __init__(self, start, end, id, type, passeur_id, receveur_id, team_passeur, team_receveur):
        # Appel de l'__init__ de la classe parente
        super().__init__(start, end, id, type)

        # Initialisation propre à la classe Passe
        self.passeur = passeur_id
        self.receveur = receveur_id
        self.team_passeur = team_passeur
        self.team_receveur = team_receveur

    def get_distance_passe(self):
        print('todo')

    def get_receveur_passeur(self):
        print('todo')

    def get_speed(self):
        print('todo')

    def get_player_eliminated(self, team0, team1, ball):

        print('todo')

    def succeed(self):
        if self.team_receveur == self.team_passeur:
            self.succeed = True
        else:
            self.succeed = False

    def get_(self):
        print('todo')

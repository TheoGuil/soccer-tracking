from math import *
import numpy as np
from trajectory import *


def calcul_distance(x1, y1, x2, y2, p_m):
    # compute distance between two points
    distance = ((float(x2) - float(x1)) / p_m) ** 2 + ((float(y2) - float(y1)) / p_m) ** 2
    return sqrt(distance)


def detect_team(df):
    # separate player of same team
    team_index = df.iloc[0, :]
    end_team1 = min(team_index[team_index == '1'].index)
    end_team2 = min(team_index[team_index == '3'].index)
    teams0 = df.iloc[:, 1:end_team1]
    teams1 = df.iloc[:, end_team1:end_team2]
    ball = df.iloc[4:, end_team2:]
    return teams0, teams1, ball


def change_trajectory(index, df_ball):
    cosine, angle = get_angle(index, df_ball)
    if cosine < 0:
        return True, cosine, angle
    else:
        if angle > 30:
            return True, cosine, angle
        else:
            return False, cosine, angle


def get_angle(index, df_ball):
    x1_ball = float(df_ball.loc[index, "bb_left"]) + float(df_ball.loc[index, "bb_width"]) / 2
    y1_ball = float(df_ball.loc[index, "bb_top"]) + float(df_ball.loc[index, "bb_height"]) / 2
    x0_ball = float(df_ball.loc[index - 1, "bb_left"]) + float(df_ball.loc[index - 1, "bb_width"]) / 2
    y0_ball = float(df_ball.loc[index - 1, "bb_top"]) + float(df_ball.loc[index - 1, "bb_height"]) / 2
    x2_ball = float(df_ball.loc[index + 1, "bb_left"]) + float(df_ball.loc[index + 1, "bb_width"]) / 2
    y2_ball = float(df_ball.loc[index + 1, "bb_top"]) + float(df_ball.loc[index + 1, "bb_height"]) / 2

    a = np.array([x1_ball + x1_ball - x0_ball, y1_ball + y1_ball - y0_ball])
    b = np.array([x1_ball, y1_ball])
    c = np.array([x2_ball, y2_ball])

    ba = a - b
    bc = c - b
    if (bc[0] == 0 and bc[1] == 0) or (ba[0] == 0 and ba[1] == 0):
        cosine_angle = 1
    else:
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    if cosine_angle > 1 or cosine_angle < -1:
        cosine_angle = int(cosine_angle)
    angle = np.degrees(np.arccos(cosine_angle))
    if isnan(cosine_angle) or isnan(angle):
        print("error")
    return cosine_angle, angle


def get_four_point(df, index, col):
    # get coordinates of bbox fout points ( top_left , top_right, ....)
    top_left = (float(df.iloc[index, col]), df.iloc[index, col + 1])
    top_right = (float(df.iloc[index, col]) + float(df.iloc[index, col + 2]), df.iloc[index, col + 1])
    bot_left = (float(df.iloc[index, col]), float(df.iloc[index, col + 1]) + float(df.iloc[index, col + 3]))
    bot_right = (float(df.iloc[index, col]) + float(df.iloc[index, col + 2]),
                 float(df.iloc[index, col + 1]) + float(df.iloc[index, col + 3]))

    return top_left, top_right, bot_left, bot_right


def get_four_center(df, index, col):
    center = (float(df.iloc[index, col]) + float(df.iloc[index, col + 2]) / 2, float(df.iloc[index, col + 1]) + float(
        df.iloc[index, col + 3]) / 2)
    center_r = (center[0] + float(df.iloc[index, col + 2]) / 2, center[1])
    center_l = (center[0] - float(df.iloc[index, col + 2]) / 2, center[1])
    center_t = (center[0], center[1] + float(df.iloc[index, col + 3]) / 2)
    center_b = (center[0], center[1] - float(df.iloc[index, col + 3]) / 2)
    return center_r, center_l, center_t, center_b


def ball_speed(speed_10, speed_25, speed_50, speed_75, speed_1, df_ball, index, pm):
    speed_10.append(
        calcul_distance(df_ball.loc[index, "bb_left"], df_ball.loc[index, "bb_top"],
                        df_ball.loc[index - 3, "bb_left"],
                        df_ball.loc[index - 3, "bb_top"], int(pm)) / 0.1)
    speed_25.append(
        calcul_distance(df_ball.loc[index, "bb_left"], df_ball.loc[index, "bb_top"],
                        df_ball.loc[index - 7, "bb_left"],
                        df_ball.loc[index - 7, "bb_top"], int(pm)) / 0.25)
    speed_50.append(
        calcul_distance(df_ball.loc[index, "bb_left"], df_ball.loc[index, "bb_top"],
                        df_ball.loc[index - 15, "bb_left"],
                        df_ball.loc[index - 15, "bb_top"], int(pm)) / 0.5)
    speed_75.append(
        calcul_distance(df_ball.loc[index, "bb_left"], df_ball.loc[index, "bb_top"],
                        df_ball.loc[index - 22, "bb_left"],
                        df_ball.loc[index - 22, "bb_top"], int(pm)) / 0.75)
    speed_1.append(
        calcul_distance(df_ball.loc[index, "bb_left"], df_ball.loc[index, "bb_top"],
                        df_ball.loc[index - 30, "bb_left"],
                        df_ball.loc[index - 30, "bb_top"], int(pm)))
    return speed_10, speed_25, speed_50, speed_75, speed_1


def calcul_player_speed(df, pixel_to_meter):
    # calcul the player speed , speed_0_5 means calcul speed  on 0.5s
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


def get_density(distance0, distance1, list_id_team0, list_id_team1, id_team):
    if id_team == 1:
        density0_5 = [list_id_team0[idx] for idx, val in enumerate(distance0) if float(val) < 0.5]
        density_1 = [list_id_team0[idx] for idx, val in enumerate(distance0) if float(val) < 1 and float(val) > 0.5]
        density_2 = [list_id_team0[idx] for idx, val in enumerate(distance0) if float(val) < 2 and float(val) > 1]
        density_3 = [list_id_team0[idx] for idx, val in enumerate(distance0) if float(val) < 3 and float(val) > 2]
    elif id_team == 0:
        density0_5 = [list_id_team1[idx] for idx, val in enumerate(distance1) if float(val) < 0.5 and float(val) > 0.5]
        density_1 = [list_id_team1[idx] for idx, val in enumerate(distance1) if float(val) < 1 and float(val) > 1]
        density_2 = [list_id_team1[idx] for idx, val in enumerate(distance1) if float(val) < 2 and float(val) > 2]
        density_3 = [list_id_team1[idx] for idx, val in enumerate(distance1) if float(val) < 3 and float(val) > 3]

    return [density0_5, density_1, density_2, density_3]


def get_closest_player(distance0, distance1, list_id_team0, list_id_team1):
    argmin0 = np.argmin(np.array(distance0))
    argmin1 = np.argmin(np.array(distance1))
    min_team = np.array([distance0[argmin0], distance1[argmin1]])
    id_team_possession = np.argmin(min_team)
    if id_team_possession == 0:
        id_player_possession = list_id_team0[argmin0]
    elif id_team_possession == 1:
        id_player_possession = list_id_team1[argmin1]
    return id_player_possession, id_team_possession, min_team, argmin0, argmin1


def get_duel(distance0, argmin0, distance1, argmin1, id_team_possession, list_id_team0, list_id_team1):
    if (distance0[argmin0] - distance1[argmin1]) ** 2 < 0.5:
        if id_team_possession == 1:
            duel = list_id_team0[argmin0]
        else:
            duel = list_id_team1[argmin1]
    else:
        duel = "no"
    return duel


def distance_KPI(index, speed, df_ball, df_team0, df_team1, pm):
    # get which player is in possession of the ball or detect a passe
    list_index0 = [i for i in range(0, len(df_team0.columns), 5)]
    list_index1 = [i for i in range(0, len(df_team1.columns), 5)]
    list_id_team0 = list(dict.fromkeys(list(df_team0.iloc[1, :])))
    list_id_team1 = list(dict.fromkeys(list(df_team1.iloc[1, :])))
    x_ball = float(df_ball.loc[index, "bb_left"]) + float(df_ball.loc[index, "bb_width"]) / 2
    y_ball = float(df_ball.loc[index, "bb_top"]) + float(df_ball.loc[index, "bb_height"]) / 2
    distance0 = []
    distance1 = []
    for v in list_index0:
        tl0, tr0, bl0, br0 = get_four_point(df_team0, index, v)
        tl1, tr1, bl1, br1 = get_four_point(df_team1, index, v)
        center0_r, center0_l, center0_t, center0_b = get_four_center(df_team0, index, v)
        center1_r, center1_l, center1_t, center1_b = get_four_center(df_team1, index, v)
        # compute distance between each player and the ball , then get the closest player for each team
        distance0.append(min([calcul_distance(tl0[0], tl0[1], x_ball, y_ball, pm),
                              calcul_distance(tr0[0], tr0[1], x_ball, y_ball, pm),
                              calcul_distance(bl0[0], bl0[1], x_ball, y_ball, pm),
                              calcul_distance(br0[0], br0[1], x_ball, y_ball, pm),
                              calcul_distance(center0_r[0], center0_r[1], x_ball, y_ball, pm),
                              calcul_distance(center0_l[0], center0_l[1], x_ball, y_ball, pm),
                              calcul_distance(center0_t[0], center0_t[1], x_ball, y_ball, pm),
                              calcul_distance(center0_b[0], center0_b[1], x_ball, y_ball, pm)]))

        distance1.append(min([calcul_distance(tl1[0], tl1[1], x_ball, y_ball, pm),
                              calcul_distance(tr1[0], tr1[1], x_ball, y_ball, pm),
                              calcul_distance(bl1[0], bl1[1], x_ball, y_ball, pm),
                              calcul_distance(br1[0], br1[1], x_ball, y_ball, pm),
                              calcul_distance(center1_r[0], center1_r[1], x_ball, y_ball, pm),
                              calcul_distance(center1_l[0], center1_l[1], x_ball, y_ball, pm),
                              calcul_distance(center1_t[0], center1_t[1], x_ball, y_ball, pm),
                              calcul_distance(center1_b[0], center1_b[1], x_ball, y_ball, pm)]))

    # get closest player, team from the ball
    id_player_possession, id_team_possession, min_team, argmin0, argmin1 = get_closest_player(distance0, distance1,
                                                                                              list_id_team0,
                                                                                              list_id_team1)

    # decide if the owner of the ball is fighting for it ,and with who
    duel = get_duel(distance0, argmin0, distance1, argmin1, id_team_possession, list_id_team0, list_id_team1)
    # get density around the ball of the team who does not have the ball
    densite = get_density(distance0, distance1, list_id_team0, list_id_team1, id_team_possession)
    if speed < 9 and min_team[id_team_possession] < 0.8:
        return id_team_possession, id_player_possession, min_team[id_team_possession], duel, densite, False
    else:
        return id_team_possession, id_player_possession, min_team[id_team_possession], duel, densite, True


def create_ball_KPI(df_ball, pm, df_team0, df_team1):
    # compute speed of the ball , which player has the possession and detect pass
    df_return = df_ball.iloc[30:, :].copy()
    acceleration = [None for i in range(7)]
    trajectory_change, cos_angle = [None], [None]
    speed_10, speed_25, speed_50, speed_75, speed_1, possession_team, possession_player, passe_list, distance_player, \
    duel_list, density_0, density_1, density_2, density_3 = [], [], [], [], [], [], [], [], [], [], [], [], [], []

    for index, row in df_return.iterrows():
        # get speed of the ball
        speed_10, speed_25, speed_50, speed_75, speed_1 = ball_speed(speed_10, speed_25, speed_50, speed_75, speed_1,
                                                                     df_ball, index, pm)
        # get acceleration
        if index > 40:
            acceleration.append((speed_10[-1] - speed_10[-3]) / 0.1)
        # detect pass or get if player that has possession
        id_team, id_player, distance_ball_player, duel, densite, passe = distance_KPI(index, speed_10[-1], df_ball,
                                                                                  df_team0,
                                                                               df_team1, pm)
        #
        if index > 34 and index < len(df_return) + 33:
            trajectory, cosine, ang = change_trajectory(index, df_return)
            cos_angle.append([cosine, ang])
            trajectory_change.append(trajectory)
        elif index == len(df_return) + 33:
            cos_angle.append([1, 0])
            trajectory_change.append(False)

        duel_list.append(duel)
        distance_player.append(distance_ball_player)
        possession_team.append(id_team)
        possession_player.append(id_player)
        passe_list.append(passe)
        density_0.append(densite[0])
        density_1.append(densite[1])
        density_2.append(densite[2])
        density_3.append(densite[3])

    df_return["speed_10"] = speed_10
    df_return["speed_25"] = speed_25
    df_return["speed_50"] = speed_50
    df_return["speed_75"] = speed_75
    df_return["speed_1"] = speed_1
    df_return["acceleration"] = acceleration
    df_return["possession_team"] = possession_team
    df_return["possession_player"] = possession_player
    df_return["passe"] = passe_list
    df_return["distance_player"] = distance_player
    df_return["cos_angle"] = cos_angle
    df_return["trajectory_change"] = trajectory_change
    df_return["duel"] = duel_list
    df_return["density_0"] = density_0
    df_return["density_1"] = density_1
    df_return["density_2"] = density_2
    df_return["density_3"] = density_3

    return df_return


def create_player_KPI(df_team0, df_team1):
    #  return one df per player with positions and speed
    players_df_list0 = []
    players_df_list1 = []
    id_player_list0 = []
    id_player_list1 = []
    # iterate over both dataframe teams0 team1, and extract bbox for each player as pl0 and pl1
    for i in range(0, len(df_team0.columns), 5):
        # get the id of each player as it was written in the original file
        id_pl0 = list(set(list(df_team0.iloc[1, i:i + 5])))
        id_pl1 = list(set(list(df_team1.iloc[1, i:i + 5])))
        if len(id_pl0) > 1 or len(id_pl1) > 1:
            print("error")
            break
        pl0 = df_team0.iloc[4:, i:i + 5]
        pl1 = df_team1.iloc[4:, i:i + 5]
        pl0.columns = ["bb_left", "bb_top", "bb_width", "bb_height", "conf"]
        pl1.columns = ["bb_left", "bb_top", "bb_width", "bb_height", "conf"]
        # add column speed in dataframe pl0 and pl1
        df_pl0 = calcul_player_speed(pl0, 25)
        df_pl1 = calcul_player_speed(pl1, 25)
        # append dataframe df_pl0 and df_pl1 in respective list and the same for id_pl0
        players_df_list0.append(df_pl0)
        id_player_list0.append(id_pl0[0])
        players_df_list1.append(df_pl1)
        id_player_list1.append(id_pl1[0])
    return players_df_list0, players_df_list1, id_player_list0, id_player_list1


def create_KPI(team0, team1, ball):
    # create KPI for ball and teams

    # rename columns names of the ball dataframe
    ball.columns = ["bb_left", "bb_top", "bb_width", "bb_height", "conf"]
    ball_df = create_ball_KPI(ball, 25, team0, team1)
    list_team0, list_team1, id_team0, id_team1 = create_player_KPI(team0, team1)
    return ball_df, list_team0, list_team1, id_team0, id_team1

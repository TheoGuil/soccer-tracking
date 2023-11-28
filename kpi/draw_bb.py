import json
import pandas as pd
import os
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--frame', type=str, required=True)
parser.add_argument('--label_dir', type=str, required=True)
parser.add_argument('--debug', type=bool, default=False)

args = parser.parse_args()
frame_folder = args.frame
label_dir = args.label_dir
debug = args.debug

list_dir_frame = os.listdir(frame_folder)
list_dir_frame.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
count = 0


def draw_object(positions, img, count, color_t):
    # draw object positions given by a list
    if len(positions) > 0:
        for key, value in positions[count].items():
            x = int(value["x"])
            y = int(value["y"])
            # x2 = int(value["w"]) + x1
            # y1 = y2 - int(value["h"])
            cv2.circle(img, (x, y), radius=10, color=color_t, thickness=-1)
            count += 1
    return img


def get_team_ball_dict(path_label):
    # load the positions of each player and the ball contained in josn file
    team0 = json.load(open(os.path.join(path_label, "players_team0.json")))
    team1 = json.load(open(os.path.join(path_label, "players_team1.json")))
    ball = json.load(open(os.path.join(path_label, "ball.json")))
    return team0, team1, ball


for dir_name in list_dir_frame:
    team0, team1, ball = get_team_ball_dict(os.path.join(label_dir, dir_name))
    dir_frame = os.listdir(os.path.join(frame_folder, dir_name))
    dir_frame.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    count = 0
    for frame in dir_frame:
        frame_path = os.path.join(frame_folder, dir_name, frame)
        img = cv2.imread(frame_path)
        print(len(team0))
        print(len(team1))
        for pl0, pl1 in zip(team0, team1):
            positions0 = pl0["positions"]
            positions1 = pl1["positions"]
            img = draw_object(positions0, img, count, (255, 0, 0))
            img = draw_object(positions1, img, count, (0, 0, 255))
        img = draw_object(ball['positions'], img, count, (255, 255, 255))
        if debug:
            cv2.imshow('frame', img)
            cv2.waitKey(1000)
        result_dir = os.path.join('/home/reda/Documents/KPI/result_detection', dir_name)
        if not os.path.isdir(result_dir):
            os.makedirs(result_dir)
        cv2.imwrite(os.path.join(result_dir, frame), img)
        count += 1

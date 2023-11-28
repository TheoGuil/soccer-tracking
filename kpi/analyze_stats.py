import pandas as pd
import os
import argparse
from math import *
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--dir_stats', type=str, required=True)
args = parser.parse_args()


def get_max_speed(list_df):
    max_0_5, max_1, max_2, max_3, max_4, max_5 = [], [], [], [], [], []
    for df in list_df:
        max_0_5.append(df["speed_0_5"].max())
        max_1.append(df["speed_1"].max())
        max_2.append(df["speed_2"].max())
        max_3.append(df["speed_3"].max())
        max_4.append(df["speed_4"].max())
        max_5.append(df["speed_5"].max())
    return [max(max_0_5), max(max_1), max(max_2), max(max_3), max(max_4), max(max_5)]


dir_stats = os.listdir(args.dir_stats)
list_df = []
for dir_name in dir_stats:
    dir_path = os.path.join(args.dir_stats, dir_name)
    list_csv_file0 = os.listdir(os.path.join(dir_path, "team0"))
    list_csv_file1 = os.listdir(os.path.join(dir_path, "team1"))

    list_df = list_df + [pd.read_csv(os.path.join(dir_path, "team0", i), header=0) for i in list_csv_file0]
    list_df = list_df + [pd.read_csv(os.path.join(dir_path, "team1", i), header=0) for i in list_csv_file1]

list_max = get_max_speed(list_df)
print(list_max)

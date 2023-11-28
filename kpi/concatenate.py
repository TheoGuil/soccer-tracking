import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dir_csv', type=str, required=True)
parser.add_argument('--outfile', type=str, required=True)
args = parser.parse_args()

root_dir = args.dir_csv
dir_csv = os.listdir(root_dir)
dir_csv.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
final_csv = pd.read_csv(os.path.join(root_dir, dir_csv[0]),header=None)
print(final_csv.shape)
for csv_file in dir_csv[1:]:
    csv_path = os.path.join(root_dir, csv_file)
    df_player = pd.read_csv(csv_path,header=None)
    if df_player.shape[1] == 121:
        print("error in df_player")
    final_csv = pd.concat([final_csv, df_player], axis=0)
    if final_csv.shape[1] == 121:
        print("error at concat")

final_csv.to_csv(args.outfile)

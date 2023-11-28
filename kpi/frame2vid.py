import cv2
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--frame_dir', type=str, required=True)
parser.add_argument('--out_dir', type=str, required=True)
parser.add_argument('--video_dir', type=str, required=True)
args = parser.parse_args()

frame_dir = args.frame_dir
out_dir = args.out_dir
video_dir = args.video_dir
frameSize = (2160, 3840)

for directory in os.listdir(frame_dir):

    cap = cv2.VideoCapture(os.path.join(video_dir, directory + '.mp4'))
    fps = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(os.path.join(out_dir, directory + ".mp4"), cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), int(fps),
                          int(cap.get(3)), int(cap.get(4)))
    frames_path = os.path.join(frame_dir, directory)
    for frame in frames_path:
        img = cv2.imread(os.path.join(frames_path, frame))
        out.write(img)
    out.release()

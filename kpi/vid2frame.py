import cv2
import os

folder = '/home/reda/Documents/KPI/top_view_video'
list_video = os.listdir(folder)
count = 0
for video in list_video:
    vidcap = cv2.VideoCapture(os.path.join(folder, video))
    success, image = vidcap.read()
    count = 0
    if not os.path.isdir("top_view_frame/" + video[:-4]):
        os.makedirs("top_view_frame/" + video[:-4])
    while success:
        cv2.imwrite("top_view_frame/"+video[:-4]+"/frame%d.jpg" % count, image)  # save frame as JPEG file
        success, image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1

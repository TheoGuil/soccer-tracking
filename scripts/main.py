from get_pitch_coordinates import *

if __name__ == '__main__':
    print("start running")
    get_pitch_coordinates(folder_path = '../archive/top_view', 
                      csv_path = "annotations/*.csv", video_path ="videos/*.mp4",
                      keypoint_path = '../archive/drone_keypoints.json', 
                      save_path = '../new_dataset/')
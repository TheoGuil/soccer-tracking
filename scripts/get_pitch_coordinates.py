import sportslabkit as slk
from sportslabkit.utils import load_keypoints
from pathlib import Path

def get_pitch_coordinates(folder_path: str, csv_path: str, 
                          video_path: str, keypoint_path: str,
                          save_path: str, coordinate_method: str = 'center') -> None:
    '''
    Convert BoundingBox to Pitch Coordinates
    and save the files to the save_path
    
    Args :
        folder_path : path to the folder
        csv_path : path to the csv file
        video_path : path to the video file
        keypoint_path : path to the keypoint file
        save_path : path to save the files
        coordinate_method : Method to determine the point within the bounding box to transform.
                            Options include 'center', 'bottom_middle', 'top_middle'.
                            Default is 'center'
        
    
    Returns : None
    '''
    
    dataset_path = Path(folder_path)
    path_to_csv = sorted(dataset_path.glob(csv_path))
    path_to_mp4 = sorted(dataset_path.glob(video_path))
    
   

    
    for csv, mp4 in zip(path_to_csv, path_to_mp4):
        cam = slk.Camera(mp4)  # Camera object will be used to load frames
        cam.source_keypoints, cam.target_keypoints = load_keypoints(keypoint_path)
        
        bbdf = slk.load_df(csv)  # We will use this as ground truth
        codf = bbdf.to_codf(cam.H, method='center') # center because we want to get the center of the bounding box
        
        # Save the file
        codf.to_csv(save_path + csv.name, index=True)
        
    print ("File saved to " + save_path + " successfully")
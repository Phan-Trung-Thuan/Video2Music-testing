from moviepy.editor import VideoFileClip
import os
from function import *

video_dir_path = './dataset/video'
motion_feature_dir_path = './dataset/vevo_motion'

# If the directory is not exist then create it
if not os.path.exists(motion_feature_dir_path):
    os.makedirs(motion_feature_dir_path)

idList = get_id_list(idlist_path='./dataset/vevo_meta/idlist.txt')

# Extract motion feature for each video downloaded
for index, _ in idList:
    video_file_path = os.path.join(video_dir_path, f'{index}.mp4')
    motion_feature_file_path = os.path.join(motion_feature_dir_path, f'{index}_motion.txt')
    # If the video is downloaded and have not extract motion feature then extract it
    if os.path.exists(video_file_path) and not os.path.exists(motion_feature_file_path):
        video_no_sound, _ = get_video_audio(video_file_path)
        
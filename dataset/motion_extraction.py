from moviepy.editor import VideoFileClip
import numpy as np
import os
from function import *

video_dir_path = './dataset/video'
motion_feature_dir_path = './dataset/vevo_motion'

# If the directory is not exist then create it
if not os.path.exists(motion_feature_dir_path):
    os.makedirs(motion_feature_dir_path)

idList = get_id_list(idlist_path='./dataset/vevo_meta/idlist.txt')

# Extract motion feature for each video downloaded
for index, _ in idList[:1]:
    video_file_path = os.path.join(video_dir_path, f'{index}.mp4')
    motion_feature_file_path = os.path.join(motion_feature_dir_path, f'{index}_motion.npy')

    # If the video is downloaded and have not extract motion feature then extract it
    if os.path.exists(video_file_path) and not os.path.exists(motion_feature_file_path):
        # Get video no sound
        video_no_sound, _ = get_video_audio(video_file_path)
        
        # Get frame list step by 1 second
        frames = get_frame_list(video_no_sound)
        num_frames = len(frames)

        motion_values = np.zeros(num_frames, dtype=np.float32)
        for i in range(1, num_frames):
            # Calculate absolute difference between 2 adjacent frames
            abs_diff = np.abs(frames[i] - frames[i - 1])
            motion_values[i] = np.average(abs_diff)

        # Save motion values
        np.save(motion_feature_file_path, motion_values)

from moviepy.editor import VideoFileClip
import os
import numpy as np
from function import *

idList = get_id_list(idlist_path='./dataset/vevo_meta/idlist.txt')

paths = ['./dataset/video', 
         './dataset/vevo_note_density', 
         './dataset/vevo_loudness', 
         './dataset/vevo_chord_sequence', 
         './dataset/vevo_key', 
         './dataset/vevo_emotion', 
         './dataset/vevo_scene_offset', 
         './dataset/vevo_motion', 
         './dataset/vevo_semantic']

for path in paths:
    # If the directory is not exist then create it
    if not os.path.exists(path):
        os.makedirs(path)

# Extract feature for each VIDEO - AUDIO pair
for index, id in idList:
    video_path = os.path.join(paths[0], f'{index}.mp4')

    # If the video is not downloaded then download it
    if not os.path.exists(video_path):
        download_youtube_video(id, paths[0], f'{index}.mp4')

    video = VideoFileClip(video_path)
    video_no_sound = video.without_audio()
    audio = video.audio()

    # MUSIC FEATURE === Note density === 1
    # MUSIC FEATURE === Loudness === 2
    # MUSIC FEATURE === Chord sequence === 3
    # MUSIC FEATURE === Key === 4

    # VIDEO FEATURE === Emotion === 5
    # VIDEO FEATURE === Scene offset === 6
    # VIDEO FEATURE === Motion === 7
    motion_feature_path = os.path.join(paths[7], f'{index}_motion.npy')
    # If this video does not extract motion feature then extract it
    if not os.path.exists(motion_feature_path):
        pass

    # VIDEO FEATURE === Semantic === 8
    semantic_feature_path = os.path.join(paths[8], f'{index}_semantic.npy')
    # If this video does not extract semantic feature then extract it
    if not os.path.exists(semantic_feature_path):
        pass

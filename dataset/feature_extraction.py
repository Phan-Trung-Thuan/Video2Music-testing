from moviepy.editor import VideoFileClip
import os
from function import *

idList = get_id_list(idlist_path='./dataset/vevo_meta/idlist.txt')

download_video_path = './dataset/video'
# If the directory is not exist then create it
if not os.path.exists(download_video_path):
    os.makedirs(download_video_path)

# Extract feature for each video - audio pair
for index, id in idList:
    video_path = os.path.join(download_video_path, f'{index}.mp4')

    # If the video is not downloaded then download it
    if not os.path.exists(video_path):
        download_youtube_video(id, download_video_path, f'{index}.mp4')

    video = VideoFileClip(video_path)
    video_no_sound = video.without_audio()
    audio = video.audio()

    # MUSIC FEATURE === Note density ===
    # MUSIC FEATURE === Loudness ===
    # MUSIC FEATURE === Chord sequence ===
    # MUSIC FEATURE === Key ===

    # VIDEO FEATURE === Emotion ===
    # VIDEO FEATURE === Scene offset ===
    # VIDEO FEATURE === Motion ===
    # VIDEO FEATURE === Semantic ===

from scenedetect import SceneManager, open_video, FrameTimecode, AdaptiveDetector
from function import *
import numpy as np
import os

def find_scenes(video_path):
    video = open_video(video_path)
    scene_manager = SceneManager()
    scene_manager.add_detector(
        AdaptiveDetector())
    # Detect all scenes in video from current position to end.
    scene_manager.detect_scenes(video, show_progress=False)
    # `get_scene_list` returns a list of start/end timecode pairs
    # for each scene that was found.
    return scene_manager.get_scene_list()

def scene_offset(video_path):
    scene_offset_list = []
    scene_list = find_scenes(video_path)
    for _, scene in enumerate(scene_list):
        scene_start_frame = scene[0].get_frames()
        scene_end_frame = scene[1].get_frames()
        scene_start_time = int(FrameTimecode(timecode=scene_start_frame, fps=25.00).get_seconds())
        scene_end_time = int(FrameTimecode(timecode=scene_end_frame, fps=25.00).get_seconds())
        if scene_start_time == scene_end_time:
            scene_offset_list.append((scene_start_time, 0))
        else:
            sec = scene_start_time
            scene_sec = 0
            for j in range(scene_start_time, scene_end_time):
                if sec == scene_end_time:
                    break
                scene_offset_list.append((sec, scene_sec))
                sec += 1
                scene_sec += 1
    return scene_offset_list

def main():
    idList = get_id_list(idlist_path='./dataset/vevo_meta/idlist.txt')
    scene_offset_path = './dataset/vevo_scene_offset'

    if not os.path.exists(scene_offset_path):
        os.makedirs(scene_offset_path)

    for index, _ in idList:
        video_file_path = f'./dataset/video/{index}.mp4'
        if os.path.exists(video_file_path):
            offset_values = scene_offset(video_file_path)
            offset_file_path = os.path.join(scene_offset_path, f'{index}_scene_offset.npy')
            # Save semantic values
            np.save(offset_file_path, offset_values)
            
            # NOTIFICATION
            print(f'Saved into {offset_file_path}')

if __name__ == '__main__':
    main()

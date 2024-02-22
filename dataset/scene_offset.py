from scenedetect import SceneManager, open_video, FrameTimecode, AdaptiveDetector


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
    for i, scene in enumerate(scene_list):
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
    video = scene_offset('video/001.mp4')
    for i in range(len(video)):
        print('%d, %d' % (video[i][0], video[i][1]))


if __name__ == '__main__':
    main()

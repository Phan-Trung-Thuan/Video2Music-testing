from moviepy.editor import VideoFileClip
import torch
import clip
from PIL import Image
import numpy as np
import os
from function import *

def predict_emotion(frame, model, preprocess):
    emotions = ['exciting', 'fearful', 'tense', 'sad', 'relaxing', 'neutral']
    text = clip.tokenize([f'This image represents {emo}' for emo in emotions]).to(DEVICE)
    # Encode text
    text_encode = model.encode_text(text)

    image = preprocess(Image.fromarray(frame)).unsqueeze(0).to(DEVICE)
    # Encode image
    img_encode = model.encode_image(image)

    # Calculate cosine similarity
    cos_sim = torch.nn.functional.cosine_similarity(text_encode, img_encode, dim=1)
    cos_sim = cos_sim.cpu().detach().numpy()

    # Calculate probabilities of each emotion
    probabilities = [value / np.sum(cos_sim) for value in cos_sim]
    return probabilities

def smooth_window(vec, window_size=5):
    smoothed = []
    
    for i in range(len(vec)):
        # Determine the range of the current window
        start_index = max(0, i - (window_size // 2))
        end_index = min(len(vec), i + (window_size // 2) + 1)
        
        # Get the frames within the window
        window = vec[start_index:end_index]
        
        # Calculate the average vector across the window frames
        average_vector = np.mean(window, axis=0)
        smoothed.append(average_vector)
    
    return smoothed


def main():
    video_dir_path = './dataset/video'
    emotion_feature_dir_path = './dataset/vevo_emotion'

    # If the directory is not exist then create it
    if not os.path.exists(emotion_feature_dir_path):
        os.makedirs(emotion_feature_dir_path)

    idList = get_id_list(idlist_path='./dataset/vevo_meta/idlist.txt')

    # Load CLIP model
    model, preprocess = clip.load('ViT-L/14', device=DEVICE)

    # Extract emotion feature for each video downloaded
    for index, _ in idList:
        video_file_path = os.path.join(video_dir_path, f'{index}.mp4')
        emotion_feature_file_path = os.path.join(emotion_feature_dir_path, f'{index}_emotion.npy')

        # If the video is downloaded and have not extract emotion feature then extract it
        if os.path.exists(video_file_path) and not os.path.exists(emotion_feature_file_path):
            # NOTIFICATION
            print(f'Processing video {video_file_path}')

            # Get video no sound
            video_no_sound, _ = get_video_audio(video_file_path)
            
            # Get frame list step by 1 second
            frames = get_frame_list(video_no_sound)
            num_frames = len(frames)

            # NOTIFICATION
            print(f'Extracting emotion feature from video {video_file_path}')

            # Calculate emotions probabilities of each frame
            emotion_values = np.zeros((num_frames, 6), dtype=np.float32)
            for i in range(num_frames):
                emotion_values[i] = predict_emotion(frames[i], model, preprocess)

            # Slide a smoothing window through emotion values
            emotion_values = smooth_window(emotion_values, window_size=5)

            # NOTIFICAITON
            print(f'Finish extract emotion feature from video {video_file_path}', end=' ')

            # Save emotion values
            np.save(emotion_feature_file_path, emotion_values)

            # NOTIFICATION
            print(f'Saved into {emotion_feature_file_path}')

if __name__ == '__main__':
    main()
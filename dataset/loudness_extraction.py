import os
import math
import pretty_midi
import sys
import numpy as np
import audioop

from function import *
from pydub import AudioSegment
from pydub.utils import make_chunks

def loudness_to_normalized(loudness):
    return 10 ** (loudness / 20)

def main():
    audio_dir_path = "./dataset/vevo_audio/wav/"
    loudness_feature_dir_path = "./dataset/vevo_loudness/"
    
    # If the directory is not exist then create it
    if not os.path.exists(loudness_feature_dir_path):
        os.makedirs(loudness_feature_dir_path)

    idList = get_id_list(idlist_path='./dataset/vevo_meta/idlist.txt')

    for index, _ in idList:   
        audio_file_path = os.path.join(audio_dir_path, f'{index}.wav')
        loudness_feature_file_path = os.path.join(loudness_feature_dir_path, f'{index}_loudness.npy')        
        
        # If the audio is not available
        if not os.path.exists(audio_file_path):
          print(f'Audio {index}.wav not found!')
          continue;

        # If the audio is available and have not extract loudness feature then extract it
        if os.path.exists(audio_file_path) and not os.path.exists(loudness_feature_file_path):  
          # NOTIFICATION
          print(f'Processing audio {audio_file_path}')

          audio_data = AudioSegment.from_file(audio_file_path)
          audio_data = audio_data.set_channels(1)  # convert to mono
          audio_data = audio_data.set_frame_rate(44100)  # set sample rate to 44100 Hz
          chunk_length = 1000  # chunk length in milliseconds
          chunks = make_chunks(audio_data, chunk_length)
          loudness_per_second = []

          # NOTIFICATION
          print(f'Extract loundness feature from audio {audio_file_path}')

          for chunk in chunks:
              data = chunk.raw_data  # get raw data as bytes
              rms = audioop.rms(data, 2)  # calculate RMS loudness using audioop module

              # if RMS = 0, then RMS = 32767 so that loudness = 20 -> normalize_loudness = 1
              if (rms == 0): 
                rms += sys.float_info.epsilon;
                      
              loudness = 20 * np.log10(rms / 32767)  # convert to decibels
              normalized_loudness = loudness_to_normalized(loudness)  # convert to 0-1 scale
              normalized_loudness = format(normalized_loudness, ".4f")
              loudness_per_second.append(normalized_loudness)   

          # NOTIFICATION    
          print(f'Finish extract loundness feature from audio {audio_file_path}')
    
          # Save note density values
          np.save(loudness_feature_file_path, loudness_per_second)

          # NOTIFICATION
          print(f'Saved into {loudness_feature_file_path}')
        else:
          print(f'Loudness feature of {index}.wav exists')
if __name__ == "__main__":
    main()
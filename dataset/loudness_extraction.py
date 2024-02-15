import os
import math
import pretty_midi

from pydub import AudioSegment
from pydub.utils import make_chunks
import numpy as np
import audioop

def loudness_to_normalized(loudness):
    return 10 ** (loudness / 20)

def main():
    directory_vevo_wav = "./dataset/vevo_audio/wav/"
    loudness_feature_dir_path = "./dataset/vevo_loudness/"
    # If the directory is not exist then create it
    if not os.path.exists(loudness_feature_dir_path):
        os.makedirs(loudness_feature_dir_path)

    for filename in sorted(os.listdir(directory_vevo_wav)):    
        fname = filename.split(".")[0]
        audio_file_path = os.path.join(directory_vevo_wav, filename.replace("lab", "wav"))
        loudness_feature_file_path = "./dataset/vevo_loudness/" + fname + ".lab"        

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
                rms = 32767
                      
              loudness = 20 * np.log10(rms / 32767)  # convert to decibels
              normalized_loudness = loudness_to_normalized(loudness)  # convert to 0-1 scale
              normalized_loudness = format(normalized_loudness, ".4f")
              loudness_per_second.append(normalized_loudness)   

          # NOTIFICATION    
          print(f'Finish extract loundness feature from audio {audio_file_path}')
    
          with open(loudness_feature_file_path, 'w', encoding = 'utf-8') as f:
              for i in range(0, len(loudness_per_second)):
                  f.write(str(i) + " "+str(loudness_per_second[i])+"\n")

          # NOTIFICATION
          print(f'Saved into {loudness_feature_file_path}')

if __name__ == "__main__":
    main()
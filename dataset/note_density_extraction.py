import os
from function import *
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH


def main():
    audio_dir_path = './dataset/vevo_audio'
    note_density_feature_dir_path = './dataset/vevo_note_density'

    # If the directory is not exist then create it
    if not os.path.exists(note_density_feature_dir_path):
        os.makedirs(note_density_feature_dir_path)

    idList = get_id_list(idlist_path='./dataset/vevo_meta/idlist.txt')

    # Extract note density feature for each audio
    for index, _ in idList:
        
        audio_file_path = os.path.join(audio_dir_path, f'{index}.wav')
        note_density_feature_file_path = os.path.join(note_density_feature_dir_path, f'{index}_note_density.lab')

        # If the audio is available and have not extract note density feature then extract it
        if os.path.exists(audio_file_path) and not os.path.exists(note_density_feature_file_path):
            # NOTIFICATION
            print(f'Processing audio {audio_file_path}')

            model_output, midi_data, note_events = predict(audio_file_path)
            
            # NOTIFICATION
            print(f'Extract note density feature from that midi file')

            total_time = midi_data.get_end_time()        
            note_density_list = []
            for i in range(int(total_time)+1):
                start_time = i
                end_time = i + 1
                total_notes = 0
                for instrument in midi_data.instruments:
                    for note in instrument.notes:
                        if note.start < end_time and note.end > start_time:
                            total_notes += 1
                note_density = total_notes / float(end_time - start_time)
                note_density_list.append(note_density)

            # NOTIFICATION    
            print(f'Note density list of {audio_file_path}: {note_density_list}', end='. ')
            print(f'Finish extract note density feature from audio {audio_file_path}')

            # Save note density values           
            with open(note_density_feature_file_path, 'w', encoding = 'utf-8') as f:
                for i in range(len(note_density_list)):
                  f.write(str(i) + " "+str(note_density_list[i])+"\n")

            # NOTIFICATION
            print(f'Saved into {note_density_feature_file_path}')

if __name__ == '__main__':
    main()
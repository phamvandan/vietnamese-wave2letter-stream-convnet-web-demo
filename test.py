from pydub import AudioSegment

def convert_to_wav(filepath):
    print("converting....")
    new_name = filepath.split(".")[0]+"_.wav"
    wav_file = AudioSegment.from_file(file=filepath)
    wav_file = wav_file.set_frame_rate(16000)
    wav_file = wav_file.set_sample_width(2)
    wav_file = wav_file.set_channels(1)
    wav_file.export(new_name, bitrate="256", format='wav')
    return new_name


convert_to_wav("static/audios/h/batdenpt_.wav")

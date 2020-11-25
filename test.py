# encoding=utf8
import os
import signal
from subprocess import Popen, PIPE

model_path = "/root/src/model"
w2l_bin = "/root/wav2letter/build/inference/inference/examples/interactive_streaming_asr_example"
w2l_process = Popen(
        ['{} --input_files_base_path={}'.format(w2l_bin, model_path)],
        stdin=PIPE, stdout=PIPE, stderr=PIPE,
        shell=True)
files = os.listdir("/root/src/eagle_vnspeech2text/PVD/inference/audio/")
paths_to_audio_file = []
for file in files:
    paths_to_audio_file.append(str(os.path.join("/root/src/eagle_vnspeech2text/PVD/inference/audio/", file)))
# print(paths_to_audio_file)
# w2l_process.stdin.write(b"output=/root/src/eagle_vnspeech2text/PVD/inference/out.txt\n")
# w2l_process.stdin.write(b"endtoken=DONE\n")
f = open("/root/src/eagle_vnspeech2text/PVD/inference/out.txt", "w+")
for path_to_audio_file in paths_to_audio_file:
    print(path_to_audio_file)
    # write to the stdin of the process
    # make sure to flush and add \n to the string
    # w2l_process.stdin.write(
    #     b"output=/root/src/eagle_vnspeech2text/PVD/inference/out.txt\n")
    # w2l_process.stdin.write(b"endtoken=DONE\n")
    w2l_process.stdin.write(bytes("input="+path_to_audio_file+"\n", encoding='utf-8'))
    w2l_process.stdin.flush()
    skip = True
    while True:
    #     # read from process stdout
        output = w2l_process.stdout.readline()
        if b'#finish transcribing\n' in output:
    #         # finish transcribing an audio
            print("FINISHING")
            break
        output = output.decode('utf-8')
        if not skip:
            output = output.split(",")[-1].replace("\n","")
            print(output)
        if "transcription" in output:
            skip = False
    break
# finish the process
os.killpg(os.getpgid(w2l_process.pid), signal.SIGTERM)
from flask import Flask
from flask import request
app = Flask(__name__)
import os
import signal
from subprocess import Popen, PIPE

class w2l_processing:
    def __init__(self):
        self.model_path = "/root/src/vietnamese-wave2letter-stream-convnet-web-demo/model"
        self.w2l_bin = "/root/wav2letter/build/inference/inference/examples/interactive_streaming_asr_example"
        self.w2l_process = Popen(['{} --input_files_base_path={}'.format(self.w2l_bin, self.model_path)],
                            stdin=PIPE, stdout=PIPE, stderr=PIPE,shell=True)

    def process_file(self, path_to_audio_file):
        print(path_to_audio_file)
        self.w2l_process.stdin.write(bytes("input=" + path_to_audio_file + "\n", encoding='utf-8'))
        self.w2l_process.stdin.flush()
        text = ""
        skip = True
        while True:
            #     # read from process stdout
            output = self.w2l_process.stdout.readline()
            #if b'#finish transcribing\n' in output:
                #         # finish transcribing an audio
             #   print("FINISHING")
                #break
            # print(output)
            output = output.decode('utf-8')
            if not skip:
                output = output.split(",")[-1].replace("\n", "").strip()
                text += " " + output
            #print(text)
            if "#finish transcribing" in text:
                text = text.split("#finish transcribing")[0]
                break
            if "transcription" in output:
                skip = False
        text = text.strip()
        return  text

    def kill_process(self):
        os.killpg(os.getpgid(self.w2l_process.pid), signal.SIGTERM)

w2l = w2l_processing()

# files = os.listdir("/root/src/eagle_vnspeech2text/PVD/inference/audio/")
# paths_to_audio_file = []
# for file in files:
#     paths_to_audio_file.append(str(os.path.join("/root/src/eagle_vnspeech2text/PVD/inference/audio/", file)))
# # print(paths_to_audio_file)
# # w2l_process.stdin.write(b"output=/root/src/eagle_vnspeech2text/PVD/inference/out.txt\n")
# # w2l_process.stdin.write(b"endtoken=DONE\n")
# f = open("/root/src/eagle_vnspeech2text/PVD/inference/out.txt", "w+")
# for path_to_audio_file in paths_to_audio_file:
#     print(path_to_audio_file)
#     # write to the stdin of the process
#     # make sure to flush and add \n to the string
#     # w2l_process.stdin.write(
#     #     b"output=/root/src/eagle_vnspeech2text/PVD/inference/out.txt\n")
#     # w2l_process.stdin.write(b"endtoken=DONE\n")
#     w2l_process.stdin.write(bytes("input="+path_to_audio_file+"\n", encoding='utf-8'))
#     w2l_process.stdin.flush()
#     while True:
#     #     # read from process stdout
#         output = w2l_process.stdout.readline()
#         if b'#finish transcribing\n' in output:
#     #         # finish transcribing an audio
#             print("FINISHING")
#             break
#         else:
#             output = output.decode('utf-8')
#             output = output.split(",")[-1].replace("\n","")
#             print(output)
# # finish the process
# os.killpg(os.getpgid(w2l_process.pid), signal.SIGTERM)

@app.route('/')
def move_to_model():
    filepath = request.args.get('filepath')
    if filepath is not None:
        return w2l.process_file(filepath)
    return  "file path is not exists"

@app.route('/kill')
def kill():
    w2l.kill_process()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5001")

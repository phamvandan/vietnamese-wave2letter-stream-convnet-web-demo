#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial

from flask import Flask, flash, redirect
from flask import request, jsonify
from flask import render_template, session
import os, shutil
from service import w2l

app = Flask(__name__)
app.secret_key = "abc_xyz"
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/static/audios/'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])

@app.route("/", methods=['POST', 'GET'])
def home():
    return render_template("login.html")


@app.route("/init_and_redirect", methods=['POST', 'GET'])
def init_and_redirect():
    session["upload_folder"] = os.path.join(app.config['UPLOAD_FOLDER'], request.args["user_name"])
    session["save_index"] = 1
    if os.path.exists(session["upload_folder"]):
        shutil.rmtree(session["upload_folder"])
    os.mkdir(session["upload_folder"])
    return redirect("/upload_file", )

@app.route("/upload_file", methods=['POST', 'GET'])
def upload_file():
    return render_template("upload.html")

from pydub import AudioSegment

def convert_to_wav(filepath):
    print("converting....")
    new_name = filepath.split(".")[0]+"_.wav"
    wav_file = AudioSegment.from_file(file=filepath)
    wav_file = wav_file.set_frame_rate(16000)
    wav_file = wav_file.set_sample_width(2)
    wav_file = wav_file.set_channels(1)
    wav_file.export(new_name, bitrate="256", format='wav')
    print(" end")
    return new_name

@app.route("/save_file_from_upload", methods=['POST'])
def save_file_from_upload():
    if 'filename' not in request.files:
        flash('No file part')
        return "error"
    file = request.files['filename']
    path_to_file = os.path.join(session["upload_folder"], file.filename)
    if ".wav" not in file.filename and ".flac" not in file.filename and ".mp3" not in file.filename:
        return "error"
    file.save(path_to_file)
    text = ""
    new_name = convert_to_wav(path_to_file)
    os.remove(path_to_file)
    path_to_file = new_name
    text = w2l.process_file(path_to_file)
    #os.remove(path_to_file)
    return text

@app.route("/record_audio", methods=['POST', 'GET'])
def record_audio():
    return render_template("my_record.html")

import time
@app.route("/speech_to_text", methods=['GET'])
def speech_to_text():
    # time.sleep(1)
    print("Processing...")
    path_to_file = os.path.join(session["upload_folder"], str(session["save_index"]) + ".wav")
    text = w2l.process_file(path_to_file)
    session["save_index"] = session["save_index"] + 1
    print("done processing", path_to_file)
    return text

@app.route("/save_audios", methods=['POST'])
def save_audios():
    if request.method == 'POST':
        files = request.files.getlist('audio_data')
        if files.count == 0:
            flash('No file selected for uploading')
            return redirect(request.url)
        else:
            text = ""
            for file in files:
                if file:
                    path_to_file = os.path.join(session["upload_folder"], str(session["save_index"]) + ".wav")
                    file.save(path_to_file)
                    print("Saved", path_to_file)
            return text


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5001, ssl_context=('cert.pem', 'key.pem'))
    # app.run(host="0.0.0.0", port=5001)


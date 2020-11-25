import os
import re
import time
import flask
import requests
from flask import flash, request, redirect, render_template, \
    send_from_directory, jsonify
from werkzeug.utils import secure_filename
from connect_database import get_all_sentences

app = flask.Flask(__name__)

app.secret_key = "colect_data"
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/static/audios'
app.config['MAX_CONTENT_LENGTH'] = 20000 * 1024 * 1024

@app.route('/get_ids', methods=['GET'])
def get_ids():
    temp = []
    dict_sentences = get_all_sentences()
    for dict_sentence in dict_sentences:
        temp_id = {}
        temp_id["id"] = dict_sentence["id"]
        temp.append(temp_id)
    return jsonify(temp)
@app.route('/get_sentence', methods=['POST'])
def get_sentence():
    sentence = None
    id = request.form["id"]
    dict_sentences = get_all_sentences()
    for dict_sentence in dict_sentences:
        if int(id) == int(dict_sentence["id"]):
            sentence = dict_sentence["sentence"]
            break
    return jsonify({"sentence":sentence})
@app.route('/upload_audios', methods=['POST'])
def upload_files():
    if request.method == 'POST':
        files = request.files.getlist('file')
        if files.count == 0:
            flash('No file selected for uploading')
            return redirect(request.url)
        else:
            time_upload = time.time()
            time_upload = time.localtime(time_upload)
            time_name = time.strftime("%Y%m%d%H%M", time_upload)
            folder_upload = os.path.join(str(app.config['UPLOAD_FOLDER']), time_name)
            if not os.path.exists(folder_upload):
                os.mkdir(folder_upload)
            file_names = []
            for file in files:
                if file:
                    filename = secure_filename(file.filename)
                    path_to_file = os.path.join(folder_upload, filename)
                    file.save(path_to_file)
                    file_names.append(filename)
            return jsonify({"upload":"Success"})
if __name__ == '__main__':
    app.run(host='0.0.0.0')
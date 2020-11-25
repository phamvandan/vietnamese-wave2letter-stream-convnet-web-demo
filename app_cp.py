#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from flask import Flask, flash, redirect
from flask import request, jsonify
from flask import render_template
from werkzeug.utils import secure_filename

from connect_database import get_all_sentences
import os
import re

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.getcwd() + '/static/audios'
#
# # for mobile call APIs
# @app.route('/get_ids', methods=['GET'])
# def get_ids():
#     temp = []
#     dict_sentences = get_all_sentences()
#     for dict_sentence in dict_sentences:
#         temp_id = {}
#         temp_id["id"] = dict_sentence["id"]
#         temp.append(temp_id)
#     return jsonify(temp)
# @app.route('/get_sentence', methods=['POST'])
# def get_sentence():
#     sentence = None
#     id = request.form["id"]
#     dict_sentences = get_all_sentences()
#     for dict_sentence in dict_sentences:
#         if int(id) == int(dict_sentence["id"]):
#             sentence = dict_sentence["sentence"]
#             break
#     return jsonify({"sentence":sentence})
# @app.route('/upload_audios', methods=['POST'])
# def upload_files():
#     if request.method == 'POST':
#         files = request.files.getlist('file')
#         if files.count == 0:
#             flash('No file selected for uploading')
#             return redirect(request.url)
#         else:
#             time_upload = time.time()
#             time_upload = time.localtime(time_upload)
#             time_name = time.strftime("%Y%m%d%H%M", time_upload)
#             folder_upload = os.path.join(str(app.config['UPLOAD_FOLDER']), time_name)
#             if not os.path.exists(folder_upload):
#                 os.mkdir(folder_upload)
#             file_names = []
#             for file in files:
#                 if file:
#                     filename = secure_filename(file.filename)
#                     path_to_file = os.path.join(folder_upload, filename)
#                     file.save(path_to_file)
#                     file_names.append(filename)
#             return jsonify({"upload":"Success"})


dict_sentences = get_all_sentences()
with open("id.txt", "r") as f_id:
    cur_id = int(f_id.read())


# for web view
@app.route("/", methods=['POST', 'GET'])
def index():
    # temp_id = []
    # for dict_sentence in dict_sentences:
    #     temp_id.append(dict_sentence["id"])
    # return render_template("login.html", list_id=temp_id)
    return render_template("my_record.html")


@app.route("/record", methods=['GET'])
def record():
    global cur_id, dict_sentences
    user_name = request.args.get("user_name")
    user_name = "".join(re.findall("[a-zA-Z]+", user_name))
    # print(user_name)
    id_1 = cur_id
    id_2 = cur_id + 9
    cur_id = cur_id + 10
    if cur_id > len(dict_sentences) - 1:
        cur_id = 0
    with open("id.txt", "w+") as f_out:
        f_out.write(str(cur_id))
    # id_2 = int(request.args.get("id_2"))
    # if id_2 < id_1:
    #     id_1, id_2 = id_2, id_1
    # id_sentence = {}
    id = []
    sentence = []
    for dict_sentence in dict_sentences:
        if id_1 <= dict_sentence["id"] <= id_2:
            id.append(dict_sentence["id"])
            sentence.append(dict_sentence["sentence"])
            # id_sentence[dict_sentence["id"]] = dict_sentence["sentence"]
    # print(id_sentence)
    return render_template("record.html", user_name=user_name, id=id, sentence=sentence, number_id=len(id))


@app.route("/save_audios", methods=['POST'])
def save_audios():
    if request.method == 'POST':
        time_upload = time.time()
        time_upload = time.localtime(time_upload)
        time_name = time.strftime("%Y%m%d%H%M", time_upload)
        folder_upload = os.path.join(str(app.config['UPLOAD_FOLDER']))
        # folder_upload = os.path.join(str(app.config['UPLOAD_FOLDER']),
        #                              time_name)
        # if not os.path.exists(folder_upload):
        #     os.mkdir(folder_upload)
        files = request.files.getlist('audio_data')
        if files.count == 0:
            flash('No file selected for uploading')
            return redirect(request.url)
        else:
            # file_names = []
            for file in files:
                if file:
                    # filename = secure_filename(file.filename)
                    path_to_file = os.path.join(folder_upload, time_name + file.filename)
                    # print(path_to_file)
                    file.save(path_to_file)
                    # file_names.append(filename)
                    print("save ok")
            return jsonify({"upload": "Success"})


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", ssl_context=('cert.pem', 'key.pem'))

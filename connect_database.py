# import pymysql.cursors
import json

def write_sentence(id, transcript):
    for i in id:
        with open("transcript.bin", "a+") as f:
            json.dump({"id":i, "transcript":transcript[i]}, f)
            f.write("\n")
# def get_all_sentences():
#     result = []
#     connection = pymysql.connect(host='localhost',
#                                  user='root',
#                                  password='45rtfgvb',
#                                  db='transcript_collection',
#                                  charset='utf8',
#                                  cursorclass=pymysql.cursors.DictCursor)
#     try:
#         with connection.cursor() as cursor:
#             sql = "SELECT * FROM sentences "
#             cursor.execute(sql)
#             for row in cursor:
#                 dict_sentences = {}
#                 dict_sentences["id"] = row['id']
#                 dict_sentences["sentence"] = row['script']
#                 result.append(dict_sentences)
#                 # dict_sentences[row['id']] = row['script']
#                 # id.append(int(row['id']))
#     finally:
#         connection.close()
#     return result

def get_all_sentences():
    result = []
    with open("transcript.bin", "r") as f:
        lines = f.readlines()
        for line in lines:
            dict_sentences = {}
            row = json.loads(line)
            dict_sentences["id"] = row['id']
            dict_sentences["sentence"] = row['transcript']
            result.append(dict_sentences)
            # dict_sentences[row['id']] = row['script']
            # id.append(int(row['id']))
    # print(result)
    return result
from random import shuffle

if __name__ == '__main__':
    # write_sentence()
    # get_all_sentences()
    with open("transcript.txt", "r") as f_in:
        sentences = f_in.readlines()
        index = [i for  i in range(0,len(sentences))]
        shuffle(index)
        for i in range(0, len(sentences)):
            with open("transcript.bin", "a+") as f:
                json.dump({"id": i, "transcript": sentences[index[i]], "status":"None"}, f)
                f.write("\n")
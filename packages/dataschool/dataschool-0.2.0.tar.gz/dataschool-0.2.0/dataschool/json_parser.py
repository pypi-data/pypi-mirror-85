import sys
import os
import json
import isodate as iso
import pandas as pds
import numpy as np
import datetime
import hashlib


###Function ton convert ISO 8601 to seconds
def convert_time(string):
    time = str(iso.parse_duration(string))
    h, m, s = time.split(':')
    sec = float(h) * 3600 + float(m) * 60 + float(s)
    return sec

def get_question_pos(cell):
    return cell["module"], cell["activity"], cell["exercice"], cell["grade"], cell["subject"], cell["path"]

def get_timestamp(date):
    time = str(iso.parse_datetime(date))
    day,hour = time.split(' ')
    hour,_ = hour.split('+')
    time = "{} {}".format(day, hour)
    return time

def clean_student_id(string):
    new_string = hashlib.sha256()
    new_string.update(string.encode())
    new_string = new_string.hexdigest()[:5]
    return new_string

def clean_question_id_adapt(cell):
    path = cell["path"]
    module = cell["module"]
    activity = cell["activity"]
    exercice = cell["exercice"]
    fmt = "[{},{},{},{}]".format(path, module, activity, exercice)
    return fmt

def clean_json_adapt(df):
    statement = df['statement']
    for i in range(len(statement)):
###Get rid of any statement that is not AdaptivLang
        if 'account' not in statement[i]['actor']:
            statement = statement.drop([i], axis=0)
        elif statement[i]['actor']['account']['homePage'] != "https://adaptivlang.evidenceb.com":
            statement = statement.drop([i], axis=0)
###Get rid of any statement that is not an answer to a question
        elif 'result' not in statement[i]:
            statement = statement.drop([i], axis=0)
    statement = statement.reset_index(drop=True)
    return statement

def parse_df_adapt(df):
    new_df = np.empty((len(df), 12), dtype=object)
###Fill array with the datas we want (student_id, question_id, duration, success)
    for i in range(len(df)):
        new_df[i][0] = clean_student_id(df[i]['actor']['account']['name'])
        new_df[i][1] = clean_question_id_adapt((df[i]["object"]["definition"]["extensions"]["https://xapi&46;evidenceb&46;com/object/details"]))
        new_df[i][2] = convert_time(df[i]['result']['duration'])
        new_df[i][3] = df[i]['result']['success']
        new_df[i][4], new_df[i][5], new_df[i][6], new_df[i][7], new_df[i][8], new_df[i][9] = get_question_pos(df[i]["object"]["definition"]["extensions"]["https://xapi&46;evidenceb&46;com/object/details"])
        new_df[i][10] = df[i]['object']['definition']['interactionType']
        new_df[i][11] = get_timestamp(df[i]['timestamp'])
###Turning the array into a Dataframe
    new_df = pds.DataFrame(new_df)
    new_df.columns = ['id_eleve', 'id_question', 'duree', 'correct', 'module', 'activity', 'exercice', 'grade', 'subject', 'path', 'interactionType', 'timestamp']
    pds.set_option("display.max_columns", None)
    return new_df

def total_parsing_adapt(df):
    clean_df = clean_json_adapt(df)
    parsed_df = parse_df_adapt(clean_df)
    return parsed_df

def clean_json_bordas(df):
    statement = df['statement']
    for i in range(len(statement)):
###Get rid of any statement that is not AdaptivLang
        if 'account' not in statement[i]['actor']:
            statement = statement.drop([i], axis=0)
        elif statement[i]['actor']['account']['homePage'] != "https://bordas-staging.netlify.app":
            statement = statement.drop([i], axis=0)
###Get rid of any statement that is not an answer to a question
        elif 'result' not in statement[i]:
            statement = statement.drop([i], axis=0)
    statement = statement.reset_index(drop=True)
    return statement

def parse_df_bordas(df):
    new_df = np.empty((len(df), 3), dtype=object)
    for i in range(len(df)):
        new_df[i][0] = df[i]['actor']['account']['name']
        new_df[i][1] = get_timestamp(df[i]['timestamp'])
        new_df[i][2] = df[i]['result']['success']
    new_df = pds.DataFrame(new_df)
    new_df.columns = ['id_eleve', 'timestamp', 'correct']
    pds.set_option("display.max_columns", None)
    return new_df

def total_parsing_bordas(df):
    clean_df = clean_json_bordas(df)
    parsed_df = parse_df_bordas(clean_df)
    return parsed_df

def main(argv):
    df = pds.read_json(argv[1])
    if len(argv) < 3:
        print("Error: Not enough arguments")
        exit(84)
    if argv[2] == "adaptivlang":
        parsed_df = total_parsing_adapt(df)
    elif argv[2] == "bordas":
        parsed_df = total_parsing_bordas(df)
    else:
        print("Error: Second argument must be \'adaptivlang\' or \'bordas\'")
        exit(84)
    print(parsed_df)
    return parsed_df

if __name__ == "__main__":
    main(sys.argv)
    pass
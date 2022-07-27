import json
import os
from typing import Union, List
from pprint import pprint
from random import randint
from datetime import datetime
from json import JSONDecodeError


def store_detected_events() -> None:
    default_lpr_values = {
        "Text": f'TEXT_{randint(100, 1000)}', "Confidence": f"{randint(50, 91)}%",
        "Center_X": "x", "Center_Y": "y", "width": randint(100, 501), "height": randint(100, 501),
        "DateTime": datetime.timestamp(datetime.now())}

    default_lpr_empty_values = {"Text": 'XXXXXX', "Confidence": "XXX", "Center_X": "x", "Center_Y": "y",
                                "width": 'X', "height": 'X', "DateTime": datetime.timestamp(datetime.now())}

    try:
        with open('alpr_raw_detect.json') as alpr_file:
            export_dict = json.load(alpr_file)

            if "LPR_Events" not in export_dict['Export'].keys():
                print("no such key, inserting a new key..")
                export_dict['Export']['LPR_Events'] = list()
                export_dict['Export']['LPR_Events'].append(dict(default_lpr_values))
                pprint(export_dict)

            else:               # if already present
                export_dict['Export']['LPR_Events'].append(dict(default_lpr_empty_values))

            with open('alpr_raw_detect.json', 'w') as json_file:
                json.dump(export_dict, json_file)

    except JSONDecodeError as e:
        print(e.msg)


def store_detected_events_2(result_dict):
    detected_lpr_values = result_dict  # this list will hold only the texts present in each dict of the lpr-event key.
    try:
        with open('alpr_raw_detect_2.json') as alpr_file:
            export_dict = json.load(alpr_file)

            if "LPR_Events" not in export_dict['Export'].keys():
                print("no such key, inserting a new key..")
                export_dict['Export']['LPR_Events'] = list()
                export_dict['Export']['LPR_Events'].append(dict(detected_lpr_values))
                # pprint(export_dict)

            else:               # if already present
                texts_present_list = []
                LPR_Events = export_dict["Export"]["LPR_Events"]
                for i in range(len(LPR_Events)):
                    unique_text = LPR_Events[i].get('Text')
                    texts_present_list.append(unique_text)
                texts_present_set = set(texts_present_list)
                if detected_lpr_values.get('Text') in texts_present_set:
                    print('Duplicate text detected, cannot insert value.')
                else:
                    print('appending new value...')
                    export_dict['Export']['LPR_Events'].append(dict(detected_lpr_values))
                    print('value appended')

            with open('alpr_raw_detect_2.json', 'w') as json_file:
                json.dump(export_dict, json_file)

    except JSONDecodeError as e:
        print(e.msg)


def store_detected_events_2_backup(result_dict):
    detected_lpr_values = result_dict
    try:
        with open('alpr_raw_detect_2.json') as alpr_file:
            export_dict = json.load(alpr_file)

            if "LPR_Events" not in export_dict['Export'].keys():
                print("no such key, inserting a new key..")
                export_dict['Export']['LPR_Events'] = list()
                export_dict['Export']['LPR_Events'].append(dict(detected_lpr_values))
                # pprint(export_dict)

            else:               # if already present
                texts_present_list = []  # this list will hold only the texts present in each dict of the lpr-event key.
                LPR_Events = export_dict["Export"]["LPR_Events"]
                for i in range(len(LPR_Events)):
                    unique_text = LPR_Events[i].get('Text')
                    texts_present_list.append(unique_text)
                texts_present_set = set(texts_present_list)

                # for i in range(len(export_dict["Export"]["LPR_Events"])):
                #     for key, val in export_dict["Export"]["LPR_Events"][i].items():
                #         if key == 'Text':
                #             texts_present_list.append(val)

                if detected_lpr_values.get('Text') in texts_present_set:
                    print('Duplicate text detected, cannot insert value.')
                else:
                    print('appending new value...')
                    export_dict['Export']['LPR_Events'].append(dict(detected_lpr_values))
                    print('value appended')

            with open('alpr_raw_detect_2.json', 'w') as json_file:
                json.dump(export_dict, json_file)

    except JSONDecodeError as e:
        print(e.msg)


def store_detected_events_3(result_dict):
    '''This function will only store contents of Scene 3'''
    detected_lpr_values = result_dict
    try:
        with open("scenes_json/Scene_3.json") as alpr_file:
            export_dict = json.load(alpr_file)

            if "LPR_Events" not in export_dict['Export'].keys():
                print("no such key, inserting a new key..")
                export_dict['Export']['LPR_Events'] = list()
                export_dict['Export']['LPR_Events'].append(dict(detected_lpr_values))
                # pprint(export_dict)

            else:               # if already present
                export_dict['Export']['LPR_Events'].append(dict(detected_lpr_values))

            with open("scenes_json/Scene_3.json", 'w') as json_file:
                json.dump(export_dict, json_file)

    except JSONDecodeError as e:
        print(e.msg)

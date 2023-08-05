#! /usr/local/python
# -*- coding: UTF-8 -*-

"""
Dado un archivo con las transcripciones obtenidas del corpus, se generan las transcripciones para el entrenamiento y
pruebas, junto con su archivo de nombres
"""
import os
import codecs
import random
from openspeechcorpus_cli.utils.common_filters import *


def remove_extensions(word):
    if "3gp" in word:
        return word.replace(".3gp", "_3gp")
    elif "mp4" in word:
        return word.replace(".mp4", "")
    return word


def execute_script(etc_folder_name, name, transcription_file, test_samples_coefficient, ignore_wav_missing=False):

    transcription_full_file = os.path.join(etc_folder_name, "{}.transcription".format(name))
    train_file = os.path.join(etc_folder_name, "{}_train.transcription".format(name))
    test_file = os.path.join(etc_folder_name, "{}_test.transcription".format(name))
    transcription_file_ids = os.path.join(etc_folder_name, "{}.fileids".format(name))
    train_file_ids = os.path.join(etc_folder_name, "{}_train.fileids".format(name))
    test_file_ids = os.path.join(etc_folder_name, "{}_test.fileids".format(name))

    f = codecs.open(transcription_file, "rb", encoding="UTF-8")
    lines = f.readlines()

    o_transcription_file = codecs.open(transcription_full_file, 'w+', encoding="UTF-8")
    o_train_file = codecs.open(train_file, 'w+', encoding="UTF-8")
    o_test_file = codecs.open(test_file, 'w+', encoding="UTF-8")
    o_transcription_file_ids = codecs.open(transcription_file_ids, 'w+', encoding="UTF-8")
    o_train_file_ids = codecs.open(train_file_ids, 'w+', encoding="UTF-8")
    o_test_file_ids = codecs.open(test_file_ids, 'w+', encoding="UTF-8")

    # TODO: delete or add an extra argument to manage this
    # ########## PATCH
    # corrupted_files_file = codecs.open("corrupted_files.txt", "rb", encoding="UTF-8")
    # corrupted_files = corrupted_files_file.read()
    # ######### End of PATCH
    for line in lines:

        file_name, raw_trasncription = line.lower().split(",")

        # ########## PATCH
        # if file_name.split("/")[1].replace(".mp4", "") in corrupted_files:
        #    print("Skiping file {}".format(file_name))
        #    continue
        # ######### End of PATCH

        line_transcription_content = "<s> {} </s>".format(
            allow_characters(
                filter_special_characters(
                    clean_accents(
                        remove_jump_characters(
                            raw_trasncription.lower()
                        )
                    )
                )
            )
        )
        line_id_content = "{}".format(
            remove_jump_characters(
                remove_extensions(
                    file_name
                )
            )
        )

        transcription_plus_id = "{} ({})\n".format(line_transcription_content, line_id_content)
        if ignore_wav_missing:
            path_to_check = os.path.join(etc_folder_name, "../wav/", "{}.wav".format(line_id_content))
            if not os.path.exists(path_to_check):
                print("Path {} Does not exits, skipping".format(path_to_check))
                continue
        line_id_content = "{}\n".format(line_id_content)
        line_transcription_content = "{}\n".format(line_transcription_content)

        o_transcription_file.write(line_transcription_content)
        o_transcription_file_ids.write(line_id_content)

        value = random.random()
        if value < test_samples_coefficient:
            o_test_file.write(transcription_plus_id)
            o_test_file_ids.write(line_id_content)
        else:
            o_train_file.write(transcription_plus_id)
            o_train_file_ids.write(line_id_content)

    o_train_file.close()
    o_test_file_ids.close()
    o_test_file.close()
    o_train_file_ids.close()


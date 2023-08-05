#!/usr/bin/env python

import os
import argparse

from openspeechcorpus_cli.utils import execute_script_with_args_if_file_does_not_exists


from openspeechcorpus_cli.htk import (
    generate_isolated_words_grammar,
    generate_list_words,
    generate_phone_level_master_labeled_file,
    generate_config_file,
    generate_features_map_file,
    generate_prototype,
    generate_list_phonemes,
    generate_dict,
    generate_word_level_master_labeled_file
)


def execute_from_command_line():
    parser = argparse.ArgumentParser(
        "Configure HTK configuration files"
    )

    parser.add_argument(
        "project_name",
        help="Name of the HTK project"
    )

    parser.add_argument(
        "--transcription_file",
        default="transcription.txt",
        help="Name of the transcription file, this file must be a file where each line contains the relative path to a"
             "recording and the transcription of that recording, the separation for the two args must be a comma"
    )

    parser.add_argument(
        "--project_folder",
        default="htk_config",
        help="Configuration folder for htk"
    )

    parser.add_argument(
        "--wav_folder",
        default="wav",
        help="wav folder for with audios"
    )

    args = vars(parser.parse_args())

    project_name = args["project_name"]
    transcript_file = args["transcription_file"]
    project_folder_name = args["project_folder"]
    wav_folder = args["wav_folder"]

    # Configuration Folder
    if not os.path.exists(project_folder_name):
        print("Creating project folder")
        os.makedirs(project_folder_name)
        print("project folder created")
    else:
        print("Project folder already created, skipping")

    # Word list
    words_list_path = os.path.join(project_folder_name, f"{project_name}.words_sorted.list")
    execute_script_with_args_if_file_does_not_exists(
        generate_list_words.execute_script,
        words_list_path,
        transcript_file,
        words_list_path,
    )
    # phoneme list
    phonemes_list_path = os.path.join(project_folder_name, f"{project_name}.phonemes_sorted.list")
    execute_script_with_args_if_file_does_not_exists(
        generate_list_phonemes.execute_script,
        phonemes_list_path,
        transcript_file,
        phonemes_list_path,
    )

    # dict
    dict_list_path = os.path.join(project_folder_name, f"{project_name}.dict")
    execute_script_with_args_if_file_does_not_exists(
        generate_dict.execute_script,
        dict_list_path,
        transcript_file,
        dict_list_path,
    )

    # Single word grammar
    words_grammar_path = os.path.join(project_folder_name, f"{project_name}.words_grammar")
    execute_script_with_args_if_file_does_not_exists(
        generate_isolated_words_grammar.execute_script,
        words_grammar_path,
        transcript_file,
        words_grammar_path,
    )

    # MLF
    master_label_file_path = os.path.join(project_folder_name, f"{project_name}.mlf")
    execute_script_with_args_if_file_does_not_exists(
        generate_phone_level_master_labeled_file.execute_script,
        master_label_file_path,
        transcript_file,
        master_label_file_path,
    )
    master_word_label_file_path = os.path.join(project_folder_name, f"{project_name}.word.mlf")
    execute_script_with_args_if_file_does_not_exists(
        generate_word_level_master_labeled_file.execute_script,
        master_word_label_file_path,
        transcript_file,
        master_word_label_file_path,
    )
    # config
    config_file_path = os.path.join(project_folder_name, f"config")
    execute_script_with_args_if_file_does_not_exists(
        generate_config_file.execute_script,
        config_file_path,
        config_file_path
    )

    # codetr
    codectr_file_path = os.path.join(project_folder_name, f"codetr.scp")
    execute_script_with_args_if_file_does_not_exists(
        generate_features_map_file.execute_script,
        codectr_file_path,
        transcript_file,
        codectr_file_path,
        wav_folder,
        project_folder_name
    )

    # train
    train_file_path = os.path.join(project_folder_name, f"train.scp")
    execute_script_with_args_if_file_does_not_exists(
        generate_features_map_file.execute_script,
        train_file_path,
        transcript_file,
        train_file_path,
        wav_folder,
        project_folder_name,
        False
    )

    # proto
    proto_file_path = os.path.join(project_folder_name, f"proto")
    execute_script_with_args_if_file_does_not_exists(
        generate_prototype.execute_script,
        proto_file_path,
        proto_file_path,
    )

    # config
    config_with_deltas_file_path = os.path.join(project_folder_name, f"config.deltas")
    execute_script_with_args_if_file_does_not_exists(
        generate_config_file.execute_script,
        config_with_deltas_file_path,
        config_with_deltas_file_path,
        source_format="HTK",
        target_kind="MFCC_0_D_A"
    )

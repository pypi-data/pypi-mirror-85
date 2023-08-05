#!/usr/bin/env python

import os
import argparse

from openspeechcorpus_cli.utils import execute_script_with_args_if_file_does_not_exists

from openspeechcorpus_cli.cmu_sphinx import (
    generate_dict,
    generate_phone_set_from_dict,
    generate_filler,
    generate_transcriptions,
)


def execute_from_command_line():
    parser = argparse.ArgumentParser(
        "Configure sphinxtrain transcription files"
    )

    parser.add_argument(
        "project_name",
        help="Name of the sphinxtrain project"
    )

    parser.add_argument(
        "--transcription_file",
        default="transcription.txt",
        help="Name of the transcription file, this file must be a file where each line contains the relative path to a"
             "recording and the transcription of that recording, the separation for the two args must be a comma"
    )

    parser.add_argument(
        "--etc_folder",
        default="etc",
        help="etc folder for Sphinx train"
    )

    parser.add_argument(
        "--test_size",
        type=float,
        default=0.3
    )

    parser.add_argument(
        "--ignore_wav_missing",
        action="store_true",
        help="In case you have already the wav folder populated for CMU Sphinx Train, this flag ensures all the fileids"
             "in the transcriptions files effectively exists."
    )

    args = vars(parser.parse_args())

    project_name = args["project_name"]
    transcript_file = args["transcription_file"]
    etc_folder_name = args["etc_folder"]
    test_size = args["test_size"]
    ignore_wav_missing = args.get("ignore_wav_missing", False)
    # Configuration Folder
    if not os.path.exists(etc_folder_name):
        print("Creating etc folder")
        os.makedirs(etc_folder_name)
        print("etc folder created")

    # Dictionary file
    dict_file = os.path.join(etc_folder_name, "{}.dic".format(project_name))
    execute_script_with_args_if_file_does_not_exists(
        generate_dict.execute_script,
        dict_file,
        transcript_file,
        dict_file
    )
    # Phone file
    phone_file = os.path.join(etc_folder_name, "{}.phone".format(project_name))
    execute_script_with_args_if_file_does_not_exists(
        generate_phone_set_from_dict.execute_script,
        phone_file,
        dict_file,
        phone_file
    )

    # Filler file
    filler_file = os.path.join(etc_folder_name, "{}.filler".format(project_name))
    execute_script_with_args_if_file_does_not_exists(
        generate_filler.execute_script,
        filler_file,
        filler_file,
    )

    # Transcriptions file
    fileids_file = os.path.join(etc_folder_name, "{}.fileids".format(project_name))
    execute_script_with_args_if_file_does_not_exists(
        generate_transcriptions.execute_script,
        fileids_file,
        etc_folder_name,
        project_name,
        transcript_file,
        test_size,
        ignore_wav_missing
    )

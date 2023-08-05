#!/usr/bin/env python

import os
import argparse

from openspeechcorpus_cli.utils.common_filters import remove_jump_characters


def execute_from_command_line():
    parser = argparse.ArgumentParser(
        "Configure HTK Flat Start"
    )

    parser.add_argument(
        "phone_list_file",
        help="Phone list name"
    )

    parser.add_argument(
        "--proto_file",
        default="./hmm0/proto"
    )

    parser.add_argument(
        "--var_floor_file",
        default="./hmm0/vFloors"
    )

    parser.add_argument(
        "--hmmdefs_output_file",
        default="./hmm0/hmmdefs"
    )
    parser.add_argument(
        "--macros_output_file",
        default="./hmm0/macros"
    )
    parser.add_argument(
        "--vector_size",
        default=39
    )
    parser.add_argument(
        "--vector_type",
        default="MFCC_0_D_A"
    )

    args = vars(parser.parse_args())

    phone_list_file = args['phone_list_file']
    proto_file = args['proto_file']
    var_floor_file = args['var_floor_file']
    hmmdefs_output_file = args['hmmdefs_output_file']
    macros_output_file = args['macros_output_file']
    vector_size = args['vector_size']
    vector_type = args['vector_type']

    # Readphones
    with open(phone_list_file) as phones_file:
        phones_list = phones_file.readlines()
    # Readphones
    with open(proto_file) as proto_file:
        proto_file_content = proto_file.readlines()
    # Readphones
    with open(var_floor_file) as var_file:
        var_file_content = var_file.readlines()

    if "sil" not in phones_list:
        phones_list.append("sil")

    hmmdefs = list()
    for phone in phones_list:
        hmmdefs.append(f'~h "{remove_jump_characters(phone)}"\n')
        hmmdefs.extend(proto_file_content[4:])
    with open(hmmdefs_output_file, 'w+') as hmmdefs_file:
        hmmdefs_file.writelines(hmmdefs)
    with open(macros_output_file, 'w+') as macros_file:
        macros_file.writelines(
            [
                "~o\n",
                f"<VecSize> {vector_size}\n",
                f"<{vector_type}>\n"
            ])
        macros_file.writelines(var_file_content)


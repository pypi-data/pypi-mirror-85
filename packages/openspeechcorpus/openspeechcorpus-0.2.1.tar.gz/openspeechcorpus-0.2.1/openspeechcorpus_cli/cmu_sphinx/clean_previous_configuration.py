import argparse
import os
FILES_CREATED = [
    "{}_test.fileids",
    "{}_test.transcription",
    "{}_train.fileids",
    "{}_train.transcription",
    "{}.dic",
    "{}.fileids",
    "{}.filler",
    "{}.phone",
    "{}.transcription",
    "{}.idngram",
    "{}.lm",
    "{}.lm.DMP",
    "{}.phone",
    "{}.vocab",
]


def clean_sphinx_configuration(etc_folder, project_name):
    for file in FILES_CREATED:
        file_to_delete = os.path.join(etc_folder, file.format(project_name))
        if os.path.exists(file_to_delete):
            print("Deleting {}".format(file_to_delete))
            os.remove(file_to_delete)
        else:
            print("File {} Does not exists, skipping".format(file_to_delete))


def execute_from_command_line():
    parser = argparse.ArgumentParser(
        "Deletes all files created by the configure_sphinx command"
    )

    parser.add_argument(
        "project_name",
        help="Name of the sphinxtrain project"
    )

    parser.add_argument(
        "--etc_folder",
        default="etc",
        help="etc folder for Sphinx train"
    )

    args = vars(parser.parse_args())

    clean_sphinx_configuration(args["etc_folder"], args["project_name"])

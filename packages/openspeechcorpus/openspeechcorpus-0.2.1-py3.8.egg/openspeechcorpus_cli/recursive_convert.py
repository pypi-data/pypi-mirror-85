import os
import argparse


def recursive_convert(path, root_dir, output_folder_path):
    new_path = os.path.join(root_dir, path)
    convert_new_path = os.path.join(output_folder_path, new_path)
    print(new_path)
    if os.path.isdir(new_path):
        if not os.path.exists(convert_new_path):
            os.makedirs(convert_new_path)
        dirs = os.listdir(new_path)
        for directory in dirs:
            recursive_convert(directory, os.path.join(root_dir, path), output_folder_path)
    else:
        print(new_path)
        if "3gp" in path:
            if not os.path.exists(convert_new_path.replace(".3gp", "_3gp.wav")):
                os.popen(
                    "ffmpeg -i %s -qscale 0 -ab 64k -ar 16000 %s" %
                    (
                        new_path,
                        convert_new_path.replace(".3gp", "_3gp.wav")
                    )
                )
            else:
                print("File already converted")
        elif "mp4" in path:
            if not os.path.exists(convert_new_path.replace(".mp4", ".wav")):
                os.popen(
                    "ffmpeg -i %s -qscale 0 -ab 64k -ar 16000 %s" %
                    (
                        new_path,
                        convert_new_path.replace(".mp4", ".wav")
                    )
                )
            else:
                print("File already converted")


def execute_from_command_line():
    parser = argparse.ArgumentParser(
        "Recursive convert mp4 files to wav"
    )

    parser.add_argument(
        "input_folder",
        help="Input folder with mp4 files"
    )

    parser.add_argument(
        "output_folder",
        help="Output folder "
    )

    args = vars(parser.parse_args())
    if not os.path.exists(args["output_folder"]):
        print("Output folder does not exists")
        print("force_create flag detected, creating {}".format(args["output_folder"]))
        os.mkdir(args["output_folder"])
    recursive_convert("", args["input_folder"], args["output_folder"])

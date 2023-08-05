import os

from openspeechcorpus_cli.utils import get_all_file_names_and_relative_paths


def execute_script(
        transcription_file,
        output_file,
        wav_folder,
        output_folder,
        include_source=True,
        verify_existing=True,
        extension='mfc',
):
    relative_paths = get_all_file_names_and_relative_paths(transcription_file)
    lines = list()
    for record in relative_paths:
        if record.endswith(".mp4"):
            record = record.replace(".mp4", ".wav")
        absolute_record_path = os.path.join(os.path.abspath(wav_folder), record)
        if verify_existing:
            if not os.path.exists(absolute_record_path):
                print(f"File {record} not found in {wav_folder}, skipping")
                continue
        relative_folders = record.split("/")
        relative_path_without_file = "/".join(relative_folders[:-1])
        new_file_name = f"{'.'.join(relative_folders[-1].split('.')[:-1])}.{extension}"
        features_path = os.path.join(
            os.path.abspath(output_folder),
            "features",
            relative_path_without_file,
            new_file_name
        )
        if include_source:
            lines.append(f"{absolute_record_path} {features_path}\n")
        else:
            lines.append(f"{features_path}\n")
    output_file = open(output_file, 'w+')
    output_file.writelines(lines, )
    output_file.close()

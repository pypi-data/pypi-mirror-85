

def get_all_text_transcriptions(transcription_file):
    with open(transcription_file, encoding='UTF-8') as file:
        lines = file.readlines()
        return [" ".join(line.split(",")[1:]).lower() for line in lines if line.replace(" ", "")]


def get_all_text_transcriptions_with_file_name(transcription_file):
    with open(transcription_file, encoding='UTF-8') as file:
        lines = file.readlines()
        return [
            (
                line.split(",")[0].split("/")[-1].split(".")[0],
                " ".join(line.split(",")[1:]).lower())
            for line in lines if line.replace(" ", "")
        ]


def get_all_file_names_and_relative_paths(transcription_file):
    with open(transcription_file, encoding='UTF-8') as file:
        lines = file.readlines()
        return [line.split(",")[0] for line in lines if line.replace(" ", "")]

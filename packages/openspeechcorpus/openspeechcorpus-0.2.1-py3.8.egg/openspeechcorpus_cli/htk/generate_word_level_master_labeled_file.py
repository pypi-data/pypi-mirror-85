from openspeechcorpus_cli.utils import get_all_text_transcriptions_with_file_name
from openspeechcorpus_cli.utils.common_filters import extract_phones_from_word, apply_filters


def execute_script(transcription_file, output_file, phonetic_annotator=extract_phones_from_word):
    transcriptions = get_all_text_transcriptions_with_file_name(transcription_file)
    output_file = open(output_file, 'w+')
    output_file.write("#!MLF!#\n")
    for file_name, transcription in transcriptions:
        output_file.write(f'"*/{file_name}.lab"\n')
        output_file.write("sil\n")
        for word in transcription.split():
            word = apply_filters(word)
            output_file.write(f"{word}\n")
        output_file.write("sil\n")
        output_file.write(".\n")

    output_file.close()


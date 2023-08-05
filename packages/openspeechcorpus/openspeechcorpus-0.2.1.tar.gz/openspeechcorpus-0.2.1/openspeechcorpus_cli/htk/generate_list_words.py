import re
from openspeechcorpus_cli.utils import get_all_text_transcriptions
from openspeechcorpus_cli.utils.common_filters import STOP_SYMBOLS, apply_filters


def execute_script(transcription_file, output_file):
    transcriptions = get_all_text_transcriptions(transcription_file)
    unique_words = set()
    for transcription in transcriptions:
        unique_words.update(map(apply_filters, re.split(STOP_SYMBOLS, transcription)))

    output_file = open(output_file, 'w+', encoding='UTF-8')
    word_list = '\n'.join(sorted(unique_words))
    output_file.write(word_list)
    output_file.write('\n')
    output_file.close()


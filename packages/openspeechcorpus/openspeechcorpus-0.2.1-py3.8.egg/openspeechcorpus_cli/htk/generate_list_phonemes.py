import re

from openspeechcorpus_cli.utils import get_all_text_transcriptions
from openspeechcorpus_cli.utils.common_filters import STOP_SYMBOLS, extract_phones_from_word


def execute_script(transcription_file, output_file, phonetic_annotator=extract_phones_from_word):
    transcriptions = get_all_text_transcriptions(transcription_file)
    unique_phonemes = set()
    for transcription in transcriptions:
        for word_in_transcription in re.split(STOP_SYMBOLS, transcription):
            for phoneme in phonetic_annotator(word_in_transcription):
                if phoneme.replace(" ", ""):
                    unique_phonemes.add(phoneme)

    output_file = open(output_file, 'w+')
    word_list = '\n'.join(sorted(unique_phonemes))
    output_file.write(word_list)

    output_file.close()


import re
from openspeechcorpus_cli.utils import get_all_text_transcriptions
from openspeechcorpus_cli.utils.common_filters import STOP_SYMBOLS, extract_phones_from_word, apply_filters


def execute_script(transcription_file, output_file, phonetic_annotator=extract_phones_from_word):
    transcriptions = get_all_text_transcriptions(transcription_file)
    unique_words = set()
    word_transcription = list()
    for transcription in transcriptions:
        for word in re.split(STOP_SYMBOLS, transcription):
            word = apply_filters(word)
            if word.replace(" ", "") and word not in unique_words:
                unique_words.add(word)
                word_transcription.append(f"{word}  {phonetic_annotator(word)}")

    output_file = open(output_file, 'w+', encoding='UTF-8')
    word_list = '\n'.join(sorted(word_transcription)).encode("UTF-8").decode("UTF-8")
    output_file.write(word_list)

    output_file.close()


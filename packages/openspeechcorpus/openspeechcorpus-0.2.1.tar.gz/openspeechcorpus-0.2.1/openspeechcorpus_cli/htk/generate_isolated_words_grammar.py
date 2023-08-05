import re
from openspeechcorpus_cli.utils import get_all_text_transcriptions
from openspeechcorpus_cli.utils.common_filters import STOP_SYMBOLS


def execute_script(transcription_file, output_file):
    transcriptions = get_all_text_transcriptions(transcription_file)
    unique_words = set()
    for transcription in transcriptions:
        unique_words.update(list(re.split(STOP_SYMBOLS, transcription)))

    output_file = open(output_file, 'w+')

    output_file.write(f"""$word = {" | ".join(unique_words)}
    ( SENT-START ( <{{SIL}} $word {{SIL}}> ) SENT-END )
    """)

    output_file.close()


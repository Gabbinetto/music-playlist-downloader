import unicodedata
import re
from youtube_transcript_api import YouTubeTranscriptApi


def caption_string(video_id):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    # ―

    output = []

    for transcript in transcript_list:
        output.append(transcript.language)

        data = transcript.fetch()
        consecutive_lines = 1

        for i in data:
            line = i["text"].replace("\u200b", "").strip(" ")

            if output[-1] == line:
                consecutive_lines += 1
                output[-1] = line + " x" + str(consecutive_lines)
            else:
                output.append(line)
                consecutive_lines = 1
        
        output.append("―" * 40)
    
    return "\n".join(output)


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

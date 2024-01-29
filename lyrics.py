from langdetect import detect, LangDetectException

def clean_lyrics(lyrics: str) -> list[str]:
    # Split the string into lines
    lines = lyrics.split("\n")

    # Remove all empty lines
    lines = [line for line in lines if line != '']

    # Remove all duplicate lines
    lines = list(set(lines))

    # Remove all lines that are prodominantly English
    english_lines = []
    for line in lines:
        try:
            if detect(line) == "en":
                english_lines.append(line)
        except LangDetectException:
            continue
    lines = [line for line in lines if line not in english_lines]

    return lines
from pathlib import Path

from mutagen import mp3


def is_mp3(file_path: Path):
    """
    Return true if a file is an mp3.
    :param file_path: file to be checked
    """
    try:
        return not mp3.MP3(str(file_path)).info.sketchy
    except mp3.HeaderNotFoundError:
        pass
    except FileNotFoundError:
        pass
    return False

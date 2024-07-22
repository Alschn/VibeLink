import re


def extract_youtube_video_id_from_url(url: str) -> str | None:
    id_regex = r'[a-zA-Z0-9_-]+'
    pattern_full = f'watch\?v=({id_regex})'
    pattern_short = f'youtu\.be\/({id_regex})'

    if match_full := re.search(pattern_full, url):
        video_id = match_full.group(1)

    elif match_short := re.search(pattern_short, url):
        video_id = match_short.group(1)

    else:
        video_id = None

    return video_id

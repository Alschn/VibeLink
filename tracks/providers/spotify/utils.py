import re


def extract_spotify_track_id_from_url(url: str) -> str | None:
    pattern = 'track/([a-zA-Z0-9]+)'
    match = re.search(pattern, url)
    if not match:
        return

    return match.group(1)

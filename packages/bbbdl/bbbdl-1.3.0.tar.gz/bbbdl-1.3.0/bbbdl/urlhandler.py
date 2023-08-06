from typing import *
import re


split_regex = re.compile(r"^(https?://.+)/playback/presentation/2\.0/playback\.html\?meetingId=([0-9a-f-]+)$")


def playback_to_data(url) -> Sequence[str]:
    match = split_regex.match(url)
    if not match:
        raise ValueError("Could not split URL in base_url and meeting_id")
    return match.groups()

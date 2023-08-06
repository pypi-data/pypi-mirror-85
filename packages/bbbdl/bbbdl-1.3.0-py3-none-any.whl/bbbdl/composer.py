from typing import *
import ffmpeg
from .resources import Meeting
from .tracks import Tracks


def compose_screensharing(meeting: Meeting, width: int, height: int) -> Tracks:
    tracks = Tracks()

    if meeting.webcams:
        tracks.overlay(meeting.webcams.get_video().filter("scale", width, height).filter("setsar", 1, 1))
        tracks.amerge(meeting.webcams.get_audio())

    if meeting.deskshare:
        tracks.overlay(meeting.deskshare.get_video().filter("scale", width, height).filter("setsar", 1, 1))

    return tracks


def compose_lesson(meeting: Meeting, width: int, height: int) -> Tracks:
    tracks = compose_screensharing(meeting, width, height)

    for shape in meeting.shapes:
        scaled_split_shape = shape.resource.get_video().filter("scale", width, height).filter("setsar", 1, 1).split()
        count = 0
        for enable in shape.enables:
            count += 1
            tracks.overlay(scaled_split_shape.stream(count), enable=f"between(t, {enable[0]}, {enable[1]})")

    return tracks

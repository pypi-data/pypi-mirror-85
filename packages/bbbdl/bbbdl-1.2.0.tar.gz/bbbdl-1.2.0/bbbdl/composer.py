from typing import *
import ffmpeg
from .resources import Meeting


def compose_screensharing(meeting: Meeting) -> Tuple[ffmpeg.Stream, ffmpeg.Stream]:
    """Keep the deskshare video and the webcam audio, while discarding the rest."""

    return (
        meeting.deskshare.as_stream().video,
        meeting.webcams.as_stream().audio,
    )


def compose_lesson(meeting: Meeting) -> Tuple[ffmpeg.Stream, ffmpeg.Stream]:
    """Keep slides, deskshare video and webcam audio, while discarding the rest."""

    video_stream, audio_stream = compose_screensharing(meeting)

    for shape in meeting.shapes:
        video_stream = ffmpeg.overlay(video_stream, shape.resource.as_stream().video.filter("scale", 1280, 720),
                                      enable=f"between(t, {shape.start}, {shape.end})")

    return video_stream, audio_stream

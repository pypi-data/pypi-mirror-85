from typing import Optional
import ffmpeg.nodes


class Tracks:
    def __init__(self):
        self.video: Optional[ffmpeg.nodes.FilterableStream] = None
        self.audio: Optional[ffmpeg.nodes.FilterableStream] = None

    def overlay(self, other: ffmpeg.nodes.FilterableStream, **kwargs):
        if self.video is None:
            self.video = other
        else:
            self.video = self.video.overlay(other, **kwargs)

    def amerge(self, other: ffmpeg.nodes.FilterableStream, **kwargs):
        if self.audio is None:
            self.audio = other
        else:
            self.audio = ffmpeg.filter((self.audio, other), "amerge", **kwargs)

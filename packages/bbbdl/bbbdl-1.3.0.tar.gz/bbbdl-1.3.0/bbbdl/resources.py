from __future__ import annotations
from typing import *
import dataclasses
import requests
import bs4
import ffmpeg
from .urlhandler import playback_to_data


class Resource:
    def __init__(self, href: str):
        self.href: str = href
        self._video: Optional[ffmpeg.Stream] = None
        self._video_count: int = 0
        self._audio: Optional[ffmpeg.Stream] = None
        self._audio_count: int = 0

    def __repr__(self):
        return f"<{self.__class__.__qualname__} href={self.href}>"

    @classmethod
    def check_and_create(cls, href: str) -> Optional[Resource]:
        """Check if the resource exists, and create it if it does."""
        r = requests.head(href)
        if not (200 <= r.status_code < 400):
            return None
        return cls(href=href)

    def get_audio(self) -> ffmpeg.nodes.FilterableStream:
        if self._audio is None:
            self._audio = ffmpeg.input(self.href).audio.asplit()
        self._audio_count += 1
        return self._audio.stream(self._audio_count)

    def get_video(self) -> ffmpeg.nodes.FilterableStream:
        if self._video is None:
            self._video = ffmpeg.input(self.href).video.split()
        self._video_count += 1
        return self._video.stream(self._video_count)


@dataclasses.dataclass()
class Shape:
    resource: Resource
    enables: List[Tuple[float, float]]


@dataclasses.dataclass()
class Meeting:
    deskshare: Resource
    webcams: Resource
    shapes: List[Shape]

    @classmethod
    def from_base_url(cls, base_url: str, meeting_id: str) -> Meeting:
        r = requests.get(f"{base_url}/presentation/{meeting_id}/metadata.xml")
        r.raise_for_status()

        deskshare = Resource.check_and_create(href=f"{base_url}/presentation/{meeting_id}/deskshare/deskshare.mp4")
        webcams = Resource.check_and_create(href=f"{base_url}/presentation/{meeting_id}/video/webcams.mp4")

        shape_soup = bs4.BeautifulSoup(requests.get(f"{base_url}/presentation/{meeting_id}/shapes.svg").text,
                                       "lxml")

        shapes: Dict[str, Shape] = {}
        for tag in shape_soup.find_all("image"):
            if not tag["in"]:
                raise ValueError("Tag has no 'in' parameter")
            if not tag["out"]:
                raise ValueError("Tag has no 'out' parameter")
            if not tag["xlink:href"]:
                raise ValueError("Tag has no 'xlink:href' parameter")

            url = tag["xlink:href"]
            if url not in shapes:
                shapes[url] = Shape(resource=Resource(f"{base_url}/presentation/{meeting_id}/{url}"), enables=[])
            shapes[url].enables.append((tag["in"], tag["out"]))

        return cls(
            deskshare=deskshare,
            webcams=webcams,
            shapes=list(shapes.values())
        )

    @classmethod
    def from_url(cls, url: str) -> Meeting:
        return cls.from_base_url(*playback_to_data(url))

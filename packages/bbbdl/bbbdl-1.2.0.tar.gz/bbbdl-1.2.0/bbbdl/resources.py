from __future__ import annotations
from typing import *
import dataclasses
import requests
import bs4
import ffmpeg
from .urlhandler import playback_to_data


@dataclasses.dataclass()
class Resource:
    href: str

    def as_stream(self, **kwargs) -> ffmpeg.Stream:
        return ffmpeg.input(self.href, **kwargs)


@dataclasses.dataclass()
class Shape:
    resource: Resource
    start: float
    end: float

    @classmethod
    def from_tag(cls, tag: bs4.Tag, *, base_url: str) -> Shape:
        # No, `"in" not in tag` does not work
        if not tag["in"]:
            raise ValueError("Tag has no 'in' parameter")
        if not tag["out"]:
            raise ValueError("Tag has no 'out' parameter")
        if not tag["xlink:href"]:
            raise ValueError("Tag has no 'xlink:href' parameter")

        return cls(
            resource=Resource(href=f"{base_url}/{tag['xlink:href']}"),
            start=float(tag["in"]),
            end=float(tag["out"]),
        )


@dataclasses.dataclass()
class Meeting:
    deskshare: Resource
    webcams: Resource
    shapes: List[Shape]

    @classmethod
    def from_base_url(cls, base_url: str, meeting_id: str) -> Meeting:
        r = requests.get(f"{base_url}/presentation/{meeting_id}/metadata.xml")
        r.raise_for_status()

        deskshare = Resource(href=f"{base_url}/presentation/{meeting_id}/deskshare/deskshare.webm")
        webcams = Resource(href=f"{base_url}/presentation/{meeting_id}/video/webcams.mp4")

        shape_soup = bs4.BeautifulSoup(requests.get(f"{base_url}/presentation/{meeting_id}/shapes.svg").text,
                                       "lxml")
        shapes: List[Shape] = []
        for tag in shape_soup.find_all("image"):
            try:
                shapes.append(Shape.from_tag(tag, base_url=f"{base_url}/presentation/{meeting_id}"))
            except ValueError:
                continue

        return cls(
            deskshare=deskshare,
            webcams=webcams,
            shapes=shapes
        )

    @classmethod
    def from_url(cls, url: str) -> Meeting:
        return cls.from_base_url(*playback_to_data(url))

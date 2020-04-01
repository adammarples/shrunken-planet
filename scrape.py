from dataclasses import dataclass

import unidecode
import feedparser
import pandas as pd


@dataclass
class Track:
    artist: str
    name: str


@dataclass
class Feed:
    title: str
    link: str

    @property
    def tracks(self):
        _, df, *rest = pd.read_html(self.link, encoding="utf-8")
        df = df.applymap(decode)
        df = df[["Artist", "Track"]].dropna()
        return tuple(
            Track(artist, name)
            for artist, name in zip(df["Artist"], df["Track"])
            if artist != name
        )


def decode(x):
    try:
        return unidecode.unidecode(x)
    except AttributeError:
        return x


def list_feeds():
    FEED_URL = "http://www.wfmu.org/playlistfeed/SP.xml"
    feed = feedparser.parse(FEED_URL)
    for entry in feed["entries"]:
        yield Feed(
            title=entry["title"], link=entry["link"],
        )

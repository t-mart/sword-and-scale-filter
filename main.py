import os
import re
import traceback
from pathlib import Path
from typing import ClassVar

import flask
import functions_framework
import httpx
from attrs import frozen
from lxml import etree

URL_ENV_VAR = "SWORD_AND_SCALE_RSS_URL"
DEBUG_ENV_VAR = "DEBUG"
CLIENT = httpx.Client()
PARSER = etree.XMLParser(strip_cdata=False)

@frozen
class Episode:
    title: str

    TITLE_PATTERNS: ClassVar[list[str]] = [
        r"\s?Sword and Scale Episode \d+",
        r"\s?\+PLUS \d+",
        r".*Secret Episode"
    ]

    @property
    def is_good(self) -> bool:
        return any(re.match(pattern, self.title) for pattern in self.TITLE_PATTERNS)

def get_rss_content() -> bytes:
    if os.environ.get(DEBUG_ENV_VAR, False):
        return Path("feed.xml").read_bytes()

    url = os.environ.get(URL_ENV_VAR, None)

    if url is None:
        raise RuntimeError(f"No environment variable {URL_ENV_VAR}")

    rss_response = CLIENT.get(url)
    rss_response.raise_for_status()

    return rss_response.content


@functions_framework.errorhandler(Exception)
def handle_zero_division(e: Exception) -> flask.Response:
    response = flask.make_response("".join(traceback.format_exception(e)))
    response.status_code = 500
    response.mimetype = "text/plain"

    return response


@functions_framework.http
def filter_func(cf_request: flask.Request) -> flask.Response:
    root = etree.XML(get_rss_content(), parser=PARSER)

    channel = root.find('channel')
    if channel is None:
        raise ValueError("No channel tag")

    for item in channel.findall("item"):
        title_ele = item.find("title")
        if title_ele is None:
            raise ValueError("No title tag")

        title_text = title_ele.text
        if title_text is None:
            raise ValueError("No title text")

        episode = Episode(title=title_text)
        if not episode.is_good:
            print(f"❌ {episode.title}")
            channel.remove(item)

    cf_response = flask.make_response(etree.tostring(root))
    cf_response.status_code = 200
    cf_response.mimetype = "application/rss+xml"

    return cf_response

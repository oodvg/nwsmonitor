import aiohttp
import pandas as pd
from .rss_parser import RSSParser
from .nws import USER_AGENT

SPC_FEED_URL = "https://weather.im/iembot-rss/room/spcchat.xml"
WPC_FEED_URL = "https://weather.im/iembot-rss/room/wpcchat.xml"


async def _fetch(session, uri) -> pd.DataFrame:
    headers = {"User-Agent": USER_AGENT}
    parser = RSSParser()
    parser.reset()  # make sure there are no residual data
    async with session.get(
        uri,
        headers=headers,
        raise_for_status=True,
        timeout=aiohttp.ClientTimeout(total=60),
    ) as resp:
        parser.feed(await resp.text())
        article_list = parser.article_list
        return pd.DataFrame(article_list)


async def fetch_spc_feed() -> pd.DataFrame:
    async with aiohttp.ClientSession() as session:
        return await _fetch(session, SPC_FEED_URL)


async def fetch_wpc_feed() -> pd.DataFrame:
    async with aiohttp.ClientSession() as session:
        return await _fetch(session, WPC_FEED_URL)

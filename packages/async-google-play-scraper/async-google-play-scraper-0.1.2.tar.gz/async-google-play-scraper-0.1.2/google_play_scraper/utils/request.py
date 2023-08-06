try:
    from typing import Union
except ImportError:
    pass

from google_play_scraper.exceptions import NotFoundError, ExtraHTTPError

import aiohttp


async def handle_resp(resp):
    try:
        resp.raise_for_status()
        return await resp.text()
    except aiohttp.ClientResponseError as x:
        if x.status == 404:
            raise NotFoundError("App not found(404).")
        else:
            raise ExtraHTTPError(
                "App not found. Status code {} returned.".format(x.status)
            )


async def post(url, data, headers):
    # type: (str, Union[str, bytes], dict) -> str
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as resp:
            # resp.text()
            return await handle_resp(resp)

    # return _urlopen(Request(url, data=data, headers=headers))


async def get(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await handle_resp(resp)

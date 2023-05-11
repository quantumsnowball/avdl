from typing import Any
from aiohttp import ClientSession

from yarl import URL

import datetime


async def async_fetch_m3u8(url: URL,
                           *,
                           headers: dict[str, str]) -> tuple[tuple[str, ...], dict[str, Any]]:
    async with ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            # fetch
            m3u8_content = await response.text()
            lines = m3u8_content.split('\n')
            # parts
            parts = tuple(line.strip()
                          for line in lines
                          if line and not line.startswith('#'))
            # duration
            count = len(parts)
            total_seconds = round(sum(float(line.split(':')[1].split(',')[0])
                                      for line in lines
                                      if line.startswith('#EXTINF:')))
            info = dict(count=count,
                        duration=str(datetime.timedelta(seconds=total_seconds)),)
            return parts, info

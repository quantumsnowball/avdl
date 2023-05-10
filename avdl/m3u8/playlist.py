from aiohttp import ClientSession

from yarl import URL


async def async_fetch_m3u8(url: URL,
                           *,
                           session: ClientSession) -> tuple[str, ...]:
    async with session.get(url) as response:
        # fetch
        m3u8_content = await response.text()
        # parse the m3u8 file to get the URLs of the video segments
        parts = tuple(line.strip()
                      for line in m3u8_content.split('\n')
                      if line and not line.startswith('#'))
        return parts

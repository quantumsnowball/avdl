import aiohttp
from urllib.parse import urljoin


async def async_fetch_m3u8(url: str,
                           headers: dict[str, str]) -> tuple[str]:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            # fetch
            m3u8_content = await response.text()
            base_url = urljoin(url, '.')
            # parse the m3u8 file to get the URLs of the video segments
            segment_urls = tuple(urljoin(base_url, line.strip())
                                 for line in m3u8_content.split('\n')
                                 if line and not line.startswith('#'))
            return segment_urls

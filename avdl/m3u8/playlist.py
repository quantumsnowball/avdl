import aiohttp


async def async_fetch_m3u8(url: str,
                           headers: dict[str, str]) -> None:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            # fetch
            m3u8_content = await response.text()
            # parse the m3u8 file to get the URLs of the video segments
            segment_urls = [line.strip()
                            for line in m3u8_content.split('\n')
                            if line and not line.startswith('#')]
            print(segment_urls)

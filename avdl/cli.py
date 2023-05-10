import click
import asyncio
import aiohttp


DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'


async def fetch_m3u8(url: str,
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


@click.group()
def avdl() -> None:
    pass


@avdl.command()
def m3u8() -> None:
    url = input('Please input a m3u8 video url:\n>>> ')
    print('Custom header? (Type name:value/Enter to finish)')
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US, en;q = 0.9',
        'User-Agent': DEFAULT_USER_AGENT,
    }
    while True:
        line = input()
        if not line:
            break
        key, val = map(str.strip, line.split(':', 1))
        headers[key] = val
    task = fetch_m3u8(url, headers)
    asyncio.run(task)

import asyncio

import aiohttp

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'}
base_url = 'http://www.xbiquge.la'
test_url = 'http://www.xbiquge.la/13/13959/'


async def test_2():
    async with aiohttp.ClientSession() as session:
        async with session.get(test_url, headers=header) as res:
            res.encoding = 'utf8'
            text = await res.text()
            print(text)
            return text


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_2())

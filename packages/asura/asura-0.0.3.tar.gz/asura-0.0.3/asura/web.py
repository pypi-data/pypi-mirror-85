import aiohttp

async def req_async(url: str):
    async with aiohttp.ClientSession() as sess:
        async with sess.get(url) as resp:
            return await resp.text()
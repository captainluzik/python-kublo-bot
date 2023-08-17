from aiohttp import request

URL = "http://api.giphy.com/v1/gifs/random?tag=fail&type=random&raiting=pg-13&api_key=uFNyVnubQGY6LMJxgfYoA0Qi9v6QA7E7"


async def get_random_gif() -> str:
    async with request("GET", URL) as response:
        if response.status == 200:
            data = await response.json()
            return data['data']['images']['original']['url']
        else:
            return "https://media.giphy.com/media/3o7aD2jB0tPcPERP6c/giphy.gif"

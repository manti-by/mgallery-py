import json

import aioredis
import asyncio

from mgallery.settings import REDIS_URL

redis = aioredis.from_url(REDIS_URL)


async def create_image(
    path: str,
    name: str,
    phash: str = None,
    width: int = None,
    height: int = None,
    size: int = None,
) -> str:
    key = f"{phash}-{path}/{name}"
    value = json.dumps(
        {
            "path": path,
            "name": name,
            "phash": phash,
            "width": width,
            "height": height,
            "size": size,
        }
    )
    await redis.set(key, value)
    return key


async def get_image(key: str) -> dict:
    return json.loads(await redis.get(key))


async def get_images(pattern: str = "*") -> tuple:
    return await asyncio.gather(*[get_image(key) for key in await redis.keys(pattern)])


async def get_duplicates() -> tuple:
    # TODO: add duplicates check
    return await get_images()


async def delete_image(path: str, name: str) -> tuple:
    return await asyncio.gather(
        *[redis.delete(key) for key in await redis.keys(f"*{path}/{name}")]
    )

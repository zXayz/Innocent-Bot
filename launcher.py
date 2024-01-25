from __future__ import annotations

import asyncio
import logging
import logging.handlers
from aiohttp import ClientSession
from core.config import BOT_TOKEN

from setup import BaseBot


async def main():
    """Main function."""
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename=f"logs/discord.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  #32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", date_format, style="{")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Start async session
    async with ClientSession() as web_client:
        async with BaseBot(
            web_client=web_client,
            ) as client:
            await client.start(BOT_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
    
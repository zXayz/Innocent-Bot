from __future__ import annotations

import os
import discord
from discord.ext import commands
from datetime import datetime
import logging
from core.config import DEFAULT_PREFIX, TEST_GUILD
from database.database import DataBase
from typing import Optional
from aiohttp import ClientSession


# logger = logging.getLogger(__name__)
logger = logging.getLogger("discord")


# All Intents 
intents = discord.Intents(
                            guilds=True,
                            members=True,
                            bans=True,
                            # voice_states=True,
                            messages=True,
                            message_content=True, 
                            # presences=True,
                        )

class BaseBot(commands.Bot):
    def __init__(self, 
                *args,
                web_client: ClientSession,
                **kwargs):
        """Initializing the bot"""

        super().__init__(
            command_prefix=DEFAULT_PREFIX,
            case_insensitive=True,
            allowed_mentions=discord.AllowedMentions(everyone=False),
            activity=discord.Game(name=f"help"),
            intents=intents,
            **kwargs,
        )
        self.web_client = web_client
        self.testing_guild_id: int | None = TEST_GUILD or None
        self.start_time = datetime.utcnow()
        self.db = DataBase()


    async def on_ready(self):
        """On Ready event handler"""
        await self.wait_until_ready()
        logger.info(f'Logged on as {self.user}!')



    
    async def setup_extension(self):
        """Loading all the extensions from cogs folder."""
        # at first load Jishaku
        await self.load_extension('jishaku')


        path = "cogs"
        extensions = [f.replace('.py', '') for f in os.listdir(path) if f.endswith('.py')]
        # Load each extension from cogs folder.
        for extension in extensions:
            try:
                await self.load_extension(f'{path}.{extension}')
                logger.info(f"Loaded extension: {extension}")
            except Exception as e:
                logger.error(f"Failed to load extension {extension}: {e}")
                

    async def set_owner(self):
        """Set owner for the bot"""
        
        await self.wait_until_ready()
        app_info = await self.application_info()
        self.owner = app_info.owner
        logger.info("Set Owner complete!")
        
    async def setup_hook(self):
        """Setup hook which will be called in the start of bot."""
        
        logger.info(f"Setup hook called!")
        await self.setup_extension()
        self.loop.create_task(self.set_owner())
        await self.db.connect()
        logger.info("Setup hook complete!")
        
        

        
        
        
        

        
        
        

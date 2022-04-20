import logging
import sqlite3

import disnake
from aiohttp import ClientSession
from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from plasmosync import settings, config

logger = logging.getLogger(__name__)


class Test(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    @commands.slash_command(name="test")
    async def test_slash_command(self, inter: ApplicationCommandInteraction):
        await inter.send(embed=disnake.Embed(title="123", description="ъеъ " * 100),
                         components=[[disnake.ui.Button(style=disnake.ButtonStyle.success, label="✅ Синхронизация ролей"),
                                     disnake.ui.Button(style=disnake.ButtonStyle.success, label="✅ Синхронизация ников"),
                                     disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="❌ Синхронизация банов", disabled=False),
                                     disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="❌ Вайтлист", disabled=False),]
                                ,[disnake.ui.Button(style=disnake.ButtonStyle.success, label="✅ Синхронизация ролей"),
                                     disnake.ui.Button(style=disnake.ButtonStyle.success, label="✅ Синхронизация ников"),], ])


def setup(client):
    client.add_cog(Test(client))

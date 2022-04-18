import logging
import sqlite3

import disnake
from aiohttp import ClientSession
from disnake.ext import commands

from plasmosync import settings, config

logger = logging.getLogger(__name__)


class AdminTools(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    # TODO: verify
    # TODO: unverify
    # TODO: /get guild <id>
    # TODO: /get guilds
    # TODO: /configure guild switch <id> <switch> <bool>
    # TODO: /configure guild role <id> <switch> <roleid>
    # TODO: /configure guild resetrole <id> <switch>
    # TODO: /guild leave <id> <reason>
    # TODO: /guild reset-and-leave <id> <reason>
    # TODO: /guild force-sync <id>
    # TODO: /force-sync-all-guilds
    # TODO: /force-update-ban <userid>


def setup(client):
    client.add_cog(AdminTools(client))

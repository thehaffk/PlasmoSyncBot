import logging
import sqlite3

import disnake
from aiohttp import ClientSession
from disnake.ext import commands

from plasmosync import settings, config

logger = logging.getLogger(__name__)


class PublicCommands(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    # TODO: /sync user
    # TODO: /sync guild
    # TODO: /settings
    # TODO: /set switch <name> <bool>
    # TODO: /set role <name> <role>
    # TODO: /reset role
    # TODO: /help
    # TODO: /status
    # TODO: SYNC usercommand


def setup(client):
    client.add_cog(PublicCommands(client))

import logging
import sqlite3
from typing import Dict

import disnake
from aiohttp import ClientSession
from disnake.ext import commands

from plasmosync import settings, config

logger = logging.getLogger(__name__)


class Synchronization(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    async def sync(self, user: disnake.Member) -> bool:
        ...
        donor = settings.DONOR
        guild = user.guild

        # Check if guild is verified
        # Get guild settings
        # If guild is verified and whitelist enabled
        #   check user pass

        # if user is on donor:
        #   If sync roles
        #       get guild roles
        #       get user roles
        #       unsync roles
        #       sync roles
        #   If sync nicknames
        #       get user nick
        #       sync nick
        # elif guild is verified:
        #   If sync bans is enabled
        #       ban if user is banned
        #   If using api and any(sync roles, sync nick)
        #       return await self._sync_via_api

    async def _sync_via_api(self, user: disnake.Member, guild_switches: Dict[str, bool]) -> bool:
        # We already know that guild is verified, so there is no reason to check it again
        donor = settings.DONOR
        guild = user.guild

        if donor.api_base_url is None:
            return False

        # We know that sync nicknames or sync roles is enabled, so we must do an api call before config checks

        #   If sync nicknames
        #       get user nick
        #       sync nick
        #   If sync roles9
        #       get guild roles
        #       get user roles from api response
        #       unsync roles
        #       sync roles
        #       if banned role is set
        #           sync ban role





def setup(client):
    client.add_cog(Synchronization(client))

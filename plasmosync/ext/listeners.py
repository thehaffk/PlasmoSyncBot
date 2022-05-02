import logging

import disnake
from disnake.ext import commands

from plasmosync import settings

logger = logging.getLogger(__name__)


class Listeners(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    @commands.Cog.listener('on_member_ban')
    async def ban_handler(self, guild: disnake.Guild, user: disnake.User):
        # TODO

        ...  # Get all guilds with sync_bans or sync_roles switches enabled and sync user

    @commands.Cog.listener('on_member_unban')
    async def unban_handler(self, guild: disnake.Guild, user: disnake.User):
        # TODO

        ...  # Get all verified guilds with sync_bans switch enabled and sync user

    @commands.Cog.listener('on_member_join')
    async def join_handler(self, guild: disnake.Guild, user: disnake.User):
        # TODO
        if guild.id == settings.DONOR.guild_discord_id:
            ...
        else:
            ...

        ...  # if donor - sync on all guilds with sync roles/sync nicknames enabled, else - sync locally

    @commands.Cog.listener('on_member_leave')
    async def leave_handler(self, guild: disnake.Guild, user: disnake.User):
        # TODO
        ...  # if donor - sync on all guilds with sync roles/whitelist enabled, else - pass

    @commands.Cog.listener('on_member_update')
    async def updates_handler(self, guild: disnake.Guild, user: disnake.User):
        # TODO
        ...  # if donor - update on all guilds where sync roles / sync nicknames / whitelist enabled

    @commands.Cog.listener('on_guild_join')
    async def ne_guild_handler(self, guild: disnake.Guild, user: disnake.User):
        # TODO
        ...  # if donor - update on all guilds where sync roles / sync nicknames / whitelist enabled

    @commands.Cog.listener('on_guild_leave')
    async def ne_guild_handler(self, guild: disnake.Guild, user: disnake.User):
        # TODO
        ...  # if donor - update on all guilds where sync roles / sync nicknames / whitelist enabled

    async def cog_load(self) -> None:
        logger.info("Loaded %s", __name__)


def setup(client):
    client.add_cog(Listeners(client))

import logging

import disnake
from disnake.ext import commands

from plasmosync import settings, config
from plasmosync.utils import database

logger = logging.getLogger(__name__)


class Listeners(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot
        self.core = None

    @commands.Cog.listener("on_member_ban")
    async def ban_handler(self, guild: disnake.Guild, user: disnake.User):
        logger.debug("%s (<@%s>) was banned on %s (%s)", user, user.id, guild, guild.id)
        if guild.id == settings.DONOR.guild_discord_id:
            guilds_to_sync = await database.get_active_guilds()
            for guild_id in guilds_to_sync:
                guild = self.bot.get_guild(guild_id)
                if (
                    guild is not None
                    and (member := await guild.getch_member(user.id)) is not None
                ):
                    await self.core.sync(member)
            return

        await self.bot.get_guild(config.DevServer.id).get_channel(
            config.DevServer.bot_logs_channel_id
        ).send(f"**[DEBUG]** {user}({user.id}) was banned in {guild}")
        guild_is_verified = await database.is_guild_verified(guild_id=guild.id)
        guild_settings = await database.get_guild_switches(guild_id=guild.id)
        if guild_is_verified and guild_settings.get("sync_bans", False):
            await self.core.sync_bans(user)

    @commands.Cog.listener("on_member_unban")
    async def unban_handler(self, guild: disnake.Guild, user: disnake.User):
        # TODO

        ...  # Get all verified guilds with sync_bans switch enabled and sync user

    @commands.Cog.listener("on_member_join")
    async def join_handler(self, user: disnake.Member):
        # TODO
        if user.guild.id == settings.DONOR.guild_discord_id:
            ...
        else:
            ...

        ...  # if donor - sync on all guilds with sync roles/sync nicknames enabled, else - sync locally

    @commands.Cog.listener("on_member_leave")
    async def leave_handler(self, guild: disnake.Guild, user: disnake.User):
        # TODO
        ...  # if donor - sync on all guilds with sync roles/whitelist enabled, else - pass

    @commands.Cog.listener("on_member_update")
    async def updates_handler(self, guild: disnake.Guild, user: disnake.User):
        # TODO
        ...  # if donor - update on all guilds where sync roles / sync nicknames / whitelist enabled

    @commands.Cog.listener("on_guild_join")
    async def new_guild_handler(self, guild: disnake.Guild, user: disnake.User):
        # TODO
        ...  # if donor - update on all guilds where sync roles / sync nicknames / whitelist enabled

    @commands.Cog.listener("on_guild_leave")
    async def deactivated_guild_handler(self, guild: disnake.Guild, user: disnake.User):
        # TODO
        ...  # if donor - update on all guilds where sync roles / sync nicknames / whitelist enabled

    async def cog_load(self) -> None:
        logger.info("Loaded %s", __name__)
        self.core = self.bot.get_cog("SyncCore")


def setup(client):
    client.add_cog(Listeners(client))

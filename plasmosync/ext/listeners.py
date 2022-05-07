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
        logger.debug("%s (%s) was banned in %s (%s)", user, user.id, guild, guild.id)
        if guild.id == settings.DONOR.guild_discord_id:
            guilds_to_sync = await database.get_active_guilds()
            for guild_id in guilds_to_sync:
                guild = self.bot.get_guild(guild_id)
                if (
                        guild is not None
                        and (member := await guild.getch_member(user.id)) is not None
                ):
                    await self.core.sync(member)
        else:
            await self.bot.get_guild(config.DevServer.id).get_channel(
                config.DevServer.bot_logs_channel_id
            ).send(f"**[DEBUG]** {user}(<@{user.id}>) was banned in {guild}")
            guild_is_verified = await database.is_guild_verified(guild_id=guild.id)
            guild_settings = await database.get_guild_switches(guild_id=guild.id)
            if guild_is_verified and guild_settings.get("sync_bans", False):
                await self.core.sync_bans(user, user_guild=guild)

    @commands.Cog.listener("on_member_unban")
    async def unban_handler(self, guild: disnake.Guild, user: disnake.User):
        logger.debug("%s (%s) was unbanned in %s (%s)", user, user.id, guild, guild.id)
        if guild.id == settings.DONOR.guild_discord_id:
            guilds_to_sync = await database.get_active_guilds(switch="sync_bans")
            for guild_id in guilds_to_sync:
                guild = self.bot.get_guild(guild_id)
                if (
                        guild is not None
                        and await database.is_guild_verified(guild.id)
                        and (member := await guild.getch_member(user.id)) is not None
                ):
                    await self.core.sync(member)
        else:
            await self.bot.get_guild(config.DevServer.id).get_channel(
                config.DevServer.bot_logs_channel_id
            ).send(f"**[DEBUG]** {user}(<@{user.id}>) was unbanned in {guild}")
            guild_is_verified = await database.is_guild_verified(guild_id=guild.id)
            guild_settings = await database.get_guild_switches(guild_id=guild.id)
            if guild_is_verified and guild_settings.get("sync_bans", False):
                await self.core.sync_bans(user, user_guild=guild)

    @commands.Cog.listener("on_member_join")
    async def user_join_handler(self, user: disnake.Member):
        if user.guild.id != settings.DONOR.guild_discord_id:
            await self.core.sync(user)

    @commands.Cog.listener("on_member_remove")
    async def user_leave_handler(self, user: disnake.Member):
        if user.guild.id == settings.DONOR.guild_discord_id:
            guilds_to_sync = []
            guilds_to_sync += await database.get_active_guilds("sync_roles")
            guilds_to_sync += await database.get_active_guilds("whitelist")
            for guild_id in set(guilds_to_sync):
                guild = self.bot.get_guild(guild_id)
                if (member := await guild.getch_member(user.id)) is not None:
                    await self.core.sync(member)

    @commands.Cog.listener("on_member_update")
    async def user_updates_handler(self, before: disnake.Member, after: disnake.Member):
        if before.guild.id != settings.DONOR.guild_discord_id:
            return

        guilds_to_sync = []
        if before.roles != after.roles:
            changed_role = (
                    list(set(before.roles) - set(after.roles))
                    + list(set(after.roles) - set(before.roles))
            )[0]
            if changed_role.id == settings.DONOR.player_role.discord_id:
                guilds_to_sync += await database.get_active_guilds(switch="whitelist")

            if changed_role.id in [role.discord_id for role in settings.DONOR.roles]:
                guilds_to_sync += await database.get_active_guilds(switch="sync_roles")

        if before.display_name != after.display_name:
            guilds_to_sync += await database.get_active_guilds(switch="sync_nicknames")

        for guild_id in set(guilds_to_sync):
            guild = self.bot.get_guild(guild_id)
            if (member := await guild.getch_member(before.id)) is not None:
                await self.core.sync(member)

    @commands.Cog.listener("on_guild_join")
    async def guild_join_handler(self, guild: disnake.Guild):
        await self.bot.get_guild(config.DevServer.id).get_channel(
            config.DevServer.bot_logs_channel_id
        ).send(f"**[DEBUG]** Joined {guild}")
        if guild.id == settings.DONOR.guild_discord_id:
            logger.info("Joined donor guild")
        else:
            await database.activate_guild(guild_id=guild.id)

    @commands.Cog.listener("on_guild_remove")
    async def guild_leave_handler(self, guild: disnake.Guild):
        await self.bot.get_guild(config.DevServer.id).get_channel(
            config.DevServer.bot_logs_channel_id
        ).send(f"**[DEBUG]** Left {guild}")
        if guild.id == settings.DONOR.guild_discord_id:
            logger.critical("Left donor guild")
        else:
            await database.deactivate_guild(guild_id=guild.id)

    async def cog_load(self) -> None:
        logger.info("Loaded Listeners")
        self.core = self.bot.get_cog("SyncCore")


def setup(client):
    client.add_cog(Listeners(client))

""""""
import asyncio
import logging

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import LargeInt

from plasmosync import config, settings
from plasmosync.utils import database

logger = logging.getLogger(__name__)


class AdminTools(commands.Cog):
    """"""

    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    @commands.guild_only()
    @commands.is_owner()
    @commands.slash_command(name="guild", guild_ids=[config.DevServer.id])
    async def guild_placeholder(self, inter: ApplicationCommandInteraction):
        """
        Placeholder for /get
        """

    @commands.guild_only()
    @guild_placeholder.sub_command(name="list")
    async def get_guilds_command(self, inter: ApplicationCommandInteraction):
        """
        Выводит список всех серверов, где установлен бот
        """
        all_guilds_string = "Name - Members count - ID\n"
        for guild in self.bot.guilds:
            if guild.id == settings.DONOR.guild_discord_id:
                all_guilds_string += (
                    f"**[DONOR]** "
                    f"{guild.name} - {guild.member_count}  <@{guild.owner_id}> ({guild.id})\n"
                )
            else:
                all_guilds_string += f"{guild.name} - {guild.member_count}  <@{guild.owner_id}> ({guild.id})\n"

        for stroke in [
            all_guilds_string[i: i + 2000]
            for i in range(0, len(all_guilds_string), 2000)
        ]:
            await inter.send(content=stroke, ephemeral=True)

    @commands.guild_only()
    @guild_placeholder.sub_command(name="get")
    async def get_guild_command(
            self, inter: ApplicationCommandInteraction, guild_id: LargeInt
    ):
        """
        Получить информацию о сервере
        """
        await inter.response.defer(ephemeral=True)
        guild = self.bot.get_guild(guild_id)
        if guild is None:
            await inter.edit_original_message(content="404 Not found")
            return

        guild_embed = disnake.Embed(title=guild.name, description=guild.description)
        guild_owner = guild.get_member(guild.owner_id)
        guild_embed.add_field(
            name="Owner", value=f"{guild_owner} {guild_owner.mention}", inline=False
        )
        guild_embed.add_field(
            name="Member count", value=guild.member_count, inline=False
        )
        guild_embed.add_field(name="Info", value=repr(guild), inline=False)
        guild_embed.add_field(
            name="Is verified",
            value=(await database.is_guild_verified(guild_id)),
            inline=False,
        )
        guild_embed.add_field(
            name="Settings",
            value=(await database.get_guild_switches(guild_id)),
            inline=False,
        )
        guild_embed.add_field(
            name="Roles", value=(await database.get_guild_roles(guild_id)), inline=False
        )

        await inter.edit_original_message(embed=guild_embed)

    @commands.guild_only()
    @guild_placeholder.sub_command(name="leave")
    async def leave_guild_command(
            self, inter: ApplicationCommandInteraction, guild_id: LargeInt
    ):
        """
        Выйти с сервера
        """
        logger.info("Leaving %s", guild_id)

        if guild_id in [settings.DONOR.guild_discord_id, config.DevServer.id]:
            await inter.send("Unable to leave dev/donor guild")
        await inter.response.defer(ephemeral=True)
        guild = self.bot.get_guild(guild_id)
        if guild is None:
            await inter.edit_original_message(content="404 Not found")
            return

        await guild.leave()

        await inter.edit_original_message(
            embed=disnake.Embed(title=f"Left {guild}", description=repr(guild))
        )

    @commands.guild_only()
    @guild_placeholder.sub_command(name="wipe-and-leave")
    async def wipe_and_leave_guild_command(
            self, inter: ApplicationCommandInteraction, guild_id: LargeInt
    ):
        """
        Выйти с сервера и очистить всю информацию о нем из базы данных
        """
        logger.info("Wiping and leaving %s", guild_id)
        await self.leave_guild_command.invoke(inter=inter, guild_id=guild_id)
        await asyncio.sleep(10)  # Wait for on_guild_remove handler to deactivate guild
        await database.wipe_guild_data(guild_id)

    @commands.guild_only()
    @commands.is_owner()
    @commands.slash_command(name="sync-ban")
    async def sync_user_ban(
            self, inter: ApplicationCommandInteraction, user_id: LargeInt
    ):
        """
        Синхронизировать бан пользователя на всех серверах, где включена синхронизация банов
        """
        logger.debug("Force updating ban for %s", user_id)

        await inter.response.defer(ephemeral=True)
        guilds_to_sync = await database.get_active_guilds(switch="sync_bans")
        user = self.bot.get_user(user_id)
        if user is None:
            await inter.edit_original_message(
                content=f"Unable to get user <@{user_id}>"
            )
            return
        for guild_id in guilds_to_sync:
            if not (await database.is_guild_verified(guild_id)):
                continue

            guild = self.bot.get_guild(guild_id)
            core = self.bot.get_cog("SyncCore")
            await core.sync_bans(user=user, user_guild=guild)
        await inter.edit_original_message(content="Done")


def setup(client):
    client.add_cog(AdminTools(client))
    logger.info("Loaded AdminTools")

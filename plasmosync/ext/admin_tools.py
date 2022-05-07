""""""
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

    # TODO: /guild leave <id> <reason>
    # TODO: /guild reset-and-leave <id> <reason>
    # TODO: /force-sync-all-guilds
    # TODO: /force-update-ban <userid>

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
    async def get_guild_command(self, inter: ApplicationCommandInteraction, guild_id: LargeInt):
        """
        Получить информацию о сервере
        """
        await inter.response.defer(ephemeral=True)
        guild = self.bot.get_guild(guild_id)
        if guild is None:
            await inter.edit_original_message(
                content="404 Not found"
            )
            return

        guild_embed = disnake.Embed(
            title=guild.name,
            description=guild.description
        )
        guild_owner = guild.get_member(guild.owner_id)
        guild_embed.add_field(name="Owner", value=f"{guild_owner} {guild_owner.mention}", inline=False)
        guild_embed.add_field(name="Member count", value=guild.member_count, inline=False)
        guild_embed.add_field(name="Info", value=repr(guild), inline=False)
        guild_embed.add_field(name="Is verified", value=(await database.is_guild_verified(guild_id)), inline=False)
        guild_embed.add_field(name="Settings", value=(await database.get_guild_switches(guild_id)), inline=False)
        guild_embed.add_field(name="Roles", value=(await database.get_guild_roles(guild_id)), inline=False)

        await inter.edit_original_message(embed=guild_embed)


def setup(client):
    client.add_cog(AdminTools(client))
    logger.info("Loaded AdminTools")

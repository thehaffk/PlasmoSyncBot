""""""
import logging

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from plasmosync import config, settings

logger = logging.getLogger(__name__)


class AdminTools(commands.Cog):
    """"""

    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    # TODO: /get guild <id>
    # TODO: /get guilds
    # TODO: /guild leave <id> <reason>
    # TODO: /guild reset-and-leave <id> <reason>
    # TODO: /guild force-sync <id>
    # TODO: /force-sync-all-guilds
    # TODO: /force-update-ban <userid>

    @commands.guild_only()
    @commands.is_owner()
    @commands.slash_command(name="get", guild_ids=[config.DevServer.id])
    async def get_placeholder(self, inter: ApplicationCommandInteraction):
        """
        Placeholder for /get
        """

    @commands.guild_only()
    @get_placeholder.sub_command(name="guilds")
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


def setup(client):
    client.add_cog(AdminTools(client))
    logger.info("Loaded AdminTools")

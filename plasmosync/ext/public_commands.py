import logging
import sqlite3

import disnake
from aiohttp import ClientSession
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import user_command

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

    @user_command(name="Синхронизировать")
    async def sync_button(
        self, inter: ApplicationCommandInteraction, user: disnake.Member
    ):
        """
        "Sync" button
        :param inter: button interaction
        :param user: user to sync
        """
        await inter.response.defer(with_message=False, ephemeral=True)
        if not all(
            [
                inter.author.guild_permissions.manage_roles,
                inter.author.guild_permissions.manage_nicknames,
            ]
        ):
            return await inter.edit_original_message(
                embed=disnake.Embed(
                    title="Missing permissions", color=disnake.Color.dark_red()
                ),
            )

        member = inter.guild.get_member(user.id)
        if member is None:
            return await inter.edit_original_message(
                embed=disnake.Embed(
                    title="Could not found that user", color=disnake.Color.dark_red()
                ),
            )
        else:
            await self.bot.get_cog("Synchronization").sync(member)

        return await inter.edit_original_message(
            embed=disnake.Embed(
                title="Synced", color=disnake.Color.dark_green()
            ),
        )



def setup(client):
    client.add_cog(PublicCommands(client))
    logger.info("Loaded PublicCommands")

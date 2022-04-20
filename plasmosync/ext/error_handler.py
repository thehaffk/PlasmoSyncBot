import logging

import disnake
from disnake.ext import commands
from disnake.ext.commands.errors import (
    MissingPermissions,
    MissingRole,
    NotOwner,
    NoPrivateMessage,
)

from plasmosync import config

logger = logging.getLogger(__name__)


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, NoPrivateMessage):
            return
        else:
            logger.error(error)
            await ctx.reply(
                embed=disnake.Embed(
                    title="Error",
                    description=f"Возникла неожиданная ошибка.\n\n`{error}`",
                    color=disnake.Color.red(),
                )
            )
            raise error

    @commands.Cog.listener()
    async def on_slash_command_error(
        self, inter: disnake.ApplicationCommandInteraction, error: Exception
    ):
        if isinstance(error, MissingRole):
            return await inter.send(
                embed=disnake.Embed(
                    title="У Вас недостаточно прав.",
                    description="Вам нужно "
                    f"иметь роль <@&{error.missing_role}> для использования этой команды.",
                    color=disnake.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, MissingPermissions):
            return await inter.send(
                embed=disnake.Embed(
                    title="У Вас недостаточно прав.",
                    description="Вам нужно "
                    f"иметь пермишен **{error.missing_permissions[0]}** для использования этой команды.",
                    color=disnake.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, NotOwner):
            return await inter.send(
                embed=disnake.Embed(
                    title="У Вас недостаточно прав.",
                    description="Вам нужно быть "
                    "создателем бота для использования этой функции.",
                    color=disnake.Color.red(),
                ),
                ephemeral=True,
            )
        else:
            logger.error(error)
            await inter.send(
                embed=disnake.Embed(
                    title="Error",
                    description=f"Возникла неожиданная ошибка.\n\n`{error}`",
                    color=disnake.Color.red(),
                ),
                ephemeral=True,
            )
            await self.bot.get_guild(config.DevServer.id).get_channel(
                config.DevServer.errors_channel_id
            ).send(
                embed=disnake.Embed(
                    title=f"Unknown error happened in {inter.guild.name}",
                    description=repr(error),
                ).add_field(name="Caused by", value=inter.author.mention)
            )
            raise error


def setup(client):
    client.add_cog(ErrorHandler(client))
    logger.info("Loaded ErrorHandler")


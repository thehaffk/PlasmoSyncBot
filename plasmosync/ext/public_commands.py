import logging

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import user_command

logger = logging.getLogger(__name__)


class PublicCommands(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot
        self.core = None

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
            sync_status, error_messages = await self.core.sync(member)

        if sync_status:
            synced_embed = disnake.Embed(title=f"Результат синхронизации - {user} | {user.guild}", color=disnake.Color.dark_green())
            synced_embed.add_field(
                name="Статус", value="✅ Синхронизация прошла успешно"
            )
        else:
            synced_embed = disnake.Embed(title=f"Результат синхронизации - {user} | {user.guild}", color=disnake.Color.dark_red())
            error_messages = "\n❌".join(error_messages)
            synced_embed.add_field(
                name="Синхронизация прошла c ошибками, проверьте настройки бота:",
                value=error_messages,
            )

        return await inter.edit_original_message(
            embed=synced_embed,
        )

    async def cog_load(self) -> None:
        self.core = self.bot.get_cog("SyncCore")
        if self.core is None:
            raise ModuleNotFoundError("Could not get sync core")


def setup(client):
    client.add_cog(PublicCommands(client))
    logger.info("Loaded PublicCommands")

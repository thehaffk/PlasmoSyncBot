import logging
from typing import List

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import user_command

from plasmosync import settings, config
from plasmosync.utils import database

logger = logging.getLogger(__name__)


class SettingButton(disnake.ui.Button["GuildSwitch"]):
    def __init__(self, setting_alias: str, disabled=False, no_access=False, row=0):
        self.switch: config.Setting = settings.DONOR.settings_by_aliases[setting_alias]
        self.switch_status = not disabled
        if self.switch_status:
            style = disnake.ButtonStyle.success
        else:
            style = disnake.ButtonStyle.secondary

        super().__init__(
            style=style, label=self.switch.name, row=row, disabled=no_access
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        ...


class SettingsView(disnake.ui.View):
    children: List[SettingButton]


async def get_settings_embeds(guild: disnake.Guild) -> List[disnake.Embed]:
    guild_is_verified = await database.is_guild_verified(guild.id)
    guild_swithes = await database.get_guild_switches(guild.id)

    settings_embed = disnake.Embed(
        title=f"Локальные настройки Plasmo Sync |"
        f" {config.Emojis.verified if guild_is_verified else ''} {guild.name}",
        color=disnake.Color.dark_green(),
    )

    inaccessible_switches = []
    for switch_alias, value in guild_swithes.items():
        switch = settings.DONOR.settings_by_aliases[switch_alias]
        if guild_is_verified if switch.verified_servers_only else True:
            settings_embed.add_field(
                name=(config.Emojis.enabled if value else config.Emojis.disabled)
                + " "
                + switch.name,
                value=switch.description,
                inline=False,
            )
        else:
            inaccessible_switches.append(switch)
    if not guild_is_verified and len(inaccessible_switches) > 0:
        settings_embed.add_field(
            name="🔒 Сервер не верифицирован",
            value=f"Настройки {', '.join([('**' + switch.name + '**') for switch in inaccessible_switches])}"
            f" доступны для синхронизации только [верифицированым серверам]({config.ABOUT_VERIFIED_SERVERS_URL})",
            inline=False
        )

    roles_embed = disnake.Embed(
        color=disnake.Color.dark_green(),
    )
    inaccessible_roles = []
    guild_roles = await database.get_guild_roles(guild.id)
    for role_alias, local_role_id in guild_roles.items():
        config_role = settings.DONOR.roles_by_aliases[role_alias]
        if guild_is_verified if config_role.verified_servers_only else True:
            roles_embed.add_field(
                name=config_role.name,
                value=f"<@&{local_role_id}>" if local_role_id is not None else "Not specified",
                inline=True,
            )
        else:
            inaccessible_roles.append(config_role)

    if not guild_is_verified and len(inaccessible_roles) > 0:
        roles_embed.add_field(
            name="🔒 Сервер не верифицирован",
            value=f"Роли {', '.join([('**' + role.name + '**') for role in inaccessible_roles])}"
                  f" доступны для синхронизации только [верифицированым серверам]({config.ABOUT_VERIFIED_SERVERS_URL})",
            inline=False
        )

    return [settings_embed, roles_embed]


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

    @commands.has_permissions(manage_roles=True, manage_nicknames=True)
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
            synced_embed = disnake.Embed(
                title=f"Результат синхронизации - {user} | {user.guild}",
                color=disnake.Color.dark_green(),
            )
            synced_embed.add_field(
                name="Статус", value="✅ Синхронизация прошла успешно"
            )
        else:
            synced_embed = disnake.Embed(
                title=f"Результат синхронизации - {user} | {user.guild}",
                color=disnake.Color.dark_red(),
            )
            error_messages = "\n❌".join(error_messages)
            synced_embed.add_field(
                name="Синхронизация прошла c ошибками, проверьте настройки бота:",
                value=error_messages,
            )

        return await inter.edit_original_message(
            embed=synced_embed,
        )

    @commands.slash_command()
    async def settings(self, inter: ApplicationCommandInteraction):
        await inter.response.defer(with_message=False, ephemeral=True)

        await inter.edit_original_message(
            embeds=(await get_settings_embeds(guild=inter.guild))
        )

    async def cog_load(self) -> None:
        self.core = self.bot.get_cog("SyncCore")
        if self.core is None:
            raise ModuleNotFoundError("Could not get sync core")


def setup(client):
    client.add_cog(PublicCommands(client))
    logger.info("Loaded PublicCommands")

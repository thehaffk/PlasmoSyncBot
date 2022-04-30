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
    def __init__(
        self, setting_alias: str, switch_position=False, no_access=False, row=0
    ):
        self.switch: config.Setting = settings.DONOR.settings_by_aliases[setting_alias]
        # privileged settings may be enabled
        # but guild may be not verified at same time,
        # they don't work without verification, so I need to disable them
        self.switch_status = switch_position and not no_access

        if self.switch_status:
            style = disnake.ButtonStyle.success
        else:
            style = disnake.ButtonStyle.secondary

        super().__init__(
            style=style,
            label=self.switch.name,
            row=row,
            disabled=no_access,
            custom_id=setting_alias,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        view: SettingsView = self.view
        if not inter.author.guild_permissions.manage_guild:
            return await inter.send(
                embed=disnake.Embed(
                    title="Не хватает прав",
                    description="Вам нужно иметь пермишен `manage_server` для изменения настроек Plasmo Sync",
                    color=disnake.Color.dark_red(),
                )
            )
        await inter.response.defer(ephemeral=True)

        self.switch_status = not self.switch_status
        if self.switch_status:
            self.style = disnake.ButtonStyle.success
        else:
            self.style = disnake.ButtonStyle.secondary



        return await inter.edit_original_message(view=view)



class SettingsView(disnake.ui.View):
    children: List[SettingButton]

    def __init__(
        self,
        inter: disnake.Interaction,
        local_settings: dict[str, bool],
        guild_is_verified=False,
    ):
        super().__init__(timeout=600)
        for index, setting in enumerate(settings.DONOR.settings):
            self.add_item(
                SettingButton(
                    setting_alias=setting.alias,
                    switch_position=local_settings.get(setting.alias, setting.default),
                    no_access=(not guild_is_verified)
                    if setting.verified_servers_only
                    else False,
                    row=index // 5,
                )
            )


async def get_settings_embeds(guild: disnake.Guild) -> List[disnake.Embed]:
    # TODO: Add guild is verified as a parameter to avoid second database call
    guild_is_verified = await database.is_guild_verified(guild.id)
    guild_swithes = await database.get_guild_switches(guild.id)

    settings_embed = disnake.Embed(
        title=f"Локальные настройки Plasmo Sync |"
        f" {config.Emojis.verified if guild_is_verified else ''} {guild.name}",
        color=disnake.Color.dark_green(),
    )

    inaccessible_switches = []
    for setting in settings.DONOR.settings:
        local_setting = guild_swithes.get(setting.alias, setting.default)
        if guild_is_verified if setting.verified_servers_only else True:
            settings_embed.add_field(
                name=(
                    config.Emojis.enabled if local_setting else config.Emojis.disabled
                )
                + " "
                + setting.name,
                value=setting.description,
                inline=False,
            )
        else:
            inaccessible_switches.append(setting)
    if not guild_is_verified and len(inaccessible_switches) > 0:
        settings_embed.add_field(
            name="🔒 Сервер не верифицирован",
            value=f"Настройки {', '.join([('**' + switch.name + '**') for switch in inaccessible_switches])}"
            f" доступны для синхронизации только [верифицированым серверам]({config.ABOUT_VERIFIED_SERVERS_URL})",
            inline=False,
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
                value=f"<@&{local_role_id}>"
                if local_role_id is not None
                else "Not specified",
                inline=True,
            )
        else:
            inaccessible_roles.append(config_role)

    if not guild_is_verified and len(inaccessible_roles) > 0:
        roles_embed.add_field(
            name="🔒 Сервер не верифицирован",
            value=f"Роли {', '.join([('**' + role.name + '**') for role in inaccessible_roles])}"
            f" доступны для синхронизации только [верифицированым серверам]({config.ABOUT_VERIFIED_SERVERS_URL})",
            inline=False,
        )

    return [settings_embed, roles_embed]


class PublicCommands(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot
        self.core = None

    # TODO: /sync user
    # TODO: /sync guild
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

    @commands.guild_only()
    @commands.slash_command()
    async def settings(self, inter: ApplicationCommandInteraction):
        await inter.response.defer(with_message=False, ephemeral=True)
        buttons = []

        if inter.author.guild_permissions.manage_guild:
            local_settings = await database.get_guild_switches(inter.guild.id)
            guild_is_verified = await database.is_guild_verified(inter.guild.id)
            view = SettingsView(inter, local_settings, guild_is_verified)
        else:
            view = None

        await inter.edit_original_message(
            embeds=(await get_settings_embeds(guild=inter.guild)),
            view=view,
        )

    async def cog_load(self) -> None:
        self.core = self.bot.get_cog("SyncCore")
        if self.core is None:
            raise ModuleNotFoundError("Could not get sync core")


def setup(client):
    client.add_cog(PublicCommands(client))
    logger.info("Loaded PublicCommands")

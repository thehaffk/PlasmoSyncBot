"""
Internal config for bot - guild, roles, switches
"""

from dataclasses import dataclass
from typing import Optional

WIKI_LINK = "https://www.notion.so/Discord-9827cd8b10ee4c33920d9c973ad90a6a"  # TODO: Add different wikis to \
# different servers
rp_api_link = "https://rp.plo.su/api/"
verified_text = "<:plasmoverified:943963401607069738> Verified"
verified_description = (
    "<:plasmoverified:943963401607069738> Cервер верифицирован командой Plasmo"
)
enabled_emoji = "<:plasmosyncenabled:944002031780233216>"
disabled_emoji = "<:plasmosyncdisabled:944002049752858704>"


@dataclass(frozen=True)
class PlasmoRole:
    """
    Represents Plasmo Role
    """

    discord_id: int
    name: str
    alias: str
    api_alias: Optional[str]
    verified_servers_only: bool


@dataclass(frozen=True)
class Setting:
    """
    Represents setting, for config
    """

    alias: str
    name: str
    description: str
    default: bool = False
    verified_servers_only: bool = True


class PlasmoRP:
    """
    Config for Plasmo RP, discord guild, api, settings
    """

    guild_discord_id = 828683007635488809  # 828683007635488809
    api_base_url = "https://rp.plo.su/api"

    roles = []

    player_role = PlasmoRole(
        discord_id=943941965655973888,  # 746628733452025866,
        name="Игрок",
        alias="player",
        api_alias="player",
        verified_servers_only=False,
    )
    roles.append(player_role)
    fusion_role = PlasmoRole(
        discord_id=943942028054650881,  # 751722994170331136,
        name="Fusion",
        alias="fusion",
        api_alias="support",
        verified_servers_only=False,
    )
    roles.append(fusion_role)
    interpol_role = PlasmoRole(
        discord_id=943942071906078831,  # 751723033357451335,
        name="Интерпол",
        alias="interpol",
        api_alias="helper",
        verified_servers_only=False,
    )
    roles.append(interpol_role)
    admin_role = PlasmoRole(
        discord_id=943942125198905414,  # 704364763248984145,
        name="Администрация",
        alias="admin",
        api_alias="admin",
        verified_servers_only=False,
    )
    roles.append(admin_role)

    support_role = PlasmoRole(
        discord_id=943942163400626257,  # 872899130270294046,
        name="Поддержка",
        alias="support",
        api_alias=None,
        verified_servers_only=True,
    )
    roles.append(support_role)
    banker_role = PlasmoRole(
        discord_id=826367015014498314,
        name="Банкир",
        alias="banker",
        api_alias="banker",
        verified_servers_only=True,
    )
    roles.append(banker_role)
    mko_member_role = PlasmoRole(
        discord_id=943942205129756673,  # 844507728671277106,
        name="Участник совета МКО",
        alias="mko_member",
        api_alias=None,
        verified_servers_only=True,
    )
    roles.append(mko_member_role)
    mko_helper_role = PlasmoRole(
        discord_id=943942311551844442,  # 826366703591620618,
        name="Помощник совета глав",
        alias="mko_helper",
        api_alias="soviet-helper",
        verified_servers_only=True,
    )
    roles.append(mko_helper_role)
    mko_head_role = PlasmoRole(
        discord_id=943942349178937344,  # 810492714235723777,
        name="Член совета глав МКО",
        alias="mko_head",
        api_alias="supa_helper",
        verified_servers_only=True,
    )
    roles.append(mko_head_role)
    president_role = PlasmoRole(
        discord_id=948303445281108038,  # 880065048792420403,
        name="Президент МКО",
        alias="president",
        api_alias="president",
        verified_servers_only=True,
    )
    roles.append(president_role)

    roles_by_aliases = dict()
    for role in roles:
        roles_by_aliases[role.alias] = role

    settings = []
    sync_nicknames = Setting(
        alias="sync_nicknames",
        name="Синхронизировать ники",
        description="Синхронизировать ники всех пользователей на сервере",
        default=False,
        verified_servers_only=False,
    )
    settings.append(sync_nicknames)
    sync_roles = Setting(
        alias="sync_roles",
        name="Синхронизировать роли",
        description="Синхронизировать роли всех пользователей на сервере",
        default=False,
        verified_servers_only=False,
    )
    settings.append(sync_roles)
    use_api = Setting(
        alias="use_api",
        name="Использовать API",
        description="Использовать API, чтобы получить роли и ники игроков, которых нет на сервере доноре",
        default=True,
        verified_servers_only=True,
    )
    settings.append(use_api)
    whitelist = Setting(
        alias="whitelist",
        name="Вайтлист игроков",
        description="Не позволять пользователям без роли игрока заходить на сервер",
        default=False,
        verified_servers_only=True,
    )
    settings.append(whitelist)

    sync_bans = Setting(
        alias="sync_bans",
        name="Синхронизация банов",
        description="Не позволять пользователям без роли игрока заходить на сервер",
        default=False,
        verified_servers_only=True,
    )
    settings.append(sync_bans)

    settings_by_aliases = dict()
    for setting in settings:
        settings_by_aliases[setting.alias] = setting


class PlasmoSMP:
    """
    Config for Plasmo SMP, discord guild, api, settings
    """

    # TODO: This
    ...


class PlasmoFRP:
    """
    Config for Plasmo FRP, discord guild, api, settings
    """

    # TODO: This
    ...


class DevServer:
    """
    Config for digital drugs (howkawgew's server) guild
    """

    id = 828683007635488809

    bot_logs_channel_id = 943953710856429588
    errors_channel_id = 965700806693257216

    """
    default_settings_dict = {
    "Синхронизировать роли": "sync_roles",
    "Синхронизировать ники": "sync_nicknames",
    }
    verified_settings_dict = {
        "Вайтлист игроков": "kick_guests",
        "Синхронизировать баны": "sync_bans",
        "Удаление ролей": "unsync_roles",
    }"""


all_plasmo_roles = [
    "player",
    "fusion",
    "interpol",
    "admin",
]
verified_plasmo_roles = [
    "support",
    "mko_member",
    "mko_head",
    "banker",
    "mko_helper",
]
all_roles_names = {
    "player": "Игрок",
    "fusion": "Fusion",
    "interpol": "Интерпол",
    "admin": "Администрация",
    "support": "Поддержка",
    "mko_member": "Участник Совета МКО",
    "mko_head": "Член совета глав",
    "banker": "Банкир",
    "mko_helper": "Помощник совета глав",
    "banned": f'Бан на {["name"]}',
}
all_roles_dict = {}
for elem in all_roles_names:
    all_roles_dict[all_roles_names[elem]] = elem

default_settings_dict = {
    "Синхронизировать роли": "sync_roles",
    "Синхронизировать ники": "sync_nicknames",
}
verified_settings_dict = {
    "Вайтлист игроков": "kick_guests",
    "Синхронизировать баны": "sync_bans",
    "Удаление ролей": "unsync_roles",
}

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

DEBUG_VALUES = bool(
    os.getenv("DEBUG_VALUES", False)
)  # Replace donor values with debug values
DEVMODE = bool(os.getenv("DEVMODE", False))  # Fast command registration
OWNERS = [737501414141591594, 222718720127139840, 191836876980748298]
TOKEN = os.getenv("BOT_TOKEN")
TEST_GUILDS = [966785796902363188, 828683007635488809]

WIKI_URL = "https://rp.plo.su/wiki/commune"
ABOUT_VERIFIED_SERVERS_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


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


class Emojis:
    verified = r"<:verified:969672029877977119>"
    enabled = r"✅"
    disabled = r"❌"


# ALL DONORS MUST HAVE SYNC_ROLES AND SYNC_NICKNAMES SWITCHES
@dataclass(frozen=True)
class Setting:
    alias: str
    name: str
    description: str
    default: bool = False
    verified_servers_only: bool = True


class PlasmoRP:
    """
    Config for Plasmo RP, discord guild, api, settings
    """

    name = "Plasmo RP"

    guild_discord_id = 828683007635488809 if DEBUG_VALUES else 672312131760291842
    api_base_url = "https://rp.plo.su/api"

    roles = []

    player_role = PlasmoRole(
        discord_id=943941965655973888 if DEBUG_VALUES else 746628733452025866,
        name="Игрок",
        alias="player",
        api_alias="player",
        verified_servers_only=False,
    )
    roles.append(player_role)
    fusion_role = PlasmoRole(
        discord_id=943942028054650881 if DEBUG_VALUES else 751722994170331136,
        name="Fusion",
        alias="fusion",
        api_alias="support",
        verified_servers_only=False,
    )
    roles.append(fusion_role)
    interpol_role = PlasmoRole(
        discord_id=943942071906078831 if DEBUG_VALUES else 751723033357451335,
        name="Интерпол",
        alias="interpol",
        api_alias="interpol",
        verified_servers_only=False,
    )
    roles.append(interpol_role)
    admin_role = PlasmoRole(
        discord_id=943942125198905414 if DEBUG_VALUES else 704364763248984145,
        name="Администрация",
        alias="admin",
        api_alias="admin",
        verified_servers_only=False,
    )
    roles.append(admin_role)

    support_role = PlasmoRole(
        discord_id=943942163400626257 if DEBUG_VALUES else 872899130270294046,
        name="Поддержка",
        alias="support",
        api_alias=None,
        verified_servers_only=True,
    )
    roles.append(support_role)
    banker_role = PlasmoRole(
        discord_id=943942205129756673 if DEBUG_VALUES else 826367015014498314,
        name="Банкир",
        alias="banker",
        api_alias="banker",
        verified_servers_only=True,
    )
    roles.append(banker_role)
    mko_member_role = PlasmoRole(
        discord_id=943942205129756673 if DEBUG_VALUES else 844507728671277106,
        name="Участник совета МКО",
        alias="mko_member",
        api_alias=None,
        verified_servers_only=True,
    )
    roles.append(mko_member_role)
    mko_helper_role = PlasmoRole(
        discord_id=943942311551844442 if DEBUG_VALUES else 826366703591620618,
        name="Помощник совета глав",
        alias="mko_helper",
        api_alias="soviet-helper",
        verified_servers_only=True,
    )
    roles.append(mko_helper_role)
    keeper_role = PlasmoRole(
        discord_id=943942311551844442 if DEBUG_VALUES else 1003276423747874896,
        name="Хранитель",
        alias="keeper",
        api_alias="keeper",
        verified_servers_only=True,
    )
    roles.append(keeper_role)
    helper_role = PlasmoRole(
        discord_id=943942311551844442 if DEBUG_VALUES else 1023622804794527805,
        name="Хелпер",
        alias="helper",
        api_alias="helper",
        verified_servers_only=True,
    )
    roles.append(helper_role)
    mko_head_role = PlasmoRole(
        discord_id=943942349178937344 if DEBUG_VALUES else 810492714235723777,
        name="Член совета глав МКО",
        alias="mko_head",
        api_alias="supa_helper",
        verified_servers_only=True,
    )
    roles.append(mko_head_role)
    president_role = PlasmoRole(
        discord_id=948303445281108038 if DEBUG_VALUES else 880065048792420403,
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
        name="Синхронизация ников",
        description="**Plasmo Sync** будет синхронизировать ники всех пользователей с Plasmo RP",
        default=False,
        verified_servers_only=False,
    )
    settings.append(sync_nicknames)
    sync_roles = Setting(
        alias="sync_roles",
        name="Синхронизация ролей",
        description="**Plasmo Sync** будет синхронизировать установленные роли всех пользователей с Plasmo RP",
        default=False,
        verified_servers_only=False,
    )
    settings.append(sync_roles)
    whitelist = Setting(
        alias="whitelist",
        name="Вайтлист игроков",
        description='**Plasmo Sync** будет кикать пользователей с сервера, если у них нет роли "Игрок" на Plasmo RP',
        default=False,
        verified_servers_only=False,
    )
    settings.append(whitelist)
    use_api = Setting(
        alias="use_api",
        name="Использование API",
        description="**Plasmo Sync** будет синхронизировать ники пользователей, даже если их нет на Plasmo RP",
        default=True,
        verified_servers_only=True,
    )
    settings.append(use_api)

    sync_bans = Setting(
        alias="sync_bans",
        name="Синхронизация банов",
        description="**Plasmo Sync** будет банить всех участников сервера, которые забанены на Plasmo RP."
        " Функция разбанов может работать нестабильно"
        " - пишите в [поддержку](https://discord.gg/snD9Zcys5Y), если найдете баг",
        default=False,
        verified_servers_only=True,
    )
    settings.append(sync_bans)

    settings_by_aliases = {setting.alias: setting for setting in settings}


class PlasmoSMP:
    """
    Config for Plasmo SMP, discord guild, api, settings
    """

    name = "Plasmo SMP"

    guild_discord_id = 828683007635488809 if DEBUG_VALUES else 385007717623922688
    api_base_url = "https://smp.plo.su/api"

    roles = []

    player_role = PlasmoRole(
        discord_id=943941965655973888 if DEBUG_VALUES else 626887926373941258,  # Done
        name="Игрок",
        alias="player",
        api_alias="player",
        verified_servers_only=False,
    )
    roles.append(player_role)
    fusion_role = PlasmoRole(
        discord_id=943942028054650881 if DEBUG_VALUES else 626887902953209866,  # Done
        name="Fusion",
        alias="fusion",
        api_alias="support",
        verified_servers_only=False,
    )
    roles.append(fusion_role)
    interpol_role = PlasmoRole(
        discord_id=943942071906078831 if DEBUG_VALUES else 626887908946739200,  # Done
        name="Хелпер",
        alias="interpol",
        api_alias="helper",
        verified_servers_only=False,
    )
    roles.append(interpol_role)
    admin_role = PlasmoRole(
        discord_id=943942125198905414 if DEBUG_VALUES else 222718720127139840,  # Done
        name="Администрация",
        alias="admin",
        api_alias="admin",
        verified_servers_only=False,
    )
    roles.append(admin_role)

    roles_by_aliases = dict()
    for role in roles:
        roles_by_aliases[role.alias] = role

    settings = []
    sync_nicknames = Setting(
        alias="sync_nicknames",
        name="Синхронизация ников",
        description="**Plasmo Sync** будет синхронизировать ники всех пользователей с Plasmo SMP",
        default=False,
        verified_servers_only=False,
    )
    settings.append(sync_nicknames)
    sync_roles = Setting(
        alias="sync_roles",
        name="Синхронизация ролей",
        description="**Plasmo Sync** будет синхронизировать установленные роли всех пользователей с Plasmo SMP",
        default=False,
        verified_servers_only=False,
    )
    settings.append(sync_roles)
    whitelist = Setting(
        alias="whitelist",
        name="Вайтлист игроков",
        description='**Plasmo Sync** будет кикать пользователей с сервера, если у них нет роли "Игрок" на Plasmo SMP',
        default=False,
        verified_servers_only=False,
    )
    settings.append(whitelist)
    use_api = Setting(
        alias="use_api",
        name="Использование API",
        description="**Plasmo Sync** будет синхронизировать ники пользователей, даже если их нет на Plasmo SMP",
        default=True,
        verified_servers_only=True,
    )
    settings.append(use_api)

    sync_bans = Setting(
        alias="sync_bans",
        name="Синхронизация банов",
        description="**Plasmo Sync** будет банить всех участников сервера, которые забанены на Plasmo SMP."
        " Функция разбанов может работать нестабильно"
        " - пишите в [поддержку](https://discord.gg/snD9Zcys5Y), если найдете баг",
        default=False,
        verified_servers_only=True,
    )
    settings.append(sync_bans)

    settings_by_aliases = dict()
    for setting in settings:
        settings_by_aliases[setting.alias] = setting


class DevServer:
    """
    Config for digital drugs technologies (howkawgew's server) guild
    """

    id = 966785796902363188

    invite_url = "https://discord.gg/snD9Zcys5Y"

    bot_logs_channel_id = 969713902831173652
    errors_channel_id = 969713902831173652

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

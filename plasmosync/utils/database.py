import logging
from dataclasses import dataclass
from typing import Optional, Dict

import aiosqlite

from plasmosync import settings
from plasmosync.settings import DONOR

logger = logging.getLogger(__name__)


async def setup(path="./plasmosync/data.db") -> bool:
    """
    Check if database is ready for use, updates columns if not
    """
    logger.info("Setting up database...")
    print(path)
    ...


async def is_guild_verified(guild_id: int) -> bool:
    """
    Returns True if guild is verified
    :param guild_id: id of guild
    :return: True if verified, False if not
    """
    # TODO: Make real sql request
    return True


async def get_guild_switches(guild_id: int) -> Dict[str, bool]:
    """
    Get guild settings (switches) from database
    :param guild_id: id of guild
    :return:
    """
    # TODO: Make real sql request
    logger.debug("Getting switches for %s", guild_id)
    return {
        "sync_nicknames": True,
        "sync_roles": True,
        "use_api": True,
        "whitelist": False,
        "sync_bans": True,
    }


async def get_guild_roles(guild_id: int) -> Dict[str, int]:
    """

    :param guild_id:
    :return:
    """
    # TODO: Make real sql request

    return {
        "player": 966785796902363189,
        "fusion": 966785796902363190,
        "interpol": 966785796902363192,
        "admin": 966785796927524897,
        "support": 966785796902363191,

        "mko_helper": 966785796902363193,
        "mko_head": 966785796902363194,
        "president": 966785796902363195,

    }


async def verify_guild(guild_id: int) -> bool:  # TODO: Verify guild
    """

    :param guild_id:
    """
    logger.info("Verifying %s guild", guild_id)
    ...


async def unverify_guild(guild_id: int) -> bool:  # TODO: Unverify guild
    """

    :param guild_id:
    """
    logger.debug("Unverifying %s guild", guild_id)

    ...  # TODO
    return True


async def set_switch(guild_id: int, alias: str, value: bool) -> bool:
    """

    :param guild_id:
    :param alias:
    :param value:
    """
    ...  # TODO
    logger.debug("Setting switch %s to %s at %s", alias, value, guild_id)

    return True


async def set_role(guild_id: int, role_alias: str, value: Optional[int]) -> bool:
    """

    :param guild_id:
    :param role_alias:
    :param value:
    """
    ...  # TODO
    logger.debug("Setting role %s to %s at %s", role_alias, value, guild_id)

    return True


async def remove_role_by_id(guild_id: int, role_id: int) -> bool:
    """
    Removes role from database by given id, used for removing roles that was deleted
    :param guild_id:
    :param role_id:
    """
    logger.debug("Removing role %s from guild %s because it does not exist anymore", role_id, guild_id)
    ...  # TODO
    return True

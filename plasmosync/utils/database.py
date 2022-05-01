import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

verified = False  # Testing, TODO: remove


async def setup(path="./plasmosync/data.db") -> bool:
    """
    Check if database is ready for use, updates columns if not
    """
    logger.info("Setting up database...")
    ...  # TODO
    return True


async def is_guild_verified(guild_id: int) -> bool:
    logger.debug("is_guild_verified was called with %s", guild_id)
    # Just for testing, TODO: This
    return verified


async def get_guild_switches(guild_id: int) -> Dict[str, bool]:
    """
    Get guild settings (switches) from database
    :param guild_id: id of guild
    :return:
    """
    ...  # TODO
    logger.debug("Getting switches for %s", guild_id)
    # Fake data
    return {
        "sync_nicknames": True,
        "sync_roles": False,
        "use_api": True,
        "whitelist": False,
        "sync_bans": True,
    }


async def get_guild_roles(guild_id: int) -> Dict[str, int]:
    # TODO

    # Fake data
    return {
        "player": 966785796902363189,
        "fusion": 966785796902363190,
        "interpol": 966785796902363192,
        "banker": None,
        "admin": 966785796927524897,
        "support": 966785796902363191,
        "mko_helper": 966785796902363193,
        "mko_head": 966785796902363194,
        "president": 966785796902363195,
    }


async def verify_guild(guild_id: int) -> bool:  # TODO: Verify guild
    logger.info("Verifying %s guild", guild_id)

    # Just for testing, TODO: This

    global verified
    verified = True


async def unverify_guild(guild_id: int) -> bool:
    logger.debug("Unverifying %s guild", guild_id)

    # Just for testing TODO: This
    global verified
    verified = False


async def set_switch(guild_id: int, alias: str, value: bool) -> bool:
    ...  # TODO
    logger.debug("Setting switch %s to %s at %s", alias, value, guild_id)

    return True


async def set_role(guild_id: int, role_alias: str, value: Optional[int]) -> bool:
    ...  # TODO
    logger.debug("Setting role %s to %s at %s", role_alias, value, guild_id)

    return True


async def remove_role_by_id(guild_id: int, role_id: int) -> bool:
    logger.debug(
        "Removing role %s from guild %s because it does not exist anymore",
        role_id,
        guild_id,
    )
    ...  # TODO
    return True

import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

verified = True  # Testing, TODO: remove


async def setup(path="./plasmosync/data.db") -> bool:
    """
    Check if database is ready for use, updates columns if not
    """
    logger.info("Setting up database...")
    ...  # TODO
    return True


async def is_guild_verified(guild_id: int) -> bool:
    logger.debug("is_guild_verified was called with %s", guild_id)
    # TODO: SELECT is_verified FROM guilds WHERE discord_id = ?

    return verified


async def get_guild_switches(guild_id: int) -> Dict[str, bool]:
    """
    Get guild settings (switches) from database
    :param guild_id: id of guild
    :return:
    """
    # TODO: SELECT * FROM settings WHERE guild_discord_id = ?
    logger.debug("Getting switches for %s", guild_id)
    # Fake data
    return {
        "sync_nicknames": True,
        "sync_roles": True,
        "use_api": True,
        "whitelist": False,
        "sync_bans": True,
    }


async def get_guild_roles(guild_id: int) -> Dict[str, int]:
    # TODO: SELECT * FROM roles WHERE guild_discord_id = ?

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


async def get_active_guilds() -> List[int]:
    """
    Get list of guild_ids where bot is active. Literally all guilds except those where bot is kicked/banned
    :return: List with guild ids
    """
    # TODO: SELECT discord_id FROM GUILDS WHERE is_available = TRUE
    ...


async def set_switch(guild_id: int, alias: str, value: bool) -> bool:
    """
    Update local guild settings in bot dabatase
    :param guild_id: Discord id of local server
    :param alias: Setting alias
    :param value: New value
    :return: Returns new value of switch
    """
    logger.debug("Setting switch %s to %s in %s", alias, value, guild_id)
    # TODO: INSERT INTO settings(guild_discord_id, alias, value) VALUES(?, ?, ?)
    #   ON CONFLICT(guild_discord_id, alias) DO UPDATE SET role_id=?;

    return value


async def set_role(guild_id: int, role_alias: str, value: Optional[int]):
    ...
    # TODO: INSERT INTO roles(guild_discord_id, alias, role_id) VALUES(?, ?, ?)
    #   ON CONFLICT(guild_discord_id, alias) DO UPDATE SET role_id=?;

    logger.debug("Setting role %s to %s at %s", role_alias, value, guild_id)

    return True


async def remove_role_by_id(role_id: int):
    """
    Remove role id from database. Called when bot could not get role from Disocrd = role is deleted
    :param role_id: Role id (int)
    """
    logger.debug(
        "Removing role %s because it does not exist anymore",
        role_id,
    )
    ...
    # TODO: DELETE FROM ROLES WHERE ROLE = role_id
    return True


async def verify_guild(guild_id: int):
    logger.info("Verifying %s guild", guild_id)

    # TODO: UPDATE

    global verified
    verified = True


async def unverify_guild(guild_id: int):
    logger.debug("Unverifying %s guild", guild_id)

    # Just for testing TODO: This
    global verified
    verified = False


async def activate_guild(guild_id):
    """
    Insert guild into database if not exist, updates and sets is_available to True
    :param guild_id:
    """
    ...


async def deactivate_guild(guild_id):
    """

    :param guild_id:
    :return:
    """


async def check_guild(guild_id):
    """

    :param guild_id:
    :return:
    """

import logging
from typing import Optional, Dict, List

import aiosqlite

from plasmosync import config, settings

logger = logging.getLogger(__name__)

PATH = config.DATABASE_PATH


async def setup() -> bool:
    """
    Check if database is ready for use, updates columns if not
    """
    logger.info("Setting up database...")
    create_guilds_query = """
        CREATE TABLE IF NOT EXISTS guilds
        (
            discord_id   integer not null
                constraint guilds_pk
                    primary key,
            is_available integer default 1 not null,
            is_verified  integer default 0 not null,
            banned       integer default 0 not null
        );
        """
    create_roles_query = """
        CREATE TABLE IF NOT EXISTS roles
        (
            guild_discord_id integer not null,
            alias            text    not null,
            role_id          integer not null,
            unique (guild_discord_id, alias)
        );
        """
    create_settings_query = """
        CREATE TABLE IF NOT EXISTS settings
        (
            guild_discord_id integer not null,
            alias            text    not null,
            value            integer default 0 not null,
            unique (guild_discord_id, alias)
        );

        """
    async with aiosqlite.connect(PATH) as db:
        async with db.execute(create_guilds_query):
            await db.commit()
        async with db.execute(create_roles_query):
            await db.commit()
        async with db.execute(create_settings_query):
            await db.commit()

    return True


async def is_guild_verified(guild_id: int) -> bool:
    logger.debug("is_guild_verified was called with %s", guild_id)

    await check_guild(guild_id)

    async with aiosqlite.connect(PATH) as db:
        async with db.execute(
            "SELECT is_verified FROM guilds WHERE discord_id = ?", (guild_id,)
        ) as cursor:
            return bool((await cursor.fetchone())[0])


async def get_guild_switches(guild_id: int) -> Dict[str, bool]:
    """
    Get guild settings (switches) from database
    :param guild_id: id of guild
    :return:
    """
    logger.debug("Getting switches for %s", guild_id)

    await check_guild(guild_id)

    guild_swithes = {}

    async with aiosqlite.connect(PATH) as db:
        async with db.execute(
                "SELECT alias, value FROM settings WHERE guild_discord_id = ?", (guild_id,)
        ) as cursor:
            for alias, value in await cursor.fetchall():
                if alias in settings.DONOR.settings_by_aliases:
                    guild_swithes[alias] = bool(value)

    for setting in settings.DONOR.settings:
        guild_swithes[setting.alias] = guild_swithes.get(setting.alias, None)

    return guild_swithes


async def get_guild_roles(guild_id: int) -> Dict[str, int]:
    """
    Get guild settings (switches) from database
    :param guild_id: id of guild
    :return:
    """
    logger.debug("Getting roles for %s", guild_id)

    await check_guild(guild_id)

    guild_roles = {}

    async with aiosqlite.connect(PATH) as db:
        async with db.execute(
                "SELECT alias, role_id FROM roles WHERE guild_discord_id = ?", (guild_id,)
        ) as cursor:
            for alias, role_id in await cursor.fetchall():
                if alias in settings.DONOR.roles_by_aliases:
                    guild_roles[alias] = int(role_id)

    for role in settings.DONOR.roles:
        guild_roles[role.alias] = guild_roles.get(role.alias, None)

    return guild_roles


async def get_active_guilds(switch=None) -> List[int]:
    """
    Get list of guild_ids where bot is active. Literally all guilds except those where bot is kicked/banned
    :return: List with guild ids
    """
    async with aiosqlite.connect(PATH) as db:
        if switch is not None:
            async with db.execute(
                    "SELECT discord_id FROM guilds WHERE is_available = 1 "
                    "AND discord_id IN (SELECT guild_discord_id FROM settings WHERE alias = ? AND value = 1)",
                    (switch,),
            ) as cursor:
                return [guild[0] for guild in await cursor.fetchall()]
        else:
            async with db.execute(
                    "SELECT discord_id FROM guilds WHERE is_available = 1",
            ) as cursor:
                return [guild[0] for guild in await cursor.fetchall()]


async def set_switch(guild_id: int, alias: str, value: bool) -> bool:
    """
    Update local guild settings in bot dabatase
    :param guild_id: Discord id of local server
    :param alias: Setting alias
    :param value: New value
    :return: Returns new value of switch
    """
    logger.debug("Setting switch %s to %s in %s", alias, value, guild_id)
    await check_guild(guild_id)

    async with aiosqlite.connect(PATH) as db:
        await db.execute(
            """INSERT INTO settings(guild_discord_id, alias, value) VALUES(?, ?, ?)
   ON CONFLICT(guild_discord_id, alias) DO UPDATE SET value=?""",
            (guild_id, alias, int(value), int(value)),
        )
        await db.commit()
        return value


async def set_role(guild_id: int, role_alias: str, value: Optional[int]):
    logger.debug("Setting role %s to %s at %s", role_alias, value, guild_id)
    await check_guild(guild_id)

    async with aiosqlite.connect(PATH) as db:
        if value is not None:
            await db.execute(
                """INSERT INTO roles(guild_discord_id, alias, role_id) VALUES(?, ?, ?)
           ON CONFLICT(guild_discord_id, alias) DO UPDATE SET role_id=?""",
                (guild_id, role_alias, value, value),
            )
        else:
            await db.execute(
                """DELETE FROM roles WHERE guild_discord_id = ? AND alias = ?""",
                (guild_id, role_alias),
            )
        await db.commit()
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

    async with aiosqlite.connect(PATH) as db:
        await db.execute(
            """DELETE FROM ROLES WHERE role_id = ?""",
            (role_id,),
        )
        await db.commit()
        return True


async def verify_guild(guild_id: int):
    logger.info("Verifying %s guild", guild_id)
    await check_guild(guild_id)

    async with aiosqlite.connect(PATH) as db:
        await db.execute(
            """UPDATE guilds SET is_verified = 1 WHERE discord_id = ?""",
            (guild_id,),
        )
        await db.commit()
        return True


async def unverify_guild(guild_id: int):
    logger.debug("Unverifying %s guild", guild_id)
    await check_guild(guild_id)

    async with aiosqlite.connect(PATH) as db:
        await db.execute(
            """UPDATE guilds SET is_verified = 0 WHERE discord_id = ?""",
            (guild_id,),
        )
        await db.commit()
        return True


async def activate_guild(guild_id):
    """
    Insert guild into database, if not exist - updates and sets is_available to True
    """
    logger.debug("Activating %s", guild_id)
    async with aiosqlite.connect(PATH) as db:
        await db.execute(
            """INSERT INTO guilds(discord_id, is_available, is_verified, banned) VALUES(?, 1, 0, 0)
       ON CONFLICT(discord_id) DO UPDATE SET is_available=1;""",
            (guild_id,),
        )
        await db.commit()
        return True


async def deactivate_guild(guild_id):
    """
    Insert guild into database with is_available=0, if not exist - updates and sets is_available to False
    """
    logger.debug("Deactivating %s", guild_id)
    async with aiosqlite.connect(PATH) as db:
        await db.execute(
            """INSERT INTO guilds(discord_id, is_available, is_verified, banned) VALUES(?, 0, 0, 0)
       ON CONFLICT(discord_id) DO UPDATE SET is_available=0;""",
            (guild_id,),
        )
        await db.commit()
        return True


async def check_guild(guild_id):
    """
    Check if row with given guild id exists and fix it if it's not
    """
    # TODO: Make it decorator

    async with aiosqlite.connect(PATH) as db:
        async with db.execute(
                "SELECT * FROM guilds WHERE discord_id = ? AND is_available = 1",
                (guild_id,),
        ) as cursor:
            if bool(await cursor.fetchone()):
                return True
            else:
                return await activate_guild(guild_id)


async def wipe_guild_data(guild_id):
    """
    Delete all data from database with given id
    """
    async with aiosqlite.connect(PATH) as db:
        async with db.execute(
                "DELETE FROM guilds WHERE discord_id = ?",
                (guild_id,),
        ) as cursor:
            await db.commit()
        async with db.execute(
                "DELETE FROM roles WHERE guild_discord_id = ?",
                (guild_id,),
        ) as cursor:
            await db.commit()
        async with db.execute(
                "DELETE FROM settings WHERE guild_discord_id = ?",
                (guild_id,),
        ) as cursor:
            await db.commit()

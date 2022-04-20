from dataclasses import dataclass
from typing import Optional, Dict

import aiosqlite

from plasmosync import settings


async def setup(path="./plasmosync/data.db") -> bool:
    """
    Check if database is ready for use, updates columns if not
    """
    print(path)
    ...


async def is_guild_verified(guild_id: int) -> bool:
    return False


async def get_guild_switches(guild_id: int) -> Dict[str, bool]:
    ...


async def get_guild_roles(guild_id: int) -> Dict[str, int]:
    ...


async def verify_guild(guild_id: int) -> bool:  # TODO: Verify guild
    ...


async def unverify_guild(guild_id: int) -> bool:  # TODO: Unverify guild
    ...


async def set_switch(guild_id: int, alias: str, value: bool) -> bool:
    ...


async def set_role(guild_id: int, role_alias: str, value: Optional[int]) -> bool:
    ...

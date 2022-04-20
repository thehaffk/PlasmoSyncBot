from typing import List

import disnake

from plasmosync.settings import DONOR
from plasmosync.utils.database import is_guild_verified


async def autocomplete_setrole(inter: disnake.ApplicationCommandInteraction, value: str) -> List[str]:
    ...


async def autocomplete_resetrole(inter: disnake.ApplicationCommandInteraction, value: str) -> List[str]:
    ...

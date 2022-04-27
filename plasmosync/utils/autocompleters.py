from typing import List

import disnake

from plasmosync.utils.database import is_guild_verified, get_guild_roles


async def autocomplete_set_role(
    inter: disnake.ApplicationCommandInteraction, value: str
) -> List[str]:
    # TODO
    ...


async def autocomplete_reset_role(
    inter: disnake.ApplicationCommandInteraction, value: str
) -> List[str]:
    # TODO
    guild_roles = await get_guild_roles(inter.guild_id)
    ...

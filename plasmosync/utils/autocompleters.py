import disnake

from plasmosync.settings import DONOR
from plasmosync.utils.database import is_guild_verified, get_guild_roles


async def autocomplete_set_role(
    inter: disnake.ApplicationCommandInteraction, value: str
) -> dict[str, str]:
    guild_id = inter.guild.id
    guild_is_verified = await is_guild_verified(guild_id)

    autocomplete_results = {}
    guild_roles = await get_guild_roles(guild_id)
    for role in guild_roles:
        role = DONOR.roles_by_aliases[role]
        if not role.verified_servers_only or (
            guild_is_verified and role.verified_servers_only
        ):
            autocomplete_results[role.name] = role.alias

    return autocomplete_results


async def autocomplete_reset_role(
    inter: disnake.ApplicationCommandInteraction, value: str
) -> dict[str, str]:
    guild_id = inter.guild.id
    guild_is_verified = await is_guild_verified(guild_id)

    autocomplete_results = {}
    guild_roles = await get_guild_roles(guild_id)
    for role in guild_roles:
        role = DONOR.roles_by_aliases[role]
        if (
            not role.verified_servers_only
            or (guild_is_verified and role.verified_servers_only)
        ) and guild_roles[role.alias] is not None:
            autocomplete_results[role.name] = role.alias

    return autocomplete_results

from __future__ import annotations

from typing import Union, Type

import disnake

from plasmosync.utils.database import get_guild_roles, remove_role_by_id
from plasmosync.config import PlasmoRP, PlasmoSMP


def build_progressbar(cursor: int, total_count: int) -> str:
    """
    Build progressbar with given numbers

    :return: string with 🟥 and 🟩
    """
    if total_count < 10:
        cursor *= 10
        total_count *= 10

    if total_count == 0 or total_count == cursor:
        return "🟩" * 10

    return "🟩" * int((cursor // (total_count // 10))) + "🟥" * (10 - int((cursor // (total_count // 10))))


async def get_roles_difference(
        donor: Type[PlasmoRP] | Type[PlasmoSMP], user: disnake.Member, donor_user: disnake.Member
) -> tuple[list[disnake.Role, None], list[disnake.Role, None]]:
    """
    Compares roles at
    :param donor: Configs for donor
    :param user: Users to sync
    :param donor_user:  Member objects from plasmo guild

    :return: Two tuples of integers - roles to add, roles to remove
    """
    guild_roles = await get_guild_roles(user.guild.id)

    roles_to_remove = []
    roles_to_add = []
    for role_alias in guild_roles.keys():
        local_role_id = guild_roles[role_alias]
        local_role = user.guild.get_role(local_role_id)
        donor_role = donor_user.guild.get_role(
            donor.roles_by_aliases[role_alias].discord_id
        )

        if local_role is None and local_role_id is not None:
            await remove_role_by_id(local_role_id)
            continue

        user_has_donor_role = donor_role in donor_user.roles
        user_has_local_role = local_role in user.roles

        if user_has_donor_role == user_has_local_role:
            continue
        elif user_has_local_role:
            roles_to_remove.append(local_role)
        else:
            roles_to_add.append(local_role)
    return roles_to_add, roles_to_remove

from __future__ import annotations

import logging
import sqlite3
from typing import Dict, Optional, Tuple, List, Union

import disnake
from aiohttp import ClientSession
from disnake import Role
from disnake.ext import commands

from plasmosync import settings, config
from plasmosync.utils import database
from plasmosync.config import PlasmoRP, PlasmoSMP

logger = logging.getLogger(__name__)


async def get_roles_difference(
    donor: Union[PlasmoRP, PlasmoSMP], user: disnake.Member, donor_user: disnake.Member
) -> tuple[list[Role | None], list[Role | None]]:
    """
    Compares roles at
    :param donor: Configs for donor
    :param user: Users to sync
    :param donor_user:  Member objects from plasmo guild

    :return: Two tuples of integers - roles to add, roles to remove
    """
    guild_roles = await database.get_guild_roles(user.guild.id)

    roles_to_remove = []
    roles_to_add = []

    for role_alias, local_role_id in guild_roles:
        local_role = user.guild.get_role(local_role_id)

        user_has_donor_role = (
            donor_user.guild.get_role(donor.roles_by_aliases[role_alias])
            in donor_user.roles
        )
        user_has_local_role = (
            user.guild.get_role(donor.roles_by_aliases[role_alias]) in user.roles
        )

        if user_has_donor_role == user_has_local_role:
            continue
        elif user_has_local_role:
            roles_to_remove.append(local_role)
        else:
            roles_to_add.append(local_role)

        return roles_to_add, roles_to_remove


class Synchronization(commands.Cog):
    """
    Main cog for user synchronization
    """

    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    async def sync(self, user: disnake.Member) -> bool:
        ...
        donor_config = settings.DONOR
        user_guild = user.guild

        # Check if user_guild is verified
        is_guild_verified: bool = await database.is_guild_verified(user_guild.id)

        # Get current user_guild settings, donor user_guild and member object from donor
        guild_settings: Dict[str, bool] = await database.get_guild_switches(
            user_guild.id
        )
        donor_guild = self.bot.get_guild(donor_config.guild_discord_id)
        donor_user: Optional[disnake.Member] = donor_guild.get_member(user.id)

        # If user_guild is verified and whitelist enabled
        #   check user`s pass and kick if it's a guest
        if (
            is_guild_verified
            and guild_settings.get(
                donor_config.whitelist.alias, donor_config.whitelist.default
            )
            is True
        ):
            if donor_user is None or not donor_user.has_role(
                donor_config.player_role.discord_id
            ):
                try:
                    await user.kick(reason="Whitelist is enabled, use /settings to disable")
                except disnake.Forbidden as error:
                    logger.warning(
                        "Could not kick user %s from %s because of \n %s",
                        user,
                        user.guild,
                        error,
                    )
                    # TODO: Log that into dev-error-channel

        # if user is on donor:
        if donor_user is not None:
            #   If sync roles is enabled
            if guild_settings.get(
                donor_config.sync_roles.alias, donor_config.sync_roles.default
            ):
                roles_to_add, roles_to_remove = get_roles_difference(
                    donor_config, user, donor_user
                )
                # TODO: edit user roles + add error logger

            if guild_settings.get(
                donor_config.sync_nicknames.alias,
                donor_config.sync_nicknames.default,
            ):
                nickname = donor_user.display_name
                try:
                    await user.edit(nick=nickname, reason="Sync roles switch is enabled, use /settings to disable")
                except disnake.Forbidden as error:
                    logger.warning("Unable to update %s local nickname at %s, error \n %s", user, user.guild, error)

        elif is_guild_verified:
            if guild_settings.get(
                donor_config.sync_bans.alias,
                donor_config.sync_bans.default,
            ):
                # Kinda heavy, TODO: rewrite if possible
                for ban in await donor_guild.bans():
                    if ban.user.id == user.id:
                        try:
                            await user.ban(delete_message_days=0, reason="Sync bans (privileged) is enabled, use /setting to disable")
                        except disnake.Forbidden as error:
                            logger.warning("Unable to ban %s in %s, error \n %s", user, user.guild,
                                           error)
                        break

            if guild_settings.get(
                donor_config.use_api.alias,
                donor_config.use_api.default,
            ):
                return await self._sync_via_api(user=user, guild_switches=guild_settings)

        return True


    async def _sync_via_api(
        self, user: disnake.Member, guild_switches: Dict[str, bool]
    ) -> bool:
        # We already know that guild is verified, so there is no reason to check it again
        donor = settings.DONOR
        guild = user.guild

        if donor.api_base_url is None:
            return False

        # TODO: this
        # We know that sync nicknames or sync roles is enabled, so we must do an api call before config checks

        #   If sync nicknames
        #       get user nick
        #       sync nick
        #   If sync roles9
        #       get guild roles
        #       get user roles from api response
        #       unsync roles
        #       sync roles
        #       if banned role is set
        #           sync ban role


def setup(client):
    client.add_cog(Synchronization(client))
    logger.info("Loaded Synchronization")

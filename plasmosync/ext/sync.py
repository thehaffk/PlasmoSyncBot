from __future__ import annotations

import asyncio
import logging
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
    for role_alias in guild_roles.keys():
        local_role_id = guild_roles[role_alias]
        local_role = user.guild.get_role(local_role_id)
        donor_role = donor_user.guild.get_role(
            donor.roles_by_aliases[role_alias].discord_id
        )

        if local_role is None:
            await database.remove_role_by_id(user.guild.id, local_role_id)
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


class Synchronization(commands.Cog):
    """
    Main cog for user synchronization
    """

    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    async def sync(self, user: disnake.Member) -> bool:
        """
        Sync user
        :param user:
        :return: True if successfully synced, False if there were errors during syncing
        """
        ...
        donor_config = settings.DONOR
        user_guild = user.guild
        sync_status = True

        logger.info("Syncing %s at %s", user, user_guild)

        # Checks if user_guild is verified
        is_guild_verified: bool = await database.is_guild_verified(user_guild.id)

        # Get current user_guild settings, donor user_guild and member object from donor
        guild_settings: Dict[str, bool] = await database.get_guild_switches(
            user_guild.id
        )
        donor_guild = self.bot.get_guild(donor_config.guild_discord_id)
        donor_user: Optional[disnake.Member] = donor_guild.get_member(user.id)

        # If user_guild is verified and whitelist enabled
        #   checks user`s pass and kicks him if it's a guest
        if is_guild_verified and guild_settings.get("whitelist", False) is True:
            if donor_user is None or donor_config.player_role.discord_id not in [
                role.id for role in donor_user.roles
            ]:
                try:
                    await user.kick(
                        reason="Whitelist is enabled, use /settings to disable"
                    )
                except disnake.Forbidden as error:
                    logger.warning(
                        "Could not kick user %s from %s because of \n %s",
                        user,
                        user.guild,
                        error,
                    )
                    sync_status = False
                    # TODO: Log that into dev-error-channel

        # if user is on donor:
        if donor_user is not None:
            #   If sync roles is enabled
            if guild_settings.get("sync_roles", False):
                roles_to_add, roles_to_remove = await get_roles_difference(
                    donor_config, user, donor_user
                )
                try:
                    await user.add_roles(
                        *roles_to_add,
                        reason="Roles sync is enabled,"
                               " use /settings to disable",
                    )
                    await user.remove_roles(
                        *roles_to_remove,
                        reason="Roles sync is enabled,"
                               " use /settings to disable",
                    )
                except disnake.Forbidden as error:
                    sync_status = False
                    logger.warning(error)

            if guild_settings.get(
                "sync_nicknames",
                False,
            ):
                nickname = donor_user.display_name
                try:
                    await user.edit(
                        nick=nickname,
                        reason="Nicknames sync is enabled,"
                               " use /settings to disable",
                    )
                except disnake.Forbidden as error:
                    logger.warning(
                        "Unable to update %s local nickname at %s, error \n %s",
                        user,
                        user.guild,
                        error,
                    )
                    sync_status = False

        elif is_guild_verified:
            if guild_settings.get(
                "sync_bans",
                False,
            ):
                # Kinda heavy, TODO: rewrite if possible
                for ban in await donor_guild.bans():
                    if ban.user.id == user.id:
                        try:
                            await user.ban(
                                delete_message_days=0,
                                reason="Sync bans (privileged) is enabled,"
                                       " use /setting to disable",
                            )
                        except disnake.Forbidden as error:
                            logger.warning(
                                "Unable to ban %s in %s, error \n %s",
                                user,
                                user.guild,
                                error,
                            )
                            sync_status = False
                        break

            if guild_settings.get(
                donor_config.use_api.alias,
                donor_config.use_api.default,
            ):
                return await self._sync_via_api(
                    user=user, guild_switches=guild_settings
                )

        return sync_status

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


def setup(bot):
    """
    Setup function?
    :param bot: discord bot client
    """
    bot.add_cog(Synchronization(bot))
    logger.info("Loaded Synchronization")

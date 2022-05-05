import logging

import disnake
from disnake.ext import commands

from plasmosync import settings, config

logger = logging.getLogger()


class PlasmoSync(commands.Bot):
    """
    Base bot instance.
    """

    def __init__(self, *args, **kwargs):
        if settings.DEBUG is True:
            kwargs["test_guilds"] = config.TEST_GUILDS
            logger.warning("registering as test_guilds")
        super().__init__(*args, **kwargs)

    @classmethod
    def create(cls) -> "PlasmoSync":
        """Create and return an instance of a Bot."""
        _intents = disnake.Intents.none()
        _intents.members = True
        _intents.bans = True
        _intents.dm_messages = True  # ????
        _intents.guilds = True

        return cls(
            owner_ids=config.OWNERS,
            status=disnake.Status.do_not_disturb,
            intents=_intents,
            sync_commands=True,
            sync_permissions=True,
            command_prefix=commands.when_mentioned,
            allowed_mentions=disnake.AllowedMentions(everyone=False),
            activity=disnake.Game(
                name="Synchronizes nicknames and roles with Plasmo,"
                " made by Plasmo R&D [howkawgew]"
            ),
        )

    async def on_ready(self):
        logger.info(f"Logged in as {self.user}")
        if (donor_guild := self.get_guild(settings.DONOR.guild_discord_id)) is None:
            logger.critical("Unable to connect to donor guild")
            return
        else:
            logger.info("Connected donor guild as: %s %s", donor_guild, donor_guild.id)
            for role in settings.DONOR.roles:
                if (discord_role := donor_guild.get_role(role.discord_id)) is None:
                    logger.critical("Unable to get %s role in donor (Config: %s)", role.name, role.discord_id)
                    return
            logger.info("Donor config is valid")
            logger.info("Loaded %s/%s roles", len(settings.DONOR.roles), len(settings.DONOR.roles))


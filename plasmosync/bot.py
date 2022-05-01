import logging

import disnake
from disnake.ext import commands

from plasmosync import settings, config

logger = logging.getLogger()

__all__ = "bot"


class PlasmoSync(commands.Bot):
    """
    Base bot instance.
    """

    def __init__(self, *args, **kwargs):
        if settings.DEBUG is True:
            kwargs["test_guilds"] = settings.TEST_GUILDS
            logger.warning("registering as test_guilds")
        super().__init__(*args, **kwargs)

    @classmethod
    def create(cls) -> "PlasmoSync":
        """Create and return an instance of a Bot."""
        _intents = disnake.Intents.none()
        _intents.members = True
        _intents.bans = True
        _intents.dm_messages = True
        _intents.emojis_and_stickers = True
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

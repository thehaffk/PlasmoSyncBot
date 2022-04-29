import logging

import disnake
from disnake.ext import commands

logger = logging.getLogger(__name__)


class Listeners(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    # TODO:
    #  - on_member_ban
    #  - on_member_unban
    #  - on_member_update
    #  - on_member_join
    #  - on_member_leave
    #  - on_member_update

    async def cog_load(self) -> None:
        logger.info("Loaded %s", __name__)


def setup(client):
    client.add_cog(Listeners(client))

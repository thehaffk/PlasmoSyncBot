import asyncio
import logging

from plasmosync import log
from plasmosync import config
from plasmosync.bot import PlasmoSync
from plasmosync.utils import database

log.setup()

bot = PlasmoSync.create()
logger = logging.getLogger(__name__)

# bot.load_extension("plasmosync.ext.core")
bot.load_extensions("plasmosync/ext")
asyncio.run(database.setup())

bot.run(config.TOKEN)

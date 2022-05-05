import logging

import sys

from plasmosync import log
from plasmosync import config
from plasmosync.bot import PlasmoSync

log.setup()

bot = PlasmoSync.create()
logger = logging.getLogger(__name__)

# bot.load_extension("plasmosync.ext.core")
bot.load_extensions("plasmosync/ext")

bot.run(config.TOKEN)

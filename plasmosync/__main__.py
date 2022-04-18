import aiohttp

from plasmosync.bot import PlasmoSync
from plasmosync import  log
from plasmosync import settings

log.setup()

bot = PlasmoSync.create()
bot.load_extensions("plasmosync/ext")
bot.run(settings.TOKEN)

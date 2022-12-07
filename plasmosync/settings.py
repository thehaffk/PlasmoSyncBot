from __future__ import annotations

import logging
from typing import Type

from plasmosync import config
from plasmosync.config import PlasmoRP, PlasmoSMP

logger = logging.getLogger(__name__)

DEBUG = True
DONOR: Type[PlasmoRP] | Type[PlasmoSMP] = PlasmoRP
DATABASE_PATH = "plasmosync/data.db"

if DONOR not in [PlasmoRP, PlasmoSMP]:
    raise ValueError("???? Pepega")

if not all(
        [value in DONOR.settings_by_aliases for value in ["sync_nicknames", "sync_roles"]]
):
    raise ValueError("Missing required settings")

if not DEBUG and config.DEVMODE:
    logger.warning(
        "Debug is deactivated, but developer mode is not, BOT WILL REGISTER COMMANDS ONLY IN DEV GUILDS"
    )

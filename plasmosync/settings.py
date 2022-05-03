from __future__ import annotations
import os
from typing import Union, Type

from dotenv import load_dotenv

from plasmosync.config import PlasmoRP, PlasmoSMP, PlasmoFRP

load_dotenv()

DEBUG = True
TOKEN = os.getenv("BOT_TOKEN")
TEST_GUILDS = [966785796902363188, 828683007635488809]
DONOR: Type[PlasmoRP] | Type[PlasmoSMP] | Type[PlasmoFRP] = PlasmoRP

if DONOR not in [PlasmoRP, PlasmoSMP, PlasmoFRP]:
    raise ValueError("???? Pepega")

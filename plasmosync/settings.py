import os
from dataclasses import dataclass
from typing import Optional, Union

from dotenv import load_dotenv

from config import PlasmoRP, PlasmoSMP

load_dotenv()

DEBUG = True
TOKEN = os.getenv("BOT_TOKEN")
TEST_GUILDS = [828683007635488809]
DONOR: Union[PlasmoRP, PlasmoSMP] = PlasmoRP





from __future__ import annotations

from typing import Type

from plasmosync.config import PlasmoRP, PlasmoSMP, PlasmoFRP

DEBUG = True
DONOR: Type[PlasmoRP] | Type[PlasmoSMP] | Type[PlasmoFRP] = PlasmoRP

if DONOR not in [PlasmoRP, PlasmoSMP, PlasmoFRP]:
    raise ValueError("???? Pepega")

if not all([value in DONOR.settings_by_aliases for value in ['sync_nicknames', "sync_roles"]]):
    raise ValueError("Missing required settings")

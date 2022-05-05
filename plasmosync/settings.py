from __future__ import annotations

from typing import Type

from plasmosync.config import PlasmoRP, PlasmoSMP, PlasmoFRP

DEBUG = True
DONOR: Type[PlasmoRP] | Type[PlasmoSMP] | Type[PlasmoFRP] = PlasmoRP

if DONOR not in [PlasmoRP, PlasmoSMP, PlasmoFRP]:
    raise ValueError("???? Pepega")

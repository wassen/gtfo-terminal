#!/usr/bin/env python
# -*- coding:utf-8 -*-

from enum import Enum, auto
from typing import Dict, Optional


class ItemProperty(Enum):
    pass


temp_item_properties: Dict[ItemProperty, Optional[int]]


class ItemType(ItemProperty):
    ammo = 1
    medi = 2
    tool = 3
    disinfection = 4
    fog_repeller = 5
    long_range_flashlight = 6
    c_form_granade = 7
    lock_melter = 8
    glow_stick = 9
    l2_lp_syringe = 10
    iix_syringe = 11
    explosive_tripmine = 12
    c_form_tripmine = 13

    @property
    def itemName(self) -> str:
        if self == ItemType.ammo:
            return "Ammunition Pack"
        elif self == ItemType.medi:
            return "Medical Pack"
        elif self == ItemType.tool:
            return "Tool Refill Pack"
        elif self == ItemType.disinfection:
            return "Disinfection Pack"
        else:
            return "None"

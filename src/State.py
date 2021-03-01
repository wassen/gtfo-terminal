#!/usr/bin/env python
# -*- coding:utf-8 -*-

from enum import Enum, auto
from typing import Optional


class AddState(Enum):
    item = auto()
    zone = auto()
    container = auto()


add_state: Optional[AddState] = None


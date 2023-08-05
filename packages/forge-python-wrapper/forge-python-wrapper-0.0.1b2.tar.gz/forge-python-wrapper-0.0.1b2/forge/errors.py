# -*- coding: utf-8 -*-

"""documentation placeholder"""

from __future__ import absolute_import

from .base import ForgeBase


two_legged = "The BIM 360 API only supports 2-legged access token."
hub_id = "A 'app.hub_id' has not been defined."
bim360_hub = "The 'app.hub_id' must be a {} hub.".format(
    ForgeBase.BIM_360_TYPES["b."]
)

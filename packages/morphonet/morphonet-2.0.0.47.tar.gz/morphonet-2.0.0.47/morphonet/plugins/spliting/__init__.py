# -*- coding: latin-1 -*-
defaultPlugins=[]

from .splitInTwoDistancePeak import splitInTwoDistancePeak
defaultPlugins.append(splitInTwoDistancePeak())

from .splitOnAxis import splitOnAxis
defaultPlugins.append(splitOnAxis())

from .splitOnRaw import splitOnRaw
defaultPlugins.append(splitOnRaw())
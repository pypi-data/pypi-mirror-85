# -*- coding: latin-1 -*-
defaultPlugins=[]

from .addTemporalLink import addTemporalLink
defaultPlugins.append(addTemporalLink())

from .delTemporalLink import delTemporalLink
defaultPlugins.append(delTemporalLink())
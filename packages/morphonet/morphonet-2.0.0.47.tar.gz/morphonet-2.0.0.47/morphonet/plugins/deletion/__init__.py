from .deleteSelectedObjects import *
from .fuseSelectedObjects import *
from .removeUnder import *


# -*- coding: latin-1 -*-
defaultPlugins=[]

from .fuseSelectedObjects import fuseSelectedObjects
defaultPlugins.append(fuseSelectedObjects())

from .deleteSelectedObjects import deleteSelectedObjects
defaultPlugins.append(deleteSelectedObjects())


from .removeUnder import removeUnder
defaultPlugins.append(removeUnder())

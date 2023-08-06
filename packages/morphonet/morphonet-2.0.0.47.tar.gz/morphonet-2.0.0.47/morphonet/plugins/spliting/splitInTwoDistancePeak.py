# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from .functions import *

class splitInTwoDistancePeak(MorphoPlugin):
    """ This plugin split opbjects based on distance between two Peaks in the segmented image 

    Parameters
    ----------
    Objects: 
        It can be apply either on selected or colored objects

    """
    
    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_Name("Split In 2")
        self.set_Parent("Split objects")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None
            
        from scipy import ndimage as ndi 
        from skimage.morphology import label,watershed
        from skimage.feature import peak_local_max
        import numpy as np
        for cid in objects:
            o=dataset.getObject(cid)
            if o is not None:
                data=dataset.get_seg(o.t)
                cellCoords=np.where(data==o.id)
                self.print_mn('     ----->>>  Split object '+str(o.getName()) + " with "+str(len(cellCoords[0]))+ " voxels ")
                xmin,xmax,ymin,ymax,zmin,zmax=getBorders(data,cellCoords)
                cellShape=[1+xmax-xmin,1+ymax-ymin,1+zmax-zmin]
                mask=np.zeros(cellShape,dtype=np.bool)
                mask[cellCoords[0]-xmin,cellCoords[1]-ymin,cellCoords[2]-zmin]=True
                distance = ndi.distance_transform_edt(mask)
                local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((3, 3, 3)),num_peaks=2)
                markers = ndi.label(local_maxi)[0]
                labelw = watershed(-distance, markers, mask=mask)
                data,newIds=applyNewLabel(data,xmin,ymin,zmin,labelw)
                if len(newIds)>0:
                    dataset.del_link(o)
                    newIds.append(o.id)
                    dataset.set_seg(t,data,newIds)
                
        self.restart()

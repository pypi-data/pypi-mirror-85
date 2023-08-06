# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from .functions import *

class splitOnRaw(MorphoPlugin):
    """ This plugin split opbjects based local maximum found at a miniym distance on the rawdata
    For more information see https://scikit-image.org/docs/dev/auto_examples/segmentation/plot_peak_local_max.html

    Parameters
    ----------
    Objects: 
        It can be apply either on selected or colored objects
    Volume Minimum : int , default 2000
        The minimum accepted volume to create a new object
    Min Distance: int, default 20
        The minmum distance between two peaks in the peak_local_max fucntion
    """

    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_Name("Split On Raw")
        self.add_InputField("Volume Minimum",default=2000)
        self.add_InputField("Min Distance",default=20)
        self.set_Parent("Split objects")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None
            
        from skimage.morphology import label,watershed
        from skimage.feature import peak_local_max
        import numpy as np
        min_distance=int(self.get_InputField("Min Distance"))
        minVol=int(self.get_InputField("Volume Minimum"))
        for cid in objects:
            o=dataset.getObject(cid)
            if o is not None:
                data=dataset.get_seg(o.t) 
                cellCoords=np.where(data==o.id)
                self.print_mn('     ----->>>  Split object '+str(o.getName()) + " with "+str(len(cellCoords[0]))+ " voxels ")
                xmin,xmax,ymin,ymax,zmin,zmax=getBorders(data,cellCoords)
                cellShape=[1+xmax-xmin,1+ymax-ymin,1+zmax-zmin]
                markers=np.zeros(cellShape,dtype=np.uint8) #PREPARE SEEDS FOR WATERSEED
                mask=np.zeros(cellShape,dtype=np.bool)
                mask[cellCoords[0]-xmin,cellCoords[1]-ymin,cellCoords[2]-zmin]=True
                rawdata=dataset.get_raw(o.t)
                rawdata=rawdata[xmin:xmax+1,ymin:ymax+1,zmin:zmax+1]
                rawdata[np.where(mask==False)]=rawdata.max() #Remove where mask is not 
                coordinates = peak_local_max(rawdata.max()-rawdata, min_distance=min_distance,num_peaks=2) 
                self.print_mn("     ----->>>  Found "+str(len(coordinates))+ " peaks ")
                l=1
                for coord in coordinates:
                    markers[coord[0],coord[1],coord[2]]=l
                    l+=1
                labelw=watershed(rawdata,markers, mask=mask)
                
                data,newIds=applyNewLabel(data,xmin,ymin,zmin,labelw,minVol=minVol)
                if len(newIds)>0:
                    dataset.del_link(o)
                    newIds.append(o.id)
                    dataset.set_seg(t,data,newIds)


        self.restart()
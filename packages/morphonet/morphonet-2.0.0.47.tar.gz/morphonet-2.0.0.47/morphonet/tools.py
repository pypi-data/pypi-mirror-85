# -*- coding: latin-1 -*-
import os,sys
import numpy as np
import datetime
from urllib.parse import unquote
from threading import Thread
from os.path import isdir,join,dirname,basename
#****************************************************************** SPECIFC ASTEC FUNCTIONS

#READ AND SAVE IMAGES
def imread(filename):
    """Reads an image file completely into memory

    :Parameters:
     - `filename` (str)

    :Returns Type:
        |numpyarray|
    """
    print(" --> Read "+filename)
    if filename.find('.inr')>0 or filename.find('mha')>0:
        from morphonet.ImageHandling import SpatialImage
        from morphonet.ImageHandling import imread as imreadINR
        return imreadINR(filename)
    elif filename.find('.nii')>0:
        from nibabel import  load as loadnii
        im_nifti = loadnii(filename)
        return im_nifti
    else:
        from skimage.io import imread as imreadTIFF
        return imreadTIFF(filename)
    return None

def imsave(filename,img):
    """Save a numpyarray as an image to filename.

    The filewriter is choosen according to the file extension. 

    :Parameters:
     - `filename` (str)
     - `img` (|numpyarray|)
    """

    print(" --> Save "+filename)
    if filename.find('.inr')>0 or  filename.find('mha')>0:
        from morphonet.ImageHandling import SpatialImage
        from morphonet.ImageHandling import imsave as imsaveINR
        return imsaveINR(filename,img)
    elif filename.find('.nii')>0:
        from nibabel import save as savenii
        #new_img = nib.nifti1.Nifti1Image(img, None, header=header_nifti)
        im_nifti = savenii(img,filename)
        return im_nifti

    else:
        from skimage.io import imsave as imsaveTIFF
        return imsaveTIFF(filename,img)
    return None


class _save_seg_thread(Thread):
    #Just perform the saving in thread
    def __init__(self,segment_path,segment_files,log,data,t,exec_time):
        Thread.__init__(self) 
        self.segment_path=segment_path
        self.segment_files=segment_files
        self.log=log
        self.data=data
        self.t=t
        self.exec_time=exec_time

    def run(self): #START FUNCTION
        filename=join(self.segment_path,self.segment_files.format(self.t))
        if self.log and isfile(filename):
            copy(filename,join(self.segment_path,self.exec_time.strftime("%Y-%m-%d-%H-%M-%S")+"_"+self.segment_files.format(self.t)))
        compressed=False
        if not isfile(filename) and isfile(filename+".gz"):
            compressed=True
        is_save=imsave(filename,self.data)    
        if compressed:
            os.system("gzip -f "+filename)
       



def _set_dictionary_value(root):
    """

    :param root:
    :return:
    """

    if len(root) == 0:

        #
        # pas de branche, on renvoie la valeur
        #

        # return ast.literal_eval(root.text)
        if root.text is None:
            return None
        else:
            return eval(root.text)

    else:

        dictionary = {}
        for child in root:
            key = child.tag
            if child.tag == 'cell':
                key = np.int64(child.attrib['cell-id'])
            dictionary[key] = _set_dictionary_value(child)

    return dictionary


#Read XML Properties
def read_XML_properties(filename):
    """
    Return a xml properties from a file 
    :param filename:
    :return as a dictionnary
    """
    properties = None
    if not os.path.exists(filename):
        print(' --> properties file missing '+filename)
    elif filename.endswith("xml") is True:
        print(' --> read XML properties from '+filename)
        import xml.etree.ElementTree as ElementTree
        inputxmltree = ElementTree.parse(filename)
        root = inputxmltree.getroot()
        properties= _set_dictionary_value(root)
    else:
        print(' --> unkown properties format for '+filename)
    return properties


def _indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            _indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i



def _set_xml_element_text(element, value):
    """

    :param element:
    :param value:
    :return:
    """
    #
    # dictionary : recursive call
    #   dictionary element may be list, int, numpy.ndarray, str
    # list : may be int, numpy.int64, numpy.float64, numpy.ndarray
    #

    if type(value) == dict:
        # print proc + ": type is dict"
        keylist = value.keys()
        sorted(keylist)
        for k in keylist:
            _dict2xml(element, k, value[k])

    elif type(value) == list:

        #
        # empty list
        #

        if len(value) == 0:
            element.text = repr(value)
        #
        # 'lineage', 'label_in_time', 'all-cells', 'principal-value'
        #

        elif type(value[0]) in (int, float, np.int64, np.float64):
            # element.text = str(value)
            element.text = repr(value)

        #
        # 'principal-vector' case
        #  liste de numpy.ndarray de numpy.float64
        #
        elif type(value[0]) == np.ndarray:
            text = "["
            for i in range(len(value)):
                # text += str(list(value[i]))
                text += repr(list(value[i]))
                if i < len(value)-1:
                    text += ", "
                    if i > 0 and i % 10 == 0:
                        text += "\n  "
            text += "]"
            element.text = text
            del text

        else:
            element.text = repr(value)
            #print( " --> error, element list type ('" + str(type(value[0]))  + "') not handled yet for "+str(value))
            #quit()
    #
    # 'barycenter', 'cell_history'
    #
    elif type(value) == np.ndarray:
        # element.text = str(list(value))
        element.text = repr(list(value))

    #
    # 'volume', 'contact'
    #
    elif type(value) in (int, float, np.int64, np.float64):
        # element.text = str(value)
        element.text = repr(value)

    #
    # 'fate', 'name'
    #
    elif type(value) == str:
        element.text = repr(value)

    else:
        print( " --> element type '" + str(type(value))  + "' not handled yet, uncomplete translation")
        quit()

def _dict2xml(parent, tag, value):
    """

    :param parent:
    :param tag:
    :param value:
    :return:
    """

    #
    # integers can not be XML tags
    #
    import xml.etree.ElementTree as ElementTree
    if type(tag) in (int, np.int64):
        child = ElementTree.Element('cell', attrib={'cell-id': str(tag)})
    else:
        child = ElementTree.Element(str(tag))

    _set_xml_element_text(child, value)
    parent.append(child)
    return parent

def dict2xml(dictionary, defaultroottag='data'):
    """

    :param dictionary:
    :param defaultroottag:
    :return:
    """
    import xml.etree.ElementTree as ElementTree
    if type(dictionary) is not dict:
        print(" --> error, input is of type '" + str(type(dictionary)) + "'")
        return None

    if len(dictionary) == 1:
        roottag = dictionary.keys()[0]
        root = ElementTree.Element(roottag)
        _set_xml_element_text(root, dictionary[roottag])

    elif len(dictionary) > 1:
        root = ElementTree.Element(defaultroottag)
        for k, v in dictionary.items():
            _dict2xml(root, k, v)

    else:
        print(" --> error, empty dictionary ?!")
        return None

    _indent(root)
    tree = ElementTree.ElementTree(root)

    return tree

def write_XML_properties(properties,filename):
    """
    Write a xml properties in a file 
    :param properties:
    :param filename:
    """
    if properties is not None:
        xmltree=dict2xml(properties)
        print(" --> write XML properties in "+filename)
        xmltree.write(filename)
    




#Return t, cell_id from long name : t*10**4+id (to have an unique identifier of cells)
def getidt(idl):
    t=int(int(idl)/(10**4))
    cell_id=int(idl)-int(t)*10**4
    return t,cell_id
def getlongid(t,idc):
    return t*10**4+idc
 

#Return Cell name as string
def getName(t,id):
    return str(t)+","+str(id)

def _getObject(o):
    """ Construct an object (as a tuple) from a string
        
    """
    to=0
    ido=0
    cho=0
    oss=o.split(',')
    if len(oss)==1:
        ido=int(o)
    if len(oss)>1:
        to=int(oss[0])
        ido=int(oss[1])
    if len(oss)>2:
        cho=int(oss[2])
    return (to,ido,cho)



def _getObjects(infos):
        """ Get the list of object from an information data
        
        Parameters
        ----------
        infos : string
            The information data

        Returns
        -------
        objects : list
            List of key/value corresponding to a split of the data

        """
        infos=infos.split('\n')
        objects={}
        for line in infos:
            if len(line)>0 and line[0]!="#":
                if line.find("type")==0:
                    dtype=line
                else:
                    tab=line.split(":")
                    ob=_getObject(tab[0])
                    if ob in objects: #Multiple times the same value (we put in list)
                        val1=objects[ob]
                        if type(val1)!=list :
                            objects[ob]=[]
                            objects[ob].append(val1)
                        objects[ob].append(tab[1])
                        #print(objects[tab[0]])
                    else:
                        objects[ob]=tab[1]
        return objects



def _getType(infos):
        """ Get the type from an information data
        
        Parameters
        ----------
        infos : string
            The information data

        Returns
        -------
        type : string
            the type (float, string, ...)

        """
        infos=infos.split('\n')
        for line in infos:
            if len(line)>0 and line[0]!="#":
                if line.find("type")==0:
                    return line.split(":")[1]
        return None

def _getString(ob):
    return str(ob[0])+","+str(ob[1])+","+str(ob[2])

def _getLastCuration(l):
    if type(l)==list:
        lastD=datetime.datetime.strptime('1018-06-29 08:15:27','%Y-%m-%d %H:%M:%S')
        value=""
        for o in l:
            d=o.split(";")[2] #1 Value, 2 Guy, 3 Date
            d2 = datetime.datetime.strptime(d,'%Y-%m-%d-%H-%M-%S')
            if d2>lastD:
                lastD=d2
                value=o
        return value
    return l


def _getParam(command,p): #Return the value of a specific parameter in http query
    params=unquote(str(command.decode('utf-8'))).split("&")
    for par in params:
        k=par.split("=")[0]
        if k==p:
            return par.split("=")[1].replace('%20',' ')
    return ""



def isfile(filename):
    if os.path.isfile(filename):
        return True
    elif os.path.isfile(filename+".gz"):
        return True
    elif os.path.isfile(filename+".zip"):
        return True
    return False

def copy(filename1,filname2):
    if os.path.isfile(filename1):
        os.system('cp '+filename1+" "+filname2)
    elif os.path.isfile(filename1+".gz"):
        os.system('cp '+filename1+".gz "+filname2+".gz")
    elif os.path.isfile(filename1+".zip"):
        os.system('cp '+filename1+".zip "+filname2+".zip")
    else:
        print("ERROR didn't found to copy "+filename1)

def loadMesh(filename):
    f=open(filename,'r')
    obj=''
    for line in f:
        obj+=line
    f.close()
    return obj


def getObjectsByTime(dataset,objects):
    times=[]
    for cid in objects: #List all time points
        o=dataset.getObject(cid)
        if o is not None and o.t not in times:
            times.append(o.t)
    times.sort() #Order Times
    return times

from vtk import vtkImageImport,vtkDiscreteMarchingCubes,vtkWindowedSincPolyDataFilter,vtkQuadricClustering,vtkDecimatePro,vtkPolyDataReader,vtkPolyDataWriter    
from threading import Thread
_dataToConvert=None
class convertOneToOBJ(Thread):
    def __init__(self, t,elt,Smooth,Decimate,Reduction,path_write,recompute):
        Thread.__init__(self)
        self.t=t
        self.elt = elt
        self.Smooth = Smooth
        self.Decimate = Decimate
        self.Reduction = Reduction
        self.polydata=None
        self.recompute=True
        self.filename=None
        if path_write is not None:
            self.recompute=recompute
            self.filename=os.path.join(path_write,str(t)+'-'+str(elt)+'.vtk')
    def run(self):
        global _dataToConvert
        if not self.recompute:
            self.recompute=self.read()
        if self.recompute:
            #print(" Compute "+str(self.t) +"-"+str(self.elt))
            nx, ny, nz = _dataToConvert.shape
            eltsd=np.zeros(_dataToConvert.shape,np.uint8)
            coord=np.where(_dataToConvert==self.elt)
            #print('     ----->>>>> Create cell '+str(self.elt) + " with "+str(len(coord[0]))+' pixels ')
            eltsd[coord]=255

            data_string = eltsd.tostring('F')
            reader = vtkImageImport()
            reader.CopyImportVoidPointer(data_string, len(data_string))
            reader.SetDataScalarTypeToUnsignedChar()

            reader.SetNumberOfScalarComponents(1)
            reader.SetDataExtent(0, nx - 1, 0, ny - 1, 0, nz - 1)
            reader.SetWholeExtent(0, nx - 1, 0, ny - 1, 0, nz - 1)
            reader.Update()

            #MARCHING CUBES
            contour = vtkDiscreteMarchingCubes()
            contour.SetInputData(reader.GetOutput())
            contour.ComputeNormalsOn()
            contour.ComputeGradientsOn()
            contour.SetValue(0,255)
            contour.Update()
            self.polydata= contour.GetOutput()

            if self.Smooth and self.polydata.GetPoints() is not None:
                smooth_angle=120.0
                smoth_passband=0.01
                smooth_itertations=25
                smoother = vtkWindowedSincPolyDataFilter()
                smoother.SetInputData(self.polydata)
                smoother.SetFeatureAngle(smooth_angle)
                smoother.SetPassBand(smoth_passband)
                smoother.SetNumberOfIterations(smooth_itertations)
                smoother.NonManifoldSmoothingOn()
                smoother.NormalizeCoordinatesOn()
                smoother.Update()
                self.polydata= smoother.GetOutput()


            if self.Decimate and self.polydata.GetPoints() is not None:
                mesh_fineness=1.0
                decimater = vtkQuadricClustering()
                decimater.SetInputData(self.polydata)
                decimater.SetNumberOfDivisions(*np.uint16(tuple(mesh_fineness*np.array(np.array(_dataToConvert.shape)/2))))
                decimater.SetFeaturePointsAngle(30.0)
                decimater.CopyCellDataOn()
                decimater.Update()
                self.polydata= decimater.GetOutput()

            if self.Reduction and self.polydata.GetPoints() is not None:
                decimatePro  = vtkDecimatePro()
                decimatePro.SetInputData(self.polydata)
                decimatePro.SetTargetReduction(0.8) 
                decimatePro.Update()
                self.polydata= decimatePro.GetOutput()
    
    def read(self):
        if os.path.isfile(self.filename):
            #print("Read "+self.filename)
            reader = vtkPolyDataReader()
            reader.SetFileName(self.filename)
            reader.Update()
            self.polydata=reader.GetOutput()
            return False
        return True


    def write(self):
        if self.recompute and self.filename is not None:
            #print("Write "+self.filename)
            writer = vtkPolyDataWriter()
            writer.SetFileName(self.filename)
            writer.SetInputData(self.polydata)
            writer.Update()
 

def convertToOBJ(dataFull,t,background=0,factor=4,Smooth=True,Decimate=True,Reduction=True,center=[0,0,0],cells_updated=None,path_write=None): ####  CONVERT SEGMENTATION IN MESH 
        global _dataToConvert
        _dataToConvert=dataFull[::factor,::factor,::factor]
        elts=np.unique(_dataToConvert)
        elts=elts[elts!=background] #Remove Background
        
        threads=[]
        recompute=path_write is not None and cells_updated is not None
        for elt in elts:
            if recompute:
                tc=convertOneToOBJ(t,elt,Smooth,Decimate,Reduction,path_write,elt in cells_updated)
            else:
                tc=convertOneToOBJ(t,elt,Smooth,Decimate,Reduction,None,True)
            tc.start()
            threads.append(tc)

        #Merge all polydata in one
        obj=""
        shiftFace=1
        for tc in threads:
            tc.join()
            tc.write()

            if tc.polydata.GetPoints() is not None:
                obj+="g "+str(t)+","+str(tc.elt)+"\n"
                if not tc.polydata.GetPoints() is None :
                    for p in range(tc.polydata.GetPoints().GetNumberOfPoints()):
                        v=tc.polydata.GetPoints().GetPoint(p) 
                        obj+='v ' + str(v[0]*factor-center[0]) +' '+str(v[1]*factor-center[1]) +' '+str(v[2]*factor-center[2])+'\n'
                    for f in range(tc.polydata.GetNumberOfCells()):
                        obj+='f ' + str(shiftFace+tc.polydata.GetCell(f).GetPointIds().GetId(0)) +' '+str(shiftFace+tc.polydata.GetCell(f).GetPointIds().GetId(1)) +' '+str(shiftFace+tc.polydata.GetCell(f).GetPointIds().GetId(2))+'\n'
                    shiftFace+=tc.polydata.GetPoints().GetNumberOfPoints()
        return obj


def addslashes(s):
    d = {'"':'\\"', "'":"\\'", "\0":"\\\0", "\\":"\\\\"}
    return ''.join(d.get(c, c) for c in s)


def tryParseInt(value):
    try:
        return int(value), True
    except ValueError:
        return value, False

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

ss=" --> "
def strblue(strs):
    return bcolors.BLUE+strs+bcolors.ENDC
def strred(strs):
    return bcolors.RED+strs+bcolors.ENDC
def strgreen(strs):
    return bcolors.BOLD+strs+bcolors.ENDC

def nodata(data):
    if data=="" or data==[] or len(data)==0:
        return True
    return False
    
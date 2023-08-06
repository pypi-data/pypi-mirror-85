# -*- coding: latin-1 -*-
import os,sys,errno
import numpy as np
from datetime import datetime
from morphonet.tools import _save_seg_thread,imread,imsave,isfile,copy,getidt,getName,_getParam
from os.path import isdir,join,dirname,basename
from morphonet.tools import convertToOBJ,write_XML_properties,read_XML_properties,getlongid
from threading import Thread
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote
from io import BytesIO
import signal

#Class Cell
class _MorphoObject():
    def __init__(self,tid):
        tids=tid.split(",")
        if len(tids)<=1:
            self.t=0
            self.id=int(tids[0])
        else:
            self.t =int(tids[0])
            self.id= int(tids[1])
        if len(tids)>2:
            self.s= int(tids[2]) #Selections
    def getName(self):
        return getName(self.t,self.id)


   
#Class Info
class _MorphoInfo():

    def __init__(self,name,info_type):
        self.name=name
        self.info_type=info_type
        self.data={}
        self.updated=True
       

    def _get_object(self,o):
        for oo in self.data:
            if oo.id==o.id and oo.t==o.t:
                return oo
        return o

    def set(self,k,v):
        self.set_curation(k,v,datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def get_last(self,o):
        if o not in self.data:
            return None
        ks=sorted(self.data[o],reverse=True)
        return self.data[o][ks[0]]

    def get_curation(self,o):
        if o not in self.data:
            return []
        if len(self.data)==1:
            return []
        ks=sorted(self.data[o])
        curated=[]
        for k in ks[:len(ks)-1]:
            curated.append( (self.data[o][k],k) )
        return curated


    def set_curation(self,k,v,d):
        if k not in self.data:
            self.data[k]={}
        self.data[k][d]=v
        self.updated=True

    def del_curation(self,k,v,d):
        if k not in self.data:
            return False

        if d not in self.data[k]:
            return False

        if self.data[k][d]==v:
            del self.data[k][d]
            self.updated=True
            return True
            

        return False



    def get_txt(self,time_begin=-1,time_end=-1):
        Text="#MorphoPlot"+'\n'
        Text+='#'+self.name+'\n'
        Text+="type:"+self.info_type+"\n"
        for o in self.data:
            if ( time_begin==-1 or (time_begin>=0 and o.t>=time_begin) ) and (time_end==-1 or (time_end>=time_begin and o.t<=time_end) ):
                if self.info_type=="time" :
                    daughters=self.get_last(o)
                    for d in daughters:
                        Text+=o.getName()+':'+d.getName()+'\n'
                else:
                    Text+=o.getName()+':'+str(self.get_last(o))+'\n' #TODO GROUP ETC...
        return Text

    def is_curated(self,time_begin=-1,time_end=-1):
        for o in self.data:
            if ( time_begin==-1 or (time_begin>=0 and o.t>=time_begin) ) and (time_end==-1 or (time_end>=time_begin and o.t<=time_end) ):
                if len(self.get_curation(o))>=1:
                    return True
        return False
                    


    def get_curation_txt(self,time_begin=-1,time_end=-1):
        Text="#MorphoPlot"+'\n'
        Text+='#Curation for '+self.name+'\n'
        Text+="type:"+self.info_type+"\n"
        for o in self.data:
            if ( time_begin==-1 or (time_begin>=0 and o.t>=time_begin) ) and (time_end==-1 or (time_end>=time_begin and o.t<=time_end) ):
                listCurated=self.get_curation(o)
                for vd in listCurated:
                    (v,da)=vd
                    if self.info_type=="time":
                        for d in v:
                            Text+=o.getName()+':'+d.getName()+'#'+str(da)+'\n'
                    else:
                        Text+=o.getName()+':'+str(v)+'#'+str(da)+'\n'
        return Text

    def get_dict(self):
        prop={}
        for o in self.data:
            cv=o.t*10**4+o.id
            val=self.get_last(o)
            if self.info_type=='time': #Cell Lineage
                for m in val:
                    mother=m.t*10**4+m.id
                    if m.t<o.t:
                        if mother not in prop:
                            prop[mother]=[]
                        prop[mother].append(cv)
                    else: #Inverse
                        if cv not in prop:
                            prop[cv]=[]
                        prop[cv].append(mother)
            else:
                prop[cv]=val
        return prop

    def write_curation(self,txt_filename):
        print(" --> save "+txt_filename)
        f=open(txt_filename,'w')
        f.write("#Curation for "+self.name+'\n')
        f.write("type:"+self.info_type+"\n")
        for o in self.data:
            listCurated=self.get_curation(o)
            for vd in listCurated:
                (v,d)=vd
                if self.info_type=="time":
                    for ds in v:
                        f.write(o.getName()+':'+ds.getName()+"#"+str(d)+'\n')
                else:
                    f.write(o.getName()+':'+str(v)+"#"+str(d)+'\n')
        f.close()

    def read_curation(self,txt_filename):
        if os.path.isfile(txt_filename):
            f=open(txt_filename,'r')
            for line in f:
                if line.find("#")!=0 and line.find("type")==-1: 
                    p=line.find(":")
                    d=line.find("#")
                    o=self._get_object(_MorphoObject(line[:p]))
                    if self.info_type=="time":
                        od=self._get_object(_MorphoObject(line[p+1:d]))
                        self.set_curation(o,[od],line[d+1:].strip()) #TODO GROUP ETC...
                    else:
                        self.set_curation(o,line[p+1:d],line[d+1:].strip()) #TODO GROUP ETC...

            f.close()



class Dataset():
    """Dataset class automatically created when you specify your dataset path in the seDataset function from Plot()

    Parameters
    ----------
    begin : int
        minimal time point
    end : int 
        maximal time point
    raw : string
        path to raw data file where time digits are in standard format (ex: (:03d) for 3 digits  )(accept .gz)
    segment : string
        path to segmented data file  where time digits are in standard format  (accept .gz)
    log : bool
        keep the log
    background : int
        the pixel value of the background inside the segmented image 
    xml_file : string
        path to the xml propertie files (.xml)
    memory : int
        number of time step keep in memory durig curation (if you have memeory issue, decrease this number)
    """

    def __init__(self,parent,begin=0,end=0,raw=None,segment=None,log=True,background=0,xml_file=None,memory=20):
        self.parent=parent
        self.begin=begin
        self.end=end
        self.log=log
        
    
        #raw data
        self.raw=False
        self.show_raw=None
        self.raw_datas={}  #list of each rawdata time point  
        if raw is not None:
            self.raw=True
            self.raw_path=dirname(raw)+"/"
            if dirname(raw)=="":
                self.raw_path=""
            self.raw_files=basename(raw)

        #Segmentation
        self.seg_datas={}  #list of each segmented time point 
        self.segment_path=""
        self.segment_files="curated_t{:03d}.inr.gz"
        if segment is not None:
            self.segment_path=dirname(segment)+"/"
            if dirname(segment)=="":
                self.segment_path=""
            self.segment_files=basename(segment)
            if self.segment_path!="" and not isdir(self.segment_path):
                os.mkdir(self.segment_path)
        
       

        #LOG 
        if self.log:
            self.log_file=join(self.segment_path,"morpho_log.txt")
    

        self.background=background #Background Color
            
        #DATA Management
        self.memory=memory #Memory to store dataset in Gibabytes
        self.lasT=[] #List of last time step
        self.times=[] #List of modified time point 
        
        #INFOS
        self.infos={} #For all infos Infos 
        self._read_properties(xml_file)  #Lineage Initialisation

        self.seeds=None #To Send Centers to Unity

        #Cell to update
        self.cells_updated={}

    def print_mn(self,msg):
        """Print a string on the 3D viewer

        Parameters
        ----------
        msg : string
            your message to print 
       
        """
        self.parent.print_mn(msg)

    def save_log(self,command,exec_time):
        """Save the specitic command in the log file 

        Parameters
        ----------
        command : string
            Executed Command
        exec_time : float
            time of execution 

        Examples
        --------
        >>> dataset.save_log("fuse",date)
        """

        if self.log :
            f=open(self.log_file,"a")
            f.write(str(command)+" # "+str(exec_time.strftime("%Y-%m-%d-%H-%M-%S"))+"\n")
            f.close()

    def restart(self,plug):  #Apply and Restart a Curation 
        """Restart the curation mode after execution of a specific plugin

        Parameters
        ----------
        plug : MorphoPlug
            the plugin just executed

        Examples
        --------
        >>> dataset.restart(fuse)
        """

        if plug is not None:
            print(" --> Done " +str(plug.name))
            for t in self.times:
                self._save_seg(t,plug.exec_time)
        
        self.parent.restart(self.times)
       
    
    #OBJECT ACCESS
    def getObject(*args):
        """Get an MorphoObject from a list of arguments (times, id, ... )

        Parameters
        ----------
        *args : list of arugemnts 
            the arguments which define the object, with at least 1 argument (object id with time =0 )

        Return 
        ----------
        MorphoObject class 

        Examples
        --------
        >>> dataset.getObject(1,2)
        """
        if len(args) == 2:
            if args[1]=="":
                return None
            return _MorphoObject(args[1])
        elif len(args) == 3:
            return _MorphoObject(getName(args[1],args[2]))
        return None
        

    ##### DATA ACCESS 
    def _setLast(self,t):
        if t in self.lasT:
            self.lasT.remove(t)
        self.lasT.append(t)
        if t not in self.seg_datas:
            if self._getDataSize()>self.memory*10**9:
                remove_t=self.lasT.pop(0)
                if remove_t in self.seg_datas:
                    del self.seg_datas[remove_t]
                if remove_t in self.raw_datas:
                    del self.raw_datas[remove_t] 

    def _getDataSize(self):
        sif=0
        for t in self.seg_datas:
            if self.seg_datas[t] is not None:
                sif+=self.seg_datas[t].nbytes
        return sif

    def _setVolume(self,data,t):
        #Compute new Volumes
        inf=self._get_info('cell_volume',info_type="float")
        factor=4 #Computational Factor to reduce time computation
        dataResize=data[::factor,::factor,::factor]
        cells=np.unique(dataResize)
        cells=cells[cells!=self.background]
        for c in cells:
            prevV=inf.get_last(c)
            newV=len(np.where(dataResize==c)[0])*(factor*factor*factor) 
            if prevV!=newV:
                inf.set(_MorphoObject(getName(t,c)),newV)
        del dataResize

    def set_seg(self,t,data,cells_updated=None):
        """Define the segmented data at a specitic time point

        Parameters
        ----------
        t : int
            the time point 
        data : numpy matrix
            the segmented image
        cells_updated (optional): list
            list of cell just udpated by the plugin (in order to compute faster)

        Examples
        --------
        >>> dataset.set_seg(1,data)
        """

        self.seg_datas[t]=data
        if t not in self.times:
            self.times.append(t)

        self.update_cells(t,cells_updated)

    def update_cells(self,t,cells_updated):
        """Updated list of modified cells given a specific time step

        Parameters
        ----------
        t : int
            the time point 
        cells_updated : list or MorphoObject
            list of cell just udpated by the plugin (in order to compute faster)

        Examples
        --------
        >>> dataset.update_cells(1,[o,d])
        """

        if t not in self.cells_updated:
            self.cells_updated[t]=[]

        if cells_updated is not None:
            for c in cells_updated:
                if c not in self.cells_updated[t]:
                    self.cells_updated[t].append(c)

    def _save_seg(self,t,exec_time,data=None):
        if data is None:
            data=self.seg_datas[t]
        else:
            self.seg_datas[t]=data
        self._setVolume(data,t)

        sst=_save_seg_thread(self.segment_path,self.segment_files,self.log,data,t,exec_time)
        sst.start()

            
    
    def get_raw(self,t):
        """Get the rawdata data at a specitic time point

        Parameters
        ----------
        t : int
            the time point 
        Return
        ----------
        numpy matrix
            the raw data

        Examples
        --------
        >>> dataset.get_raw(1)
        """

        self._setLast(t) #Define the time step as used
        if t not in self.raw_datas:
            self.raw_datas[t]=imread(join(self.raw_path,self.raw_files.format(t)))
        return self.raw_datas[t]

    def get_seg(self,t):
        """Get the segmented data at a specitic time point

        Parameters
        ----------
        t : int
            the time point 

        Return
        ----------
        numpy matrix
            the segmented image

        Examples
        --------
        >>> dataset.get_seg(1)
        """
        self._setLast(t) #Define the time step as used
        if t not in self.seg_datas:
            self.seg_datas[t]=None
            if isfile(join(self.segment_path,self.segment_files.format(t))):
                self.seg_datas[t]=imread(join(self.segment_path,self.segment_files.format(t)))
        return self.seg_datas[t]

    def getCenter(self,data): #Calculate the center of a dataset
        """Get the barycnetr of an matrix passed in argument 

        Parameters
        ----------
        data : numpy matrix
            the 3D image (could be segmented or rawdata) 

        Return
        ----------
        list of coordinates 
            the barycenter of the image 

        Examples
        --------
        >>> center=dataset.getCenter(seg)
        """

        return [np.round(data.shape[0]/2),np.round(data.shape[1]/2),np.round(data.shape[2]/2)]

    def addSeed(self,seed):
        """Add a seed in the seed list

        Parameters
        ----------
        seed : numpy array
            the coordinate of a seed 


        Examples
        --------
        >>> dataset.addSeed(np.int32([23,34,45]))
        """

        if self.seeds is None:
            self.seeds=[]
        self.seeds.append(seed)

    def getSeeds(self):
        """Return the list of seeds as string

        Examples
        --------
        >>> seeds=mc.getSeeds()
        """

        if self.seeds is None or len(self.seeds)==0:
            return None
        strseed=""
        for s in self.seeds:
            strseed+=str(s[0])+","+str(s[1])+","+str(s[2])+";"
        self.seeds=None #Reinitializeation
        return strseed[0:-1]

    ##### LINEAGE FUNCTIONS
    def _read_properties(self,xml_file):
        self._get_info("cell_lineage","time")
        self._get_info("cell_volume","float")
        self.xml_file=xml_file
        if self.xml_file is not None :
            prop_path=os.path.dirname(self.xml_file)
            properties=read_XML_properties(self.xml_file)
            if properties is not None:
                for info_name in properties:
                    prop=properties[info_name]
                    if prop is not None:
                        if info_name!="all_cells":
                            inf=self._get_info(info_name)
                            for idl in prop:
                                t,c=getidt(idl) 
                                mo=_MorphoObject(getName(t,c))
                                if info_name=='cell_lineage':
                                    daughters=[]
                                    for daughter in prop[idl]:
                                        td,d=getidt(daughter)
                                        daughters.append(_MorphoObject(getName(td,d)))
                                    inf.set(mo,daughters)
                                else:
                                    inf.set(mo , prop[idl] )

                            inf.read_curation(join(prop_path,info_name+".log")) #READ CURATION FILE

    def _write_properties(self):
        if self.xml_file is not None:
            properties={}
            prop_path=os.path.dirname(self.xml_file)
            for info_name in self.infos:
                inf=self.infos[info_name]
                properties[info_name]=inf.get_dict()
                if inf.updated:
                    inf.write_curation(join(prop_path,info_name+".log"))
            #Add ALL CELLS
            properties["all_cells"]=[]
            inf=self._get_info("cell_volume")
            for o in inf.data:
                properties["all_cells"].append(getlongid(o.t,o.id))
            write_XML_properties(properties,self.xml_file)

    def _get_info(self,info_name,info_type="string"):
        if info_name not in self.infos:  #Create a new one
            self.infos[info_name]=_MorphoInfo(info_name,info_type)
        return self.infos[info_name]

    ################## TEMPORAL FUNCTIONS 
    def _get_at(self,objects,t):
        cells=[]
        for cid in objects:
            o=self.getObject(cid)
            if o is not None and o.t==t:
                    cells.append(o)
        return cells
    
    def add_link(self,da,mo):
        """Create a temporal link in the lineage

        Parameters
        ----------
        da : MorphoObject
            the daughter cell 
        mo : MorphoObject
            the mother cell 


        Examples
        --------
        >>> mc.add_link(da,mo)
        """
        inf=self._get_info("cell_lineage",info_type="time")
        listCells=inf.get_last(da)
        if listCells is None:
            listCells=[]
        listCells.append(mo)
        inf.set(da,listCells)

    def del_link(self,o): #We remove all links correspond to a cells
        """Remove all temporal relations for a sepcific in the lineage

        Parameters
        ----------
        o : MorphoObject
            the cell 

        Examples
        --------
        >>> mc.del_link(o)
        """
        inf=self._get_info("cell_lineage",info_type="time")
        for a in inf.data:
            if a.t==o.t and a.id==o.id:
                inf.set(a,[])
                #print("Set null to "+str(o.id))
            else:
                listCells=inf.get_last(a)
                if listCells is not None:
                    listCellsB=[]
                    remove=False
                    for c in listCells:
                        if c.t==o.t and c.id==o.id:
                            remove=True
                        else:
                            listCellsB.append(c)                    
                    if remove:
                        #print("Remove links for "+str(a.id))
                        inf.set(a,listCellsB)
            



#****************************************************************** MORPHONET SERVER


class _MorphoServer(Thread):
    def __init__(self,ploti,todo,host="",port=9875):
        Thread.__init__(self) 
        self.ploti=ploti
        self.todo=todo
        self.host=host
        self.port=port
        self.server_address = (self.host, self.port)
        self.available = threading.Event() #For Post Waiting function
        self.lock = threading.Event()
        self.lock.set()
        

    def run(self): #START FUNCTION
        #print("Run server Localhost on the port ", self.port)
        if self.todo=="send":
            handler = _MorphoSendHandler(self.ploti,self)
        else: #recieve
            handler = _MorphoRecieveHandler(self.ploti,self)

        self.httpd = HTTPServer(self.server_address, handler)
        self.httpd.serve_forever()

    def reset(self):
        self.obj = None  
        self.cmd=None  
        self.available = threading.Event() #Create a new watiing process for the next post request
        self.lock.set() #Free the possibility to have a new command

    def wait(self):  #Wait free request to plot (endd of others requests)
        self.lock.wait()

    def post(self,cmd,obj): #Prepare a command to post
        self.lock = threading.Event() #LOCK THE OTHER COMMAND
        self.available.set() 
        self.cmd=cmd
        self.obj=obj
        
    def stop(self):
        self.lock.set()
        self.available.set()
        self.httpd.shutdown()


class _MorphoSendHandler(BaseHTTPRequestHandler):
 
    def __init__(self, ploti,ms):
        self.ploti = ploti
        self.ms=ms
     
    def __call__(self, *args, **kwargs): #Handle a request 
        super().__init__(*args, **kwargs)

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*") #To accept request from morphonet
        self.end_headers()


    def do_GET(self): #NOT USED
        self._set_headers()
        self.wfile.write(b'OK')

    def do_POST(self):
        self.ms.available.wait() #Wait the commnand available
        self._set_headers()
        #print("-> SEND for "+self.ms.cmd)#+"->"+str(self.ms.obj))
        content_length = int(self.headers['Content-Length']) 
        command =self.rfile.read(content_length)
        response = BytesIO()
        #print(command)
        response.write(bytes(self.ms.cmd, 'utf-8'))
        response.write(b';') #ALWAYS ADD A SEPARATOR
        if self.ms.obj is not None:
            if  self.ms.cmd.find("RAW")==0:
                response.write(self.ms.obj)
            else :
                response.write(bytes(self.ms.obj, 'utf-8'))
        self.wfile.write(response.getvalue())
        self.ms.cmd=""
        self.ms.obj=None
        self.ms.reset() #FREE FOR OTHERS COMMAND
        

    def log_message(self, format, *args):
        return

class _MorphoRecieveHandler(BaseHTTPRequestHandler):
 
    def __init__(self, ploti,ms):
        self.ploti = ploti
        self.ms=ms
     
    def __call__(self, *args, **kwargs): #Handle a request 
        super().__init__(*args, **kwargs)


    def _set_headers(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*") #To accept request from morphonet
        self.end_headers()


    def do_GET(self): #NOT USED
        self._set_headers()
        self.wfile.write(b'OK')

    def do_POST(self):
        self._set_headers()
        response = BytesIO() #Read 
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        command =self.rfile.read(content_length)
        action=_getParam(command,"action")
        current_time=int(_getParam(command,"time"))
        objects=_getParam(command,"objects").split(";")
        #print("action="+action)
        if action=="showraw":
            self.ploti.plot_raws(current_time)
        elif action=="upload":
            self.ploti.upload(objects[0],2)
        elif action=="create_curation":
            self.ploti.curate_info(_getParam(command,"info"),_getParam(command,"objects"),_getParam(command,"value"),_getParam(command,"date"))
        elif action=="delete_curation":
            self.ploti.delete_curate_info(_getParam(command,"info"),_getParam(command,"objects"),_getParam(command,"value"),_getParam(command,"date"))
        else:
            actions=unquote(str(command.decode('utf-8'))).split("&")
            for plug in self.ploti.plugins:
                if plug._cmd()==action: #print(" Found Plugin "+plug().cmd())
                    ifo=0 
                    for tf in plug.inputfields:
                        plug._set_InputField(tf,actions[3+ifo][actions[3+ifo].index("=")+1:])
                        ifo+=1
 
                    for dd in plug.dropdowns:
                        plug._set_Dropdown(dd,actions[3+ifo][actions[3+ifo].index("=")+1:])
                        ifo+=1
                    for cd in plug.coordinates:
                        plug._set_Coordinates(cd,actions[3+ifo][actions[3+ifo].index("=")+1:])
                        ifo+=1

                    plug.process(current_time,self.ploti.dataset,objects)

        response.write(bytes("DONE", 'utf-8'))
        self.wfile.write(response.getvalue())
        

    def log_message(self, format, *args):
        return
    
class Plot:#Main function to initalize the plot mode
    """Plot data onto the 3D viewer of the MorphoNet Window.

    Parameters (mostly for debuging )
    ----------
    log : bool
        keep the log
    start_browser : bool
        automatically start the browser when plot initliaze
    port : int
        port number to communicate with the MorphoNet Window. 
    
    Returns
    -------
    MorphoPlot
        return an object of morphonet which will allow you to send data to the MorphoNet Window.


    Examples
    --------
    >>> import morphonet
    >>> mn=morphonet.Plot()

    """

    def __init__(self,log=True,start_browser=True,port_send=9875,port_recieve=9876): 
        
        self.server_send=_MorphoServer(self,"send",port=port_send) #Instantiate the local MorphoNet server 
        self.server_send.start() #

        self.server_recieve=_MorphoServer(self,"recieve",port=port_recieve) #Instantiate the local MorphoNet server 
        self.server_recieve.start() 
    

        if start_browser :
            self.showBrowser()
        self.plugins=[]
        self.log=log        

        signal.signal(signal.SIGINT, self._receiveSignal)

    #########################################  SERVER COMMUNICATION

    def connect(self, login,passwd): #Need to be connected to be upload on MorphoNet 
        """Connect to the MorphoNet server

        In order to directly upload data to the MorphoNet server, you have to enter your MorphoNet credentials

        Parameters
        ----------
        login : string
            your login in MorphoNet
        passwd : string
            your password in MorphoNet

        Examples
        --------
        >>> import morphonet
        >>> mc=morphonet.Plot()
        >>> mc.connect("mylogin","mypassword")
        """
        import morphonet 
        self.mn=morphonet.Net(login,passwd)
     
    def print_mn(self,msg):
        """Print a string on the 3D viewer

        Parameters
        ----------
        msg : string
            your message to print 
       
        Examples
        --------
        >>> mc=print_mn("Hello")
        """
        if msg!="DONE":
            print(msg)
        self.send("MSG",msg)

    def send(self,cmd,obj=None):
        """ Send a command to the 3D viewer

        Examples
        --------
        >>> mc.send("hello")
        """
        self.server_send.wait() #Wait the commnand available
        if cmd is not None:
            cmd=cmd.replace(" ","%20")
        if obj is not None:
            obj=obj.replace(" ","%20")
        self.server_send.post(cmd,obj)

    def quit(self):
        """ Stop communication between the browser 3D viewer and python

        Examples
        --------
        >>> mc.quit()
        """
        self.server_send.stop() #Shut down the server
        self.server_recieve.stop() #Shut down the server

    def upload(self,dataname,upload_factor=2):
        """Create the dataset on MorphoNet server and upload data

        Parameters
        ----------
        dataname : string
            Name of the new dataset on the server
        upload_factor : float
            the scaling attached to the dataset to match the raw data

        Examples
        --------
        >>> ...after starting MorphoPlot and curating the data
        >>> mc.upload("new dataset name",1)
        """
        print("---->>> Upload dataset "+dataname)
        self.mn.createDataSet(dataname,minTime=self.dataset.begin,maxTime=self.dataset.end)
        for t in range(self.dataset.begin,self.dataset.end+1):
            data=self.dataset.get_seg(t)
            if data is not None:
                obj=convertToOBJ(data,t,background=self.dataset.background,factor=upload_factor,cells_updated=None,path_write=self.temp_path)
                self.mn.uploadMesh(t,obj)
        #TODO add Infos
        print("---->>>  Uploading done")

   
    def showBrowser(self): 
        """ Start Mozilla Firefox browser and open morphoplot page
        
        Examples
        --------
        >>> mc.showBrowser()
        """
        import webbrowser
        from morphonet import url
        print("open "+url)
        try:
            webbrowser.get('firefox').open_new_tab("http://"+url+'/morphoplot')
        except Exception as e:
            print("Firefox error: " % e)
            quit()


    def curate(self): #START UPLOAD AND WAIT FOR ANNOTATION
        """ Start sending data to the browser 3D viewer, then wait for annotation from the browser

        Examples
        --------
        >>> mc=morphonet.Plot(start_browser=False)
        >>> mc.setDataset(...)
        >>> mc.curate()
        """
        self.print_mn("Wait for the MorphoNet Windows")
        self.send("START_"+str(self.dataset.begin)+"_"+str(self.dataset.end))
        self.set_default_plugins()  #Initialise Default set of plugins
        self.plot_meshes()
        self.plot_infos()
        self.plot_infos_currated()
        self._reset_infos()
        self.print_mn("DONE")

    def restart(self,times):

        self.dataset._write_properties()

        if times is not None: #PLOT MESHES
            self.plot_meshes(times)

        if self.dataset.show_raw is not None: #PLOT RAWDATAS
            self.plot_raw(self.dataset.show_raw)

        self.plot_seeds(self.dataset.getSeeds()) #PLOT SEEDS
 
        self.plot_infos() #PLOT ALL INFOS
        self._reset_infos()
        self.print_mn("DONE")

    #########################################  DATASET 

    def setDataset(self,begin=0,end=0,raw=None,segment=None,background=0,xml_file=None,factor=4,raw_factor=4,memory=20):
        """ Define a dataset to curate
        
        Parameters
        ----------
        begin : int
            minimal time point
        end : int 
            maximal time point
        raw : string
            path to raw data file where time digits are in standard format (ex: (:03d) for 3 digits  )(accept .gz)
        segment : string
            path to segmented data file  where time digits are in standard format  (accept .gz)
        background : int
            the pixel value of the background inside the segmented image 
        xml_file : string
            path to the xml propertie files (.xml)
        factor : int
            reduction factor when meshes are calculated and send to the MorphoNet window
        raw_factor : int
            raw data reduction factor
        memory : int
            number of time step keep in memory durig curation (if you have memeory issue, decrease this number)

        Examples
        --------
        >>> ...after connection
        >>> mc.setDataset(self,begin=0,end=10,raw=path/to/name_t(:03d).inr.gz,segment=path/to/segmenteddata_t(:03d).inr.gz,xml_file=path/to/properties_file.xml)
        """
        self.dataset=Dataset(self,begin,end,raw=raw,segment=segment,log=self.log,background=background,xml_file=xml_file,memory=memory)
        self.center=None
        self.factor=factor #Reduce factor to compute the obj
        self.raw_factor=raw_factor #Reduction factor

        #Temporary folder
        self.temp_path=".temp_morphonet_"+str(os.path.basename(segment))
        if self.temp_path!="" and not isdir(self.temp_path):
            os.mkdir(self.temp_path)

    ######################################### PLUGINS

    def add_plugin(self,plug):
        """ Add a python plugin to be import in the MorphoNet Window
        
        Parameters
        ----------
        plugin : MorphoPlugin
            A plugin instance

        Examples
        --------
        >>> from plugins.MARS import MARS
        >>> mc.add_plugin(MARS())
        """
        if plug not in self.plugins:
            self.plugins.append(plug)
            self._create_plugin(plug)

    def _create_plugin(self,plug):
        """ Create the plugin in the MorphoNet Window
        
        Parameters
        ----------
        plugin : MorphoPlugin
            A plugin instance
    
        """
        print(" --> create Plugin "+plug.name)
        self.send("BTN",plug._getBtn())
        
    def set_default_plugins(self):
        """ Load the default plugins to the 3D viewer

        Examples
        --------
        >>> mc.set_default_plugins()
        """
        from morphonet.plugins import defaultPlugins
        for plug in defaultPlugins:
            self.add_plugin(plug)


    ######################################### RAWIMAGES 
   
    def plot_raws(self,t):
        """ Enable the possibility to plot raw images to the browser for a specified time point ? 
        
        Parameters
        ----------
        t : int
            time point to display raw images from

        Examples
        --------
        >>> mc.plot_raws(1)
        """
        if self.dataset.raw:
            if self.dataset.show_raw is None or self.dataset.show_raw!=t:
                self.dataset.show_raw=t
                self.restart(None)         

    def plot_raw(self,t):
        """ Compute and send raw images to the browser for a specified time point
        
        Parameters
        ----------
        t : int
            time point to display raw images from

        Examples
        --------
        >>> mc.plot_raw(1)
        """
        if self.dataset.raw:
            print(" --> Send rawdatas at "+str(t))
            rawdata=self.dataset.get_raw(t)
            new_shape=np.uint16(np.floor(np.array(rawdata.shape)/self.raw_factor)*self.raw_factor) #To avoid shifting issue
            rawdata=rawdata[0:new_shape[0],0:new_shape[1],0:new_shape[2]]
            factor_data=rawdata[::self.raw_factor,::self.raw_factor,::self.raw_factor]
            bdata=np.uint8(np.float32(np.iinfo(np.uint8).max)*factor_data/factor_data.max()).tobytes(order="F")        
            if self.center is None:
                self.center=self.dataset.getCenter(rawdata)
            cmd="RAW_"+str(t)+"_"+str(rawdata.shape[0])+"_"+str(rawdata.shape[1])+"_"+str(rawdata.shape[2])+"_"+str(self.raw_factor)+"_"+self._getCenterText()
            self.send(cmd,bdata)

    ######################################### ADDD CENTERS
    
    def plot_seeds(self,seeds):
        """ Plot the cell centers to the browser
        
        Parameters
        ----------
        seeds : string
            the centers of the cells

        Examples
        --------
        >>> mc.plot_seeds(seed_info)
        """
        if seeds is not None and seeds!="":
            self.send("SEEDS",seeds)

    def _getCenterText(self):
        if self.center is not None:
            return str(int(round(self.center[0])))+"_"+str(int(round(self.center[1])))+"_"+str(int(round(self.center[2])))
        return "0_0_0"

    ######################################### PRIMITIVES  
    
    def addPrimitive(self,name,obj): 
        """ Add a primitive using specified content with the specified name to the browser
        
        Parameters
        ----------
        name : string
            the name of the primitive
        obj : bytes
            content of the primitive (3D data)

        Examples
        --------
        >>> #Specify a file on the hard drive by path, with rights
        >>> f = open(filepath,"r+")
        >>> #load content of file inside variable
        >>> content = f.read()    
        >>> mc.addPrimitive("primitive name",content)
        >>> f.close()
        """
        self.send("PRIM_"+str(name),obj)

    ######################################### INFOS 
    
    def _reset_infos(self):
        """
            Reset the updated of all infos 
        """
        if self.dataset.infos is not None:
            for info_name in self.dataset.infos: 
                inf=self.get_info(info_name)
                inf.updated=False

    def plot_infos(self):

        """ Plot all the infos of the datasset
        """

        if self.dataset.infos is not None:
            for info_name in self.dataset.infos: 
                self.plot_info(self.get_info(info_name))

    def plot_info(self,info): #PLOT INFO (CORRESPONDENCAE)
        """ Send the specified informations with the specified name to browser
        
        Parameters
        ----------
        info : Info Class
           the info to plot   

        Examples
        --------
        >>> my_info=mc.get_info("Cell Name")
        >>> mc.plot_infos(my_info)
        """

        
        if info is None:
            return 
        if info.updated:
            print(" --> plot "+info.name)
            info_text=info.get_txt(time_begin=self.dataset.begin,time_end=self.dataset.end) 
            self.send("INFO_"+info.name,info_text)

            
    def plot_infos_currated(self):

        """ Plot all the curation for all the infos of the datasset
        """

        if self.dataset.infos is not None:
            for info_name in self.dataset.infos: 
                self.plot_info_currated(self.get_info(info_name))

    def plot_info_currated(self,info): 
        """ Send the specified currattion for the informations with the specified name to browser
        
        Parameters
        ----------
        info : Info Class
           the info to plot   
        """

        
        if info is None:
            return 
        if info.is_curated():
            curation_txt=info.get_curation_txt(time_begin=self.dataset.begin,time_end=self.dataset.end)
            self.send("CUR_"+info.name,curation_txt)

    def get_info(self,info_name):
        """ Return the info associated to the dataset
        
        Parameters
        ----------
        info_name : string
           the name of the info

        return info : Class info 
            return an object of info 

       
        Examples
        --------  
        >>> my_info=mc.get_info("Cell Name")
        >>> my_info.get_txt() #return the text file
        """
        if info_name in self.dataset.infos:
            return self.dataset.infos[info_name]
        return None

    def create_info(self,info_name,info_type,data=None):
        """ Create an info associated to the dataset
        
        Parameters
        ----------
        info_name : string
           the name of the info
        info_type
            the type of the info (float,string, etc.. )
        data (optional) : List<string>
            information content as a list of all lines 

        Examples
        --------  
        >>> mc.create_info("Cell Name","string")
        """
        inf=self.dataset._get_info(info_name,info_type=info_type)
        if data is not None:
            inf.data=data

    def curate_info(self,info_name,k,v,d):
        """ Apply the curration value of a specific object for the info name 
        
        Parameters
        ----------
        info_name : string
           the name of the info
        k : string
            object to curate
        v : string
            value of curation
        d : string
            date of curation  
        """
        info=self.get_info(info_name)
        o=info._get_object(_MorphoObject(k))
        info.set_curation(o,v,d)
        self.restart(None)

    def delete_curate_info(self,info_name,k,v,d):
        """ Delete the curration value of a specific object for the info name 
        
        Parameters
        ----------
        info_name : string
           the name of the info
        k : string
            object to curate
        v : string
            value of curation
        d : string
            date of curation  
        """
        info=self.get_info(info_name)
        o=info._get_object(_MorphoObject(k))
        if not info.del_curation(o,v,d):
            print(" Error during the deletion of the curation ")
        self.restart(None)

    #########################################  MESH
    def _get_mesh(self,t,data):
        if self.center is None:
            self.center=self.dataset.getCenter(data)
        if t not in self.dataset.cells_updated:
            self.dataset.cells_updated[t]=[]
        obj=convertToOBJ(data,t,background=self.dataset.background,factor=self.factor,center=self.center,cells_updated=self.dataset.cells_updated[t],path_write=self.temp_path) #Create the OBJ
        self.dataset.cells_updated[t]=[]
        return obj  
    
    def plot_mesh(self,t): #UPLOAD DITECLTY THE OBJ TIME POINT IN UNITY
        """ Send the 3D files for the specified time point to browser and display the mesh 
        
        Parameters
        ----------
        t : int
            the time point to display in browser

        Examples
        --------
        >>> mc.plot_mesh(1)
        """
        obj=""
        data=self.dataset.get_seg(t)
        if data is not None:
            print(" --> Send mesh at "+str(t))
            self.dataset._setVolume(data,t) #Update Volumes
            obj=self._get_mesh(t,data)
        self.send("LOAD_"+str(t),obj)

    def plotAt(self,t,obj):#PLOT DIRECTLY THE OBJ PASS IN ARGUMENT
        """ Plot the specified 3D data to the specified time point inside the browser
        
        Parameters
        ----------
        t : int
            the time point to display in browser
        obj : bytes
            the 3d data

        Examples
        --------
        >>> #Specify a file on the hard drive by path, with rights
        >>> f = open(filepath,"r+")
        >>> #load content of file inside variable
        >>> content = f.read()    
        >>> mc.plotAt(1,content)
        >>> f.close()
        """
        self.send("LOAD_"+str(t),obj)

    def plot_meshes(self,times=None):  # PLOT ALL THE TIMES STEP EMBRYO IN MORPHONET
        """ Plot all data inside the browser

        Examples
        --------
        >>> mc.plot_meshes()
        """
        if times is None:
            times=range(self.dataset.begin,self.dataset.end+1)
        for t in times:
            self.plot_mesh(t)
           
    def del_mesh(self,t): #DELETE DITECLTY THE OBJ TIME POINT IN UNITY
        """ Delete the specified time point in the browser
        
        Parameters
        ----------
        t : int
            the time point to delete

        Examples
        --------
        >>> mc.del_mesh(1)
        """
        self.send("DEL_"+str(t))


    ################ TO QUIT PROPERLY
    def _receiveSignal(self,signalNumber, frame):
        if signalNumber==2:
            try:
                self.quit()
                quit()
            except:
                print(" --> quit MorphoPlot")
        return




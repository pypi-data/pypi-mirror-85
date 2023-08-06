"""Docstring for the net.py module.

This API is used to directly interact with your data on  MorphoNet

For any information for the installation go on https://pypi.org/project/morphonet/

"""

import sys,os
import time
import bz2
import hashlib
import json
import requests
import numpy as np
import gzip
from http.client import HTTPSConnection
from urllib.parse import urlencode
from urllib.request import urlretrieve

from morphonet.tools import addslashes,tryParseInt,strblue,strred,strgreen,nodata,ss,_getObjects,_getObject,_getType,_getLastCuration,_getString

#New For https...
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import urllib3
urllib3.disable_warnings()


class Net:
    """Connect to the MorphoNet server.

    Use your credentials to connect to MorphoNet

    Parameters
    ----------
    login : string
        your login in MorphoNet
    passwd : string
        your password in MorphoNet
    new_url : string, optional
        for developmental purpose, you can specify a new server that will be used to compute API request and get/upload MorphoNet data. 
    new_port : int, optional
        for developmental purpose, you can specify an other port

    Returns
    -------
    MorphoConnection
        return an object of morphonet which will allow you to upload or download data



    Examples
    --------
    >>> import morphonet
    >>> mn=morphonet.Net("yourlogin","yourpassword")


     
    """
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    def __init__(self,login,passwd,new_url=None,new_port=-1): 
        self.id_people=-1
        self.id_dataset=-1
        self.token = ""
        self.id_dataset_owner=-1
        self.minTime=-1
        self.maxTime=-1
        self.login=login
        self.passwd=passwd
        self.bundle=0
        self.id_NCBI=1 #0 -> Unclassified 
        self.id_type=0; #0 Observed Data, 1 Simulated Data, 2 Drawing Data
        self.guys={}
        self.datasettype={}
        if new_url is not None:
             self.url=new_url
        else:
            from morphonet import url
            self.url=url
        if new_port!=-1:    
            self.port=new_port 
        else:
            from morphonet import port
            self.port=port
        self._connect()

    def _getHeaders(self):
        if self.token == "":
            return {"Content-Type": "application/json"}
        return {"Content-Type": "application/json",'Authorization':'Token '+self.token}

    def _connect(self):
        #HTTPSConnection.debuglevel = 1
        conn = HTTPSConnection(self.url)
        params = json.dumps({'username': self.login, 'password': self.passwd})
        conn.request("POST", "/rest-auth/login/",params,self._getHeaders())
        response=conn.getresponse()
        if response.status==200:
            data=json.loads(str(response.read().decode("utf-8")))
            conn.close()
            self.id_people=data['user']
            self.token=data['key']
            print(strblue(self.login+' is connected to MorphoNet'))
            return True
        else:
            print(strred('CONNECTION ERROR '+str(response.status)+" "+response.reason))
        conn.close()
        return False
        
    def _isConnected(self):
        if self.id_people==-1:
            print(strred(' ERROR : You are not connected '))
            return False
        return True
    def _request(self,param,path,request_type):
        if self._isConnected():
            conn = HTTPSConnection(self.url,timeout=100)
            try:
                conn.request(request_type, path,json.dumps(param), self._getHeaders())
                response=conn.getresponse()
                if response.status==200:
                    da=json.loads(str(response.read().decode("utf-8")))
                    conn.close()
                    return da
                else:
                    print(strred('CONNECTION ERROR '+str(response.status)+" "+response.reason))
                    quit()
            except  Exception as e:
                print('Error cannot request ... '+str(e))
                time.sleep(5)
                print(' --> Retry')
                return self._request(param,path,request_type)
            conn.close()   
    def _binary_request(self,param,path,request_type):
        if self._isConnected():
            conn = HTTPSConnection(self.url,timeout=100)
            try:
                conn.request(request_type, path,json.dumps(param), self._getHeaders())
                response=conn.getresponse()
                if response.status==200:
                    da=response.read()
                    conn.close()
                    return da
                else:
                    print(strred('CONNECTION ERROR '+str(response.status)+" "+response.reason))
                    quit()
            except  Exception as e:
                print('Error cannot request ... '+str(e))
                time.sleep(5)
                print(' --> Retry')
                return self._binary_request(param,path,request_type)
            conn.close()   
    def _large_request(self,param,path,data):
        if self._isConnected():
            try:
                if os.path.isfile("temp.bz2"):
                    os.system('rm -f temp.bz2')
                if sys.version_info[0]>=3: #PYTHON 3
                    if isinstance(data,str):
                        data=bytes(data.encode('utf-8'))
                    with bz2.open("temp.bz2", "wb") as f:
                        unused = f.write(data)
                files = {'file': open("temp.bz2", 'rb')}
                session = requests.Session()
                del session.headers['User-Agent']
                del session.headers['Accept-Encoding']
                session.headers['Authorization'] = 'Token '+self.token 
                r = session.post("https://"+self.url+path, files=files,data=param,verify=False)
                if r.status_code == requests.codes.ok:
                    return r.text
                else:
                    print(strred('CONNECTION ERROR '+str(r.status_code)))
                    quit()
                if os.path.isfile("temp.bz2"):
                    os.system('rm -f temp.bz2')
            except  Exception as e:
                print('ERROR cannot request ... '+str(e))
                quit()
     
    def _large_request_image(self,param,path,data,format):
        if self._isConnected():
            try:
                if os.path.isfile("temp."+format):
                    os.system('rm -f temp.'+format)
                if sys.version_info[0]>=3: #PYTHON 3
                    if isinstance(data,str):
                        data=bytes(data.encode('utf-8'))
                    f = open("temp."+format, "wb")
                    f.write(data)
                    f.close()
                files = {'file': open("temp."+format, 'rb')}
                session = requests.Session()
                del session.headers['User-Agent']
                del session.headers['Accept-Encoding']
                session.headers['Authorization'] = 'Token '+self.token 
                r = session.post("https://"+self.url+path, files=files,data=param,verify=False)
                if r.status_code == requests.codes.ok:
                    return r.text
                else:
                    print(strred('CONNECTION ERROR '+str(r.status_code)))
                    quit()
                if os.path.isfile("temp.bz2"):
                    os.system('rm -f temp.bz2')
            except  Exception as e:
                print('ERROR cannot request ... '+str(e))
                quit()
    
    def _getGuys(self): 
        """ List all people in MorphoNet 

        """
        data=self._request({},'/api/people/','GET')
        for g in data:
            self.guys[int(g['id'])]=g['surname']+" "+g['name']
    def getGuyByID(self,id_guy): 
        """ Return the person corresponding to an id 
        
        Parameters
        ----------
        id_guy : int
            the id of the person you'r lokking for 
        
        Returns
        -------
        object
            name , surname and login

        Examples
        --------
        >>> mn.getGuyByID(1)
        """


        id_guy=int(id_guy)
        if self.guys=={}:
            self._getGuys()
        if id_guy in self.guys:
            return self.guys[id_guy]
        data=self._request({},'/api/people/'+str(id_guy),'GET')
        if data=="[]":
            return strred("unkown")
        else:
            return data
    def getGuyByName(self,name): # RETURN NAME + SURNAME + LOGIN FORM SPECIFIC ID
        """ Return the person corresponding to a specific name and surname 
        
        Parameters
        ----------
        name : string
            the name and surname separated by a space 
        
        Returns
        -------
        id_guy
            the id corresponding to the person, -1 if the person does not exist

        Examples
        --------
        >>> mn.getGuyByName("Faure Emmanuel")
        """

        values = name.split(' ')
        u_name = str(values[0])
        u_surname = str(values[1])
        data=self._request({'name':u_name,'surname':u_surname},'/api/userbyname/','GET')
        if nodata(data):
            print(strred('User is unknown or input is incorrect. Please input as "name surname"'))
            quit()
        if data=="[]":
            print(strblue(ss+str(name)+" is unkown"))
            return -1
        else:
            #dataset=json.loads(data)
            return int(data['id'])
    def getGroupByName(self,name): # RETURN NAME + SURNAME + LOGIN FORM SPECIFIC ID
        """ Return the group corresponding to a specific name  
        
        Parameters
        ----------
        name : string
            the name of the group
        
        Returns
        -------
        id_group
            the id corresponding to the group, -1 if the group does not exist

        Examples
        --------
        >>> mn.getGroupByName("The ascidians")
        """
        data=self._request({'name':name},'/api/groupidbyname/','GET')
        if nodata(data):
            print(strred('Please input as "name"'))
            quit()
        if data=="[]" or data['status'] is not None:
            print(strblue(ss+str(name)+" is unkown"))
            return -1
        else:
            #dataset=json.loads(data)
            return int(data['id'])
    #NCBI Taxonomy
    def _getNCBITypeByID(self,id_NCBI):
        """ Return the name of a specific NCBI id  c
        
        Parameters
        ----------
        id_NCBI : int
            the id of the NCBI Category 
        
        Returns
        -------
        name
            the corresponding name to the NCBI id coategory
        """
        if self._isConnected():
            data=self._request({},'/api/ncbitree/'+str(id_NCBI)+'/','GET')
            return data['name']
    #TYPE 
    def _getTypeName(self,id_type): #
        """ Return the name of a specific type
        
        Parameters
        ----------
        id_type : int
            0 for Observed Data, 1 for Simulated Data, 2 for Drawing Data 
        
        Returns
        -------
        name
            the corresponding name to the type 
        """
        if id_type==0:
            return "Observed Data"
        if id_type==1:
            return "Simulated Data"
        if id_type==2:
            return "Drawing Data"
        return "Unknown Data"


    #DATASET 
    def _isDataSet(self):
        """ Return true if you selected a dataset, false if you didn't
        
        """
        if not self._isConnected():
            return False
        if self.id_dataset==-1:
            print(strgreen(ss+'you first have to select a dataset'))
            return False
        return True
    def _ownDataSet(self):
        """ Return true if you are the owner of the dataset you select, false if you aren't

        """
        if not self._isDataSet():
            return False
        if str(self.id_dataset_owner)!=str(self.id_people):
            print(strgreen(ss+'you are not the owner of this dataset, ask '+self.getGuyByID(self.id_dataset_owner)))
            return False
        return True  
    def _initTimePoint(self,minTime,maxTime): #INTERNAL FUNCTION TO INITIALISE TIME POINT
        """ Localy override min and max time for the current dataset
        
        Parameters
        ----------
        minTime : int
            The new min_time value

        maxTime : int
            The new max_time value
        
        """
        self.minTime=int(minTime)
        self.maxTime=int(maxTime)
    def _parseDataSet(self,data): #Parse id,name,minTime,maxTime,id_people to dataset structure
        """ Store values into the current dataset
        
        Parameters
        ----------
        data : object
            Contains all data to be parsed and stored inside the daraser
        
        """
        if nodata(data):
            print(strred(ss+'dataset not found'))
        else:
            dataset=data
            ids,ok=tryParseInt(dataset['id'])
            if not ok: 
                print(strgreen(ss+'dataset not found '+str(data)))
            else: 
                name=dataset['name']
                self._initTimePoint(dataset['mintime'],dataset['maxtime'])
                self.id_dataset_owner=dataset['id_people']
                self.bundle,ok=tryParseInt(dataset['bundle'])
                self.id_NCBI,ok=tryParseInt(dataset['id_ncbi'])
                self.id_type,ok=tryParseInt(dataset['type'])
                self.id_dataset=ids
                print(ss+'found dataset '+name+' with id ' + str(self.id_dataset)+' from '+str(self.minTime)+' to ' +str(self.maxTime)+' owned by '+str(self.id_dataset_owner)+' with type='+str(self.id_NCBI))
    def _showDataSets(self,data):
        """ Display the values given inside parameter, formatted like a dataset
        
        Parameters
        ----------
        data : object
            Contains all values to be displayed
        
        """
        #dataset=json.loads(data)
        for datas in data:  #id,name,minTime,maxTime,id_people,bundle,id_NCBI,type,date
            s='('+str(datas['id'])+') '+datas['name']
            if int(datas['mintime'])!=int(datas['maxtime']):
                s+=' from '+str(datas['mintime'])+' to '+str(datas['mintime'])
            s+=' is '+self._getTypeName(int(datas['type']))
            if datas['id_ncbi'] != 0 and datas['id_ncbi'] != -1:
                s+=' of '+self._getNCBITypeByID(datas['id_ncbi'])
            s+=' created by '+self.getGuyByID(datas['id_people'])
            s+=' the '+datas['date']
            print(s)
    def listMyDataSet(self): #LIST ALL MY DATASET 
        """To display the datasets you own
        
        Examples
        --------
        >>> mn.listMyDataset()

        Notes
        --------
        It will display all your datasets like this
        >>> (id_set) set_name is data_type created by set_owner the creation_date

        """
        if self._isConnected():
            data=self._request({},'/api/mydataset/','GET')
            self._showDataSets(data)
    def listDataSet(self): #LIST ALL  DATASET 
        """To display dataset you can access (even if you re not owner) 
        
        Examples
        --------
        >>> mn.listDataSet()

        It will display all your datasets like this
        >>> (id_set) set_name is data_type created by set_owner the creation_date

    
        """
        if self._isConnected():
            data=self._request({},'/api/userrelatedset/','GET')
            self._showDataSets(data)
    def shareDatasetWithUser(self,id_user,role): #SHARE A DATASET with USER (role = 0:reader , 1:manager )
        """To share the current dataset with a specific user
        
        Parameters
        ----------
        id_user : int
            the id of the user
        role : int
            the role (Manager : 1, Reader : 0 ) which will be attribute to the user

        Examples
        --------
        >>> mn.shareDatasetWithUser(1,0)

        """
        if self._ownDataSet():
            data=self._request({"sharedataset":self.id_dataset,"id_user":id_user,"how":role},'/api/shareuserapi/','POST')
            ids,ok=tryParseInt(data['id'])
            if not ok: 
                print(strred(' ERROR : Share not created '+str(data['id'])))
            else :
                print(ss+"your share is created (with id "+str(data['id'])+')')
    def unshareDatasetWithUser(self,id_user): #UNSHARE A DATASET with USER
        """To unshare the current dataset with a specific user
        
        Parameters
        ----------
        id_user : int
            the id of the user
       
        Examples
        --------
        >>> mn.unshareDatasetWithUser(1)

        """
        if self._ownDataSet():
            data=self._request({"sharedataset":self.id_dataset,"id_user":id_user},'/api/unshareuserapi/','POST')
            if data['status'] == "failed": 
                print(strred(' ERROR : Share not deleted'))
            else :
                print(ss+"your share is deleted")
    def shareDatasetWithGroup(self,id_group,role): #SHARE A DATASET with GROUP
        """To share the current dataset with a specific group
        
        Parameters
        ----------
        id_group : int
            the id of the group
        role : int
            the role (Manager : 1, Reader : 0 ) which will be attribute to the group

        Examples
        --------
        >>> mn.shareDatasetWithGroup(1,0)

        """
        if self._ownDataSet():
            data=self._request({"sharedataset":self.id_dataset,"id_group":id_group,"how":role},'/api/sharegroupapi/','POST')
            ids,ok=tryParseInt(data['id'])
            if not ok: 
                print(strred(' ERROR : Share not created '+str(data['id'])))
            else :
                print(ss+"your share is created (with id "+str(data['id'])+')')
    def unshareDatasetWithGroup(self,id_group): #SHARE A DATASET with GROUP
        """To unshare the current dataset with a specific group
        
        Parameters
        ----------
        id_group : int
            the id of the group
       
        Examples
        --------
        >>> mn.unshareDatasetWithGroup(1)

        """

        if self._ownDataSet():
            data=self._request({"sharedataset":self.id_dataset,"id_group":id_group},'/api/unsharegroupapi/','POST')
            if data['status'] == "failed": 
                print(strred(' ERROR : Share not deleted'))
            else :
                print(ss+"your share is deleted")
    def createDataSet(self,name,minTime=0,maxTime=0,id_NCBI=0,id_type=0,spf=-1,dt=-1,serveradress=None): #CREATE A NEW DATA SET
        """To create a data in the MorphoNet database 
        
        Parameters
        ----------
        name : string
            the given name of the dataset
        minTime : int, optional
            the time first time point for 3D (or 2D) + t dataset, default: 0
        maxTime : int, optional
            the last first time point for 3D (or 2D) + t dataset, default: 0
        id_NCBI :int, optional
            the NCBI id attribute to the dataset
        id_type : int, optional
            the tType of dataset :
                - 0 : Observed
                - 1 : Simulated
                - 2 : Drawed
        spf : int , optional
            the second post fertilization for the first time point
        dt : int , optional 
            the delta time in seconds between two consecutive time points
        serveradress : string , optional 
            you own server adress

        Examples
        --------
        >>> mn.createDataSet("test set",minTime=1,maxTime=150)

        """
        self.id_NCBI=id_NCBI
        self.id_type=id_type
        if self._isConnected():
            data=self._request({"createdataset":name,"minTime":minTime,"maxTime":maxTime,"serveradress":serveradress,"id_NCBI":self.id_NCBI,"id_type":self.id_type,"spf":spf,"dt":dt},'/api/createdatasetapi/','POST')
            self.id_dataset_owner=self.id_people
            ids,ok=tryParseInt(data)
            if not ok: 
                print(strred(' ERROR : Dataset not created '+str(data)))
            else :
                self.id_dataset=ids
                self.id_dataset_owner=self.id_people
                self._initTimePoint(minTime,maxTime)
                print(ss+"your id dataset '"+name+"' is created (with id "+str(self.id_dataset)+')')
    def uploadDescription(self,description): #Upload a description 
        """ Change description of the selected dataset on the server
        
        Parameters
        ----------
        description : string
            New description to upload

        Examples
        --------
        >>> mn.uploadDescription("The new description attached")
        """
        if self._ownDataSet():
            data=self._request({"uploadescription":self.id_dataset,"description":description},'/api/uploadcommentapi/','POST')
            print(data['status'])        
    def updateDataSet(self,dataname="",minTime=-1,maxTime=-1,id_NCBI=-1,id_type=-1): #COMPLETE DELETE OF A DATASET
        """ Change specified values for the selected dataset
        
        Parameters
        ----------
        dataname : string, optional
            New name
        minTime : int, optional
            New minimal time point
        maxTime : int, optional
            New maximum time point
        id_NCBI : int, optional
            New taxonomy category id
        id_type : int, optional
            New dataset stored type 
        

        Examples
        --------
        >>> mn.updateDataSet("Changing name only")
        
        or
        
        >>> mn.updateDataSet("new name",1,1,1000,1)
        """
        if dataname!="":
            self.dataname=dataname
        if minTime!=-1:
            self.minTime=minTime
        if maxTime!=-1:
            self.maxTime=maxTime
        if id_NCBI!=-1:
            self.id_NCBI=id_NCBI 
        if id_type!=-1:
            self.id_type=id_type 
        if self._ownDataSet():
            data=self._request({"updatedataset":self.id_dataset,"minTime":self.minTime,"maxTime":self.maxTime,"id_NCBI":self.id_NCBI,"id_type":self.id_type,"dataname":self.dataname},'/api/updatesetapi/','POST')
            if nodata(data): 
                self._initTimePoint(self.minTime,self.maxTime)
            else:
                print(strred(' ERROR : '+str(data)))
    def selectDataSetById(self,ids): #SELECT A DATASET BY ID
        """ Select a dataset using an id
        
        Parameters
        ----------
        ids : int
            The dataset id to select

        Examples
        --------
        >>> mn.selectDataSetById(1)
        """
        if self._isConnected():
            self.id_dataset=-1
            data=self._request({"dataset":ids},'/api/sitedataset/'+str(ids)+'/','GET')
            if data is not None :
                self._parseDataSet(data)
            else :
                print("No dataset found")         
    def selectDataSetByName(self,name): #SELECT A DATASET BY NAME
        """ Select a dataset using is name
        
        Parameters
        ----------
        name : string
            The dataset name to select

        Examples
        --------
        >>> mn.selectDataSetByName("The name")
        """
        if self._isConnected():
            self.id_dataset=-1
            data=self._request({"datasetname":name},'/api/datasetnameapi/','GET')
            if len(data) > 0:
                self._parseDataSet(data[0])
            else :
                print("No dataset found")
    def deleteDataSet(self): #COMPLETE DELETE OF A DATASET
        """ Remove the selected dataset from the server

        Examples
        --------
        >>> mn.deleteDataSet()
        """
        if self._ownDataSet():
            data=self._request({"deletedataset":self.id_dataset},'/api/deletedatasetapi/','POST')
            if data['status'] == 'Delete done': 
                print(ss+'dataset deleted')
                self.id_dataset=-1
                self.id_dataset_owner=-1
                self.minTime=-1
                self.maxTime=-1
            else:
                print(strred(' ERROR : '+str(data)))
    def clearDataSet(self): # CLEAR ALL TIME POINT AND INFOS
        """ Remove the 3D data and all informations for the selected dataset

        Examples
        --------
        >>> mn.clearDataSet()
        """
        if self._ownDataSet():
            data=self._request({"cleardataset":self.id_dataset},'/api/cleardatasetapi/','POST')
            if data['status'] == 'Clear done':  
                print(ss+'dataset cleared')
            else:
                print(strred(' ERROR : '+str(data)))
    
    #MESH
    def _computeCenter(self,obj):
        """ Compute center of the given 3D object data
        
        Parameters
        ----------
        obj : bytes
            The 3D data to compute center
        
        Returns
        -------
        center : string
            The center formatted like this : X-value,Y-value,Z-value

        """
        objA=obj.split("\n")
        X=0.0; Y=0.0; Z=0.0; nb=0;
        for line in objA:
           if len(line)>2 and line[0]=='v' and line[1]!='n'  and line[1]!='t' :
               while line.find("  ")>=0:
                   line=line.replace("  "," ")
               tab=line.strip().split(" ")
               if len(tab)==4:
                   X+=float(tab[1].replace(',','.'))
                   Y+=float(tab[2].replace(',','.'))
                   Z+=float(tab[3].replace(',','.'))
                   nb+=1
        if nb==0:
           print('ERROR your obj does not contains vertex ')
           quit()                
        X/=nb
        Y/=nb
        Z/=nb
        return str(round(X,2))+','+str(round(Y,2))+','+str(round(Z,2))
    def readMesh(self,filename):
        """ Read the mesh inside the given filename
        
        Parameters
        ----------
        filename : string
            the mesh file name

        
        Returns
        -------
        obj : string
            the mesh

        Examples
        --------
        >>> mn.readMesh("path/to/myfile.obj")
        """
        f=open(filename,'r')
        obj=""
        for line in f:
            obj+=line
        f.close()
        return obj
    def getNumberofMeshAt(self,t,quality=-1,channel=-1):
        """ Get the number of 3D data mesh for the selected dataset at a specifid time point, for a quality and a channel
        
        Parameters
        ----------
        t : int
            The time point to get the number of 3D data from
        quality : int
            The quality of the 3D data
        channel : int
            Wich channel of the object

        
        Returns
        -------
        count : int
            the number of the 3D meshes for the specified configuration

        Examples
        --------
        >>> mn.getNumberofMeshAt(1,0,0)
        """
        if self._ownDataSet():
            data=self._request({"getnumberofmeshat":self.id_dataset,"t":t,"quality":quality,"channel":channel},'/api/numbermeshapi/','GET')
            ids,ok=tryParseInt(data['nb'])
            if not ok: 
                print(strred(' ERROR : cannot count number of mesh'))
            else :
                return ids
    def clearMeshAt(self,t,quality=-1,channel=-1):
        """ Remove the 3D data for the selected dataset at a specified time point, for a quality and channel
        
        Parameters
        ----------
        t : int
            The time point to clear 3D data from
        quality : int
            The quality of the 3D data
        channel : int
            Wich channel of the object

        Examples
        --------
        >>> mn.clearMeshAt(1,0,0)
        """
        if self._ownDataSet():
            data=self._request({"clearmeshat":self.id_dataset,"t":t,"quality":quality,"channel":channel},'/api/clearmeshapi/','POST')
            #data2=json.loads(data)
            if data['status'] == 'Clear done': 
                if quality==-1 and channel==-1:
                    print(ss+'mesh cleared at '+str(t))
                elif quality==-1:
                    print(ss+'mesh cleared at '+str(t)+ " with channel "+str(channel))
                elif channel==-1:
                    print(ss+'mesh cleared at '+str(t)+ " with quality "+str(quality))
                else:
                    print(ss+'mesh cleared at '+str(t)+ " with quality "+str(quality)+ " and channel "+str(channel))
            else:
                print(strred(' ERROR : '+str(data)))
    def uploadMesh(self,t,obj,quality=0,channel=0,link="null",texture=None,material=None,ttype="bmp"): #UPLOAD TIME POINT IN DATASET,new behaviour : do not override existing mesh in database (become uploadMultipleMesh)
        """ Upload a new mesh (3D data) to a specific time point, for a quality and channel given. You can upload a texture by giving a texture and a material, specifying the texture format
        
        Parameters
        ----------
        t : int
            The time point to set 3D data 
        obj : bytes
            The content of the 3D data
        quality : int, optional
            Which quality of the dataset
        channel : int, optional
            Which channel of the dataset
        link : string, optional 
            Do not specify this one if you don't know what you are doing !! If bundle already exist for this mesh on the server, specify it
        texture : bytes, optional
            The texture data content that will be applied to the mesh
        material : string, optional
            If texture is set, the name of the material that will be applied after applying the texure
        ttype : 
            If texture is set, the file format for the texture

        Returns
        -------
        id : int
            The id of the mesh created on the server

        Examples
        --------
        >>> #Specify a file on the hard drive by path, with rights
        >>> f = open(filepath,"r+")
        >>> #load content of file inside variable
        >>> content = f.read()    
        >>> mn.uploadMesh(1,content,0,0)
        >>> f.close()
        """
        if self._ownDataSet():
            #First we have to upload the texture
            if texture is not None and  material is None:
                print("Please specify the material associate with the texture")
                quit()
            if texture is  None and  material is not None:
                print("Please specify the texture associate with the material")
                quit()
            if obj is None:
                print("The Object file you provided is empty or corrupted, please verify that it is correct")
                return
            id_texture=-1
            center=self._computeCenter(obj)
            data=self._large_request({"uploadlargemesh":self.id_dataset,"t":t,"quality":quality,"channel":channel,"center":center,"link":link,"id_texture":id_texture},'/api/uploadlargemesh/',obj)
            data2 = json.loads(data)
            ids = -1
            if 'status' in data2: 
                print(strred(' ERROR : time point not uploaded '+str(data)))
            else :
                ids = data2['id']
                print(ss+"meshes at time point "+str(t)+" uploaded ( with id "+str(ids)+' )')
                if texture is not None and material is not None:
                    data=self._large_request_image({"uploadlargetexture":self.id_dataset,"t":t,"id_mesh":ids,"quality":quality,"channel":channel,"type":ttype,"material":material},'/api/uploadtextureapi/',texture,ttype)
                    data2 = json.loads(data)
                    id_texture = -1
                    if 'status' in data2: 
                        print(strred(' ERROR : texture not upload '+str(data)))
                    else :
                        id_texture = data2['id']
                        print(ss+"texture at time point "+str(t)+" uploaded ( with id "+str(id_texture)+' )')
            return ids
    def _getURLDecompress(self,data):
        obj=None
        if data is not None:
            try:
                import ast,gzip
                data_str=data.decode("UTF-8")
                if "url" in data_str:
                    dict_str = ast.literal_eval(data_str)
                    if "url" in dict_str:
                        url=dict_str["url"]
                else:
                    url=data_str
                if "http" not in url:
                    url="http://"+url
                r = requests.get(url,verify = False)
                obj=gzip.decompress(r.content)
                obj = str(obj,'utf-8')
            except ValueError:
                print("Error with "+str(data))
        return obj

    def getMesh(self,t,quality=0,channel=0):
        """ Retrieve the mesh on the server for the specified time, quality and channel
        
        Parameters
        ----------
        t : int
            The time point to get 3D data from
        quality : int, optional
            Which quality of the dataset
        channel : int, optional
            Which channel of the dataset

        Returns
        -------
        obj : string
            The 3D data for the mesh

        Examples
        --------
        >>> data = mn.getMesh(1)
        """
        obj = None
        if self._isDataSet():
            data=self._binary_request({"getmesh":self.id_dataset,"t":t,"quality":quality,"channel":channel},'/api/getmeshapi/','GET')
            obj=self._getURLDecompress(data)
            if obj is None:
                print(" --> No mesh found")
        return obj

    #RAW IMAGES
    def uploadRawImages(self,t,rawdata,voxel_size="1,1,1",channel=0,scale=1):
        """ Upload the dataset raw images with a scale value for a specified time, channel,  
        
        Parameters
        ----------
        t : int
            The time point to upload raw images
        rawdata : bytes
            The numpy array of the raw images of the dataset
        channel : int, optional
            For which channel of the dataset
        scale : float, optional
            Scale the raw images during the display to match the 3D data

        Returns
        -------
        id : int
            The id of the raw image created on the server

        Examples
        --------
        >>> im = imread(filepath) #Read your image
        >>> factor=2 #specify the resacle Factor
        >>> im=np.uint8(255*np.float32(im[::factor,::factor,::factor])/im.max())  #Convert it in 8 bits    
        >>> mn.uploadRawImages(1,im)
        """
        if self._ownDataSet():
            if not rawdata.dtype==np.uint8:
                print("Please first convert your data in uint8 ( actually in " + str(rawdata.dtype)+ " ) ")
                quit() 
            data=self._large_request({"uploadlargerawimages":self.id_dataset,"t":t,"channel":channel,"scale":scale,"voxel_size":str(voxel_size),"size":str(rawdata.shape)},'/api/uploadrawimageapi/',rawdata.tobytes(order="F"))
            data2 = json.loads(data)
            if 'status' in data2: 
                print(strred(' ERROR : raw image not uploaded '+str(data)))
            else :
                print(ss+"raw image at time point "+str(t)+" uploaded ( with id "+str(data2['id'])+' )')
            return data2['id']
    def clearRawImages(self):
        """ Remove all the raw images from the server for the specified dataset

        """
        if self._ownDataSet():
            data=self._request({"clearrawimages":self.id_dataset},'/api/clearrawimageapi/','POST')
            data2 = json.loads(data)
            if data2['status'] == 'done':  
                print(ss+'rawdata all cleared ')
            else:
                print(strred(' ERROR : '+str(data)))
    def deleteRawImages(self,t,channel=0):
        """ Remove the raw image of the 3D dataset on the server, but only for a specific time point and channel
        
        Parameters
        ----------
        t : int
            The time point to delete raw images
        channel : int, optional
            Which channel of the dataset

        >>> mn.deleteRawImages(0)
        """
        if self._ownDataSet():
            data=self._request({"deleterawimages":self.id_dataset,"t":t,"channel":channel},'/api/deleterawimageapi/','POST')
            data2 = json.loads(data)
            if data2['status'] == 'done':
                print(ss+'rawdata cleared at '+str(t))
            else:
                print(strred(' ERROR : '+str(data)))

    #PRIMITIVES
    def uploadMeshWithPrimitive(self,t,obj,quality=0,channel=0):
        """ Upload a new mesh (3D data) to a specific time point, for a quality and channel given but using a primitive object
        
        Parameters
        ----------
        t : int
            The time point to store 3D data
        obj : string
            The mesh of the 3D data
        quality : int, optional
            Which quality of the dataset
        channel : int, optional
            Which channel of the dataset

        Returns
        -------
        id : int
            The id of the mesh created on the server

        Examples
        --------
        >>> 
        >>> with open('mymesh.obj','r') as f: #Specify a file on the hard drive by path, with rights
        >>>     obj = f.read()   #load mesh of the file inside variable
        >>> mn.uploadMeshWithPrimitive(1,obj)
        """
        if self._ownDataSet():
            data=self._large_request({"uploadmeshwithprimitive":self.id_dataset,"t":t,"quality":quality,"channel":channel},'/api/uploadmeshprimitiveapi/',obj)
            data2 = json.loads(data)
            if 'status' in data2: 
                print(strred(' ERROR : raw image not uploaded '+str(data)))
            else :
                print(ss+"meshes at time point "+str(t)+" uploaded ( with id "+str(data2['id'])+' )')
            return data2['id']
    def uploadPrimitive(self,name,obj):
        """ Create a reusable 3D format instance in the database 
        
        Parameters
        ----------
        name : string
            Name of the primitive 
        obj : bytes
            The content of the primitive (3D Data)

        Returns
        -------
        id : int
            The id of the primitive created on the server

        Examples
        --------
        >>> with open('myprimitive.obj','r') as f: #Specify a file on the hard drive by path, with rights
        >>>     obj = f.read()   #load mesh of the file inside variable
        >>> mn.uploadPrimitive("a new primitive",obj)
        """
        if self._ownDataSet():
            data=self._large_request({"uploadprimitive":self.id_dataset,"name":name},'/api/uploadprimitiveapi/',obj)
            data2 = json.loads(data)
            if 'status' in data2: 
                print(strred(' ERROR : raw image not uploaded '+str(data)))
            else :
                print(ss+"primitive "+name+" uploaded ( with id "+str(data2['id'])+' )')
            return data2['id']
    def clearPrimitive(self):
        """ Clear all primitive existing for the selected dataset

        """
        if self._ownDataSet():
            data=self._request({"clearprimitive":self.id_dataset},'/api/clearprimitiveapi/','POST')
            data2 = json.loads(data)
            if data2['status'] == 'done': 
                print(ss+'primitive all deleted')
            else:
                print(strred(' ERROR : '+str(data)))
    def deletePrimitive(self,name):
        """ Delete a specific primitive (specified by its name) for the selected dataset
        
        Parameters
        ----------
        name : string
            Name of the primitive 

        Examples
        -------- 
        >>> mn.deletePrimitive("primitive to delete")
        """
        if self._ownDataSet():
            data=self._request({"deleteprimitive":self.id_dataset,"name":name},'/api/deleteprimitiveapi/','POST')
            data2 = json.loads(data)
            if data2['status'] == 'done': 
                print(ss+'primitive '+name+' deleted')
            else:
                print(strred(' ERROR : '+str(data)))



    #INFOS
    def showInfosType(self):
        """ Display all informations type storing fomats
        
        """
        MorphoFormat={}
        MorphoFormat ["time"] = " objectID:objectID";
        MorphoFormat ["space"] = "objectID:objectID";
        MorphoFormat ["float"] = "objectID:float";
        MorphoFormat ["string"] = "objectID:string";
        MorphoFormat ["group"] = "objectID:string";
        MorphoFormat ["selection"] = "objectID:int";
        MorphoFormat ["color"] = "objectID:r,g,b";
        MorphoFormat ["dict"] = "objectID:objectID:float";
        MorphoFormat ["sphere"] = "objectID:x,y,z,r";
        MorphoFormat ["vector"] = "objectID:x,y,z,r:x,y,z,r";
        print("\nUpload Type : ")
        for s in MorphoFormat:
            print("   "+s+'->'+MorphoFormat[s])
        print('   where objectID : <t,id,ch> or <t,id> or <id>')
        print('\n')
    def getInfos(self):
        """ List all informations for the selected dataset 

        Returns
        -------
        data : list
            The list of informations

        """
        if self._isDataSet():
            data=self._request({"listinfos":self.id_dataset},'/api/correspondencelistapi/','GET')
            return data
    def uploadInfo(self,infos,field): 
        """ Create a new information in the database 
        
        Parameters
        ----------
        name : string
            Name of the information 
        field : bytes
            The content of the infos (text Data respecting the corresponding format)

        Returns
        -------
        id : int
            The id of the information created on the server

        Examples
        --------
        >>> #Specify a file on the hard drive by path, with rights
        >>> file = open(filepath,"r+")
        >>> #load content of file inside variable
        >>> content = f.read()    
        >>> mn.uploadInfo("a new info",content)
        """
        if self._isDataSet():
            tab=field.split('\n')
            nbL=0
            datatype=""
            while datatype=="" and nbL<len(tab):
                if len(tab[nbL])>0:
                    types=tab[nbL].split(":")
                    if len(types)==2 and types[0]=="type":
                        datatype=types[1]
                nbL+=1
            if datatype=="":
                self.showInfosType()
                print('You did not specify your type inside the file')
                quit()
            dtype=2 #TYPE =1 For direclty load upload and 2 for load on click
            if datatype=="time" or datatype=="group"  or datatype=="space" :
                dtype=1
            data=self._large_request({"uploadlargecorrespondence":self.id_dataset,"infos":infos,"type":dtype,"datatype":datatype},'/api/uploadinfoapi/',field)
            data2 = json.loads(data)
            ids = -1
            if 'status' in data2: 
                print(strred(' ERROR : info not uploaded '+str(data)))
            else :
                ids = data2['id']
                print(ss+infos+" uploaded (with id "+str(ids)+')')
            return ids
    def deleteInfoByName(self,name):
        """ Delete an information specified by its name on the server
        
        Parameters
        ----------
        name : string
            Name of the information 

        Examples
        --------
        >>> mn.deleteInfoByName("information name")
        """
        if self._isDataSet():
            data=self._request({"deletecorrespondence":self.id_dataset,"infos":name},'/api/deleteinfonameapi/','POST')
            ids,ok=tryParseInt(data['id'])
            if not ok: 
                print(strred(' ERROR : '+str(name)+' '+str(data)))
            else :
                print(ss+infos+" with id "+str(ids)+" deleted")
    def deleteInfoById(self,id_info):
        """ Delete an information specified by its id on the server
        
        Parameters
        ----------
        name : string
            Name of the information 

        Examples
        --------
        >>> mn.deleteInfoById("1")
        """
        if self._isDataSet():
            data=self._request({"deletecorrespondenceid":self.id_dataset,"idinfos":id_info},'/api/deleteinfoidapi/','POST')
            ids,ok=tryParseInt(data)
            if not ok: 
                print(strred(' ERROR : '+str(id_info)+' '+str(data)))
            else :
                print(ss+"Infos with id "+str(ids)+" deleted")
    def getInfoByName(self,name):
        """ Get the data of the information specified by its name
        
        Parameters
        ----------
        name : string
            Name of the information 

        Returns
        -------
        infos : bytes
            The data stored on the server

        Examples
        --------
        >>> mn.getInfoByName("information name")
        """
        info=None
        if self._isDataSet():
            data=self._binary_request({"getinfos":self.id_dataset,"infos":name},'/api/getinfonameapi/','GET')
            print(data)
            info=self._getURLDecompress(data)
        return info
    def getInfoById(self,id_info):
        """ Get the data of the information specified by its id
        
        Parameters
        ----------
        id : int
            ID of the information 

        Returns
        -------
        infos : bytes
            The data stored on the server

        Examples
        --------
        >>> mn.getInfoById("information name")
        """
        info=None
        if self._isDataSet():
            data=self._binary_request({"getinfosid":self.id_dataset,"idinfos":id_info},'/api/getinfoidapi/','GET')
            info=self._getURLDecompress(data)
        return info


    def getObjectsFromInfoById(self,id_info):
        """ Get the list of object of an information specified by its id
        
        Parameters
        ----------
        id_info : int
            ID of the infomation 

        Returns
        -------
        objects : list
            List of key/value corresponding to a split to the information data

        Examples
        --------
        >>> objetcs = mn.getObjectsFromInfoById(1)
        """
        infos=self.getInfoById(id_info)
        return _getObjects(infos)
    def getObjectsFromInfoByName(self,name):
        """ Get the list of object of an information specified by its name
        
        Parameters
        ----------
        name : string
            name of the infomation 

        Returns
        -------
        objects : list
            List of key/value corresponding to a split to the information data

        Examples
        --------
        >>> objetcs = mn.getObjectsFromInfoByName("Information name")
        """
        infos=self.getInfoByName(name)
        return _getObjects(infos)

    def shareInfo(self,id_info):
        """ The information specified by its id become accessible to everyone you shared it (or public if you shared the information with public)
        
        Parameters
        ----------
        id_info : int
            ID of the infomation 

        Examples
        --------
        >>> objetcs = mn.shareInfo(1)
        """
        if self._ownDataSet():
            data=self._request({"idinfos":id_info},'/api/shareinfo/','POST')
            ids,ok=tryParseInt(data['id'])
            if not ok: 
                print(strred(' ERROR : Share not created '+str(data['id'])))
            else :
                print(ss+"your share is created (with id "+str(data['id'])+')')
    def unshareInfo(self,id_info):
        """ The information specified by its id become unaccessible to everyone you shared it (or public if you shared the information with public)

        Parameters
        ----------
        id_info : int
        ID of the infomation 

        Examples
        --------
        >>> objetcs = mn.unshareInfo(1)
        """
        if self._ownDataSet():
            data=self._request({"idinfos":id_info},'/api/unshareinfo/','POST')
            ids,ok=tryParseInt(data['id'])
            if not ok: 
                print(strred(' ERROR : Share not created '+str(data['id'])))
            else :
                print(ss+"your share is created (with id "+str(data['id'])+')')


    def getCuration(self,id_info):
        """ Retrieve the curations for a information from MorphoNet
        
        Parameters
        ----------
        id_info : int
            ID of the information

        Returns
        -------
        file : string
            The curation txt file for this information

        Examples
        --------
        >>> data = mn.getCuration(1)
        """
        curation=None
        if self._isDataSet():
            data=self._binary_request({"id_dataset":self.id_dataset,"id_infos":id_info},'/api/curationfileapi/','GET')
            if data is not None:
                data = str(data,'utf-8')
                if data !=  "failed":
                    curation=data
                #    data
        if curation is None:
                print("No information currations found")
        return curation


    def getInfoCurated(self,id_info):
        """ Retrieve directly the information curated from MorphoNet
        
        Parameters
        ----------
        id_info : int
            ID of the information

        Returns
        -------
        file : string
            The information with the last curation as a txt file in the MorphoNet Format

        Examples
        --------
        >>> data = mn.getInfoCurated(1)
        """
        info_curated=None
        if self._isDataSet():
            info=self.getInfoById(id_info)
            if info is not None:
                info_objets=_getObjects(info)
                curation=self.getCuration(id_info)
                if curation is not None:
                    curation_objets=_getObjects(curation)
                    info_curated="#Infor Curated\n"
                    for line in info.split('\n'):  #Add the comments of the info 
                        if len(line)>0 and line[0]=="#":
                            info_curated+=line+"\n"

                    for line in curation.split('\n'):
                        if len(line)>0 and line[0]=="#":  #Add the comments of the curation 
                            info_curated+=line+"\n"

                    info_curated+="type:"+_getType(info)+"\n"
                    for o in info_objets:
                        info_curated+=_getString(o)+":"
                        if o in curation_objets:
                            oCurated=_getLastCuration(curation_objets[o])
                            info_curated+=str(oCurated.split(';')[0])
                        else:
                            info_curated+=str(info_objets[o])
                        info_curated+="\n"
                    
                    #Only Curated value
                    onlyCurated=[]
                    for o2 in curation_objets:
                        if o2 not in info_objets:
                            if o2 not in onlyCurated:
                                onlyCurated.append(o2)
                    for o2 in onlyCurated:
                        oCurated=_getLastCuration(curation_objets[o2])
                        info_curated+=_getString(o2)+":"+str(oCurated.split(';')[0])+"\n"
                    
        return info_curated




    
        


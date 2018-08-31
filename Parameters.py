from pyproj import Proj, transform
from abc import ABCMeta, abstractmethod

class ProjRange(object):
    def __init__(self,minlat,maxlat,minlon,maxlon):
        self.MinLat = minlat
        self.MaxLat = maxlat
        self.MinLon = minlon
        self.MaxLon = maxlon




class ProjParameters(object):

    def __init__(self):
        self.observers = []
        self.__SrcProj = Proj(proj='latlong',ellps='WGS84')
        self.__ProjRange = ProjRange(-90,90,-180,180)

        self.OutputPath = '/'
        self.ProjectResolution = 0
        self.ProjectTaskName = 'Proj'
        self.BandWaveLengthList = None
        self.IsAuxiliaryFileMode = False

        # add wangqiang 20180824
        self.InputPath = ''
        self.AtmFilePath = ''
        self.ProjName = ''
        self.Atmosphere = 0
        self.satName = ''
        self.insName = ''
        self.TimeFlag = None
        self.AuxiliaryDataList = dict()
        self.CentralLon = 0
        
    def register(self, observer):
        if observer not in self.observers:
            if  'OnParametersUpdate' in dir(observer):
                self.observers.append(observer)
            else:
                raise Exception('OnParametersUpdate Not Define!')

    def deregister(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self):
        for o in self.observers:
            o.OnParametersUpdate()

    def data_changed(self):
        self.notify_observers()



    def setSrcProj(self,scrProj):
        self.__SrcProj = scrProj


    def getSrcProj(self):
        return  self.__SrcProj

    SrcProj = property(getSrcProj,setSrcProj)



    # __DstProj = Proj(proj='lcc',ellps='WGS84')
    __DstProj = None
    def setDstProj(self,dstproj):
        self.__DstProj = dstproj

    def getDstProj(self):
        return  self.__DstProj

    DstProj = property(getDstProj,setDstProj)





    def setProjRange(self,projrange):
        self.__ProjRange = projrange

    def getProjRange(self):
        return  self.__ProjRange

    ProjRange = property(getProjRange, setProjRange)

    def GetParamDescription(self):
        return  self.DstProj.srs + '_'+str(self.ProjRange.MinLat) + '-' + str(self.ProjRange.MaxLat) + '-' + str(
            self.ProjRange.MinLon) + '-' + str(self.ProjRange.MaxLon)
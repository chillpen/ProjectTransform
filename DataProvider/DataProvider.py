import sys
from abc import ABCMeta, abstractmethod
import numpy as N
import gc

class OrbitInfo(object):
    def __init__(self):
        self.Sat = ''
        self.Sensor = ''
        self.OrbitDirection= ''
        self.DNFlag = ''
        self.Date=''
        self.Time=''
        self.Width = 0
        self.Height = 0
        self.BandsWavelength=dict()
        self.BandsType=dict()


class DataProvider(object):

    def __init__(self):
        self.__OrbitInfo = OrbitInfo()

        self.startLine = -1
        self.endLine = -1
        self.__parameter = None
        return





    def Dispose(self):
        self.__OrbitInfo = None
        self.__parameter = None

    @property
    def OrbitInfo(self):
        return  self.__OrbitInfo


    @abstractmethod
    def GetLongitude(self):
        pass

    @abstractmethod
    def GetLatitude(self):
        pass

    @abstractmethod
    def GetResolution(self):
        pass

    @abstractmethod
    def GetOBSData(self, band):
        pass

    @abstractmethod
    def GetOBSDataCount(self):
        pass

    @abstractmethod
    def GetAuxiliaryData(self, dataName):
        pass

    @abstractmethod
    def GetAuxiliaryDataNamesList(self):
        pass

    @abstractmethod
    def GetDataDescription(self):
        pass

   
    @abstractmethod
    def GetInverseRef(self):
        pass


    # @abstractmethod
    # def GetSensorAzimuth(self):
    #     pass
    #
    # @abstractmethod
    # def GetSensorZenith(self):
    #     pass
    #
    # @abstractmethod
    # def GetSolarAzimuth(self):
    #     pass
    #
    # @abstractmethod
    # def GetSolarZenith(self):
    #     pass

    def SetParameter(self, parameter):
        parameter.register(self)
        self.__parameter = parameter

        return

    def GetParameter(self):
        return  self.__parameter

    def OnParametersUpdate(self):
        lat = self.GetLatitude()
        minlat = self.__parameter.ProjRange.MinLat
        maxlat = self.__parameter.ProjRange.MaxLat


        rangeIndex = N.where((minlat<=lat) & (lat<=maxlat))

        if rangeIndex[0][:].size<=0:
            return

        self.startLine = N.min(rangeIndex[0][:])-10
        self.endLine = N.max(rangeIndex[0][:])+10

        if self.startLine < 0:
            self.startLine = 0

        lineCount = lat.shape[0]

        if self.endLine >= lineCount:
            self.endLine = lineCount-1
        del lat 
        del rangeIndex
        gc.collect()
        return
        
    @abstractmethod
    def SetAuxiliaryDataFile(self, AuxiliaryNameDict, AuxiliaryDataDict):
       	pass
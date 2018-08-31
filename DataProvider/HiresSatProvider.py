from DataProvider import *
from HdfOperator import *
import types
import numpy as N
from Parameters import *
import ProjOutputData_module as SD

class HiresSatProvider(DataProvider):


    def __init__(self):
        super(HiresSatProvider,self).__init__()
        self.__AuxiliaryDataNamesList =dict()
        self.__HdfFileHandleList =dict()
        self.__obsDataCount = 1
        self.__description = 'NULL'
        self.__BandWaveLenthList = None

        self.__HdfOperator = HdfOperator()

        self.__dataRes = 50
        # self.__dataWidthAndHeight = 0
        return

    def OnParametersUpdate(self):
        super(HiresSatProvider, self).OnParametersUpdate()

        self.__BandWaveLenthList = self.GetParameter().BandWaveLengthList

        self.__obsDataCount =len(self.__BandWaveLenthList)
        self.CreateBandsInfo()

        return

    def CreateBandsInfo(self):

        index  = 1
        for wavelength in self.__BandWaveLenthList:
            self.OrbitInfo.BandsWavelength['EVB'+str(index)] = wavelength
            if int(wavelength)>230:
                self.OrbitInfo.BandsType['EVB'+str(index)] = 'EMIS'
            else:
                self.OrbitInfo.BandsType['EVB'+str(index)] = 'REF'
            index = index+1

    def GetLongitude(self):
        return self.GetDataSet(self.__HdfFileHandleList['L1'], '/', 'Longitude')

    def GetLatitude(self):
        return self.GetDataSet(self.__HdfFileHandleList['L1'], '/', 'Latitude')


    def GetDataSet(self,filehandle,group,ds):

        data = self.__HdfOperator.ReadHdfDataset(filehandle, group, ds)
        startLine = self.startLine
        endlLine = self.endLine
        ret = None
        if startLine!= -1 & endlLine!= -1:
            ret = data[startLine:endlLine, :]
        else:
            ret = data[:,:]

        return ret

    def SetL1File(self, file):

        # self.__L1DataFileHandle = self.__HdfOperator.Open(file)
        self.__HdfFileHandleList['L1'] = self.__HdfOperator.Open(file)
        savePath,saveFile =  os.path.split(file)
        saveFile = saveFile.upper()
        self.__description=saveFile.replace('.HDF','')

    def GetResolution(self):
        return  self.__dataRes


    def GetOBSData(self, band):
        bandname = 'DN'
        # caltableName = 'CAL'+self.OrbitInfo.BandsWavelength[band]
        ret = self.GetDataSet(self.__HdfFileHandleList['L1'], '/', bandname)[:,:].astype(N.int32)

        return ret


    def GetOBSDataCount(self):
        return self.__obsDataCount


    def GetAuxiliaryData(self, dataName):
        pass


    def GetAuxiliaryDataNamesList(self):
        return self.__AuxiliaryDataNamesList


    def GetDataDescription(self):
        return self.__description
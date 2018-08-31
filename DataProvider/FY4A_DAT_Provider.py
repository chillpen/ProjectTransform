from DataProvider import *
from HdfOperator import *
import types
import numpy as N
from Parameters import *
import ProjOutputData_module as SD


class FY4A_DAT_Provider(DataProvider):


    def __init__(self):
        super(FY4A_DAT_Provider,self).__init__()
        self.__AuxiliaryDataNamesList =dict()
        self.__HdfFileHandleList =dict()
        self.__obsDataCount = 0
        self.__description = 'NULL'
        self.__BandWaveLenthList = None

        self.__HdfOperator = HdfOperator()

        self.__longitude = None
        self.__latitude = None
        self.__dataRes = 0
        self.__dataWidthAndHeight = 0
        return

    def Dispose(self):
        self.__AuxiliaryDataNamesList.clear()
        if self.__BandWaveLenthList is not None:
            del self.__BandWaveLenthList
            self.__BandWaveLenthList=None

        # del self.__AuxiliaryDataNamesList
        for filehandleName in self.__HdfFileHandleList:
            filehandle = self.__HdfFileHandleList[filehandleName]
            if isinstance(filehandle,str):return
            if filehandle.id.valid:
                filehandle.close()

        self.__HdfFileHandleList.clear()

        self.__description = 'NULL'
        self.__obsDataCount = 0
        super(FY4A_DAT_Provider, self).Dispose()

    def __InitOrbitInfo(self):
        self.OrbitInfo.Sat = 'Himawari8'
        self.OrbitInfo.Sensor = 'OBI'
        self.OrbitInfo.OrbitDirection= ''

        self.OrbitInfo.Width = self.__dataWidthAndHeight
        self.OrbitInfo.Height = self.__dataWidthAndHeight

        # solarzenith = self.GetSolarZenith()
        # if solarzenith[int(self.__dataWidthAndHeight/2),int(self.__dataWidthAndHeight/2)] <=85:
        #     self.OrbitInfo.DNFlag = 'D'
        # else:
        #     self.OrbitInfo.DNFlag = 'N'

        self.OrbitInfo.Date=self.GetDate()
        self.OrbitInfo.Time=self.GetTime()




    def GetDate(self):
        filehandle=self.__HdfFileHandleList['L1']

        year = self.__HdfOperator.ReadHdfAttri(filehandle,'/','iStartYear')
        month = self.__HdfOperator.ReadHdfAttri(filehandle,'/','iStartMonth')
        day = self.__HdfOperator.ReadHdfAttri(filehandle,'/','iStartDay')
        strmonth = '{:0>2}'.format(str(month[0]))
        srtday = '{:0>2}'.format(str(day[0]))
        stryear = '{:0>4}'.format(str(year[0]))
        return stryear+strmonth+srtday

    def GetTime(self):
        filehandle=self.__HdfFileHandleList['L1']

        hour = self.__HdfOperator.ReadHdfAttri(filehandle,'/','iStartHour')
        minute = self.__HdfOperator.ReadHdfAttri(filehandle,'/','iStartMinute')

        strhour= '{:0>2}'.format(str(hour[0]))
        srtminute = '{:0>2}'.format(str(minute[0]))

        return strhour+srtminute

    def OnParametersUpdate(self):
        super(FY4A_DAT_Provider, self).OnParametersUpdate()

        self.__BandWaveLenthList = self.GetParameter().BandWaveLengthList

        self.__obsDataCount =len(self.__BandWaveLenthList)
        self.CreateBandsInfo()

        return

    def SetLonLatFile(self,latfile,lonfile):
        self.__HdfFileHandleList['Latitude'] = self.__HdfOperator.Open(latfile)
        self.__HdfFileHandleList['Longitude'] = self.__HdfOperator.Open(lonfile)

    def SetL1File(self, file):

        # self.__L1DataFileHandle = self.__HdfOperator.Open(file)
        self.__HdfFileHandleList['L1'] = self.__HdfOperator.Open(file)

        if '_2000M_' in file:
            self.__dataRes = 2000
            self.__dataWidthAndHeight = 5500
        elif '_0500M' in file:
            self.__dataRes = 500
            self.__dataWidthAndHeight = 22000
            # self.__obsDataCount = 1
            # self.__BandWaveLenthList = ['0064']
        elif '_1000M' in file:
            self.__dataRes = 1000
            self.__dataWidthAndHeight = 11000
            # self.__obsDataCount = 4
            # self.__BandWaveLenthList = ['0046', '0051', '0064', '0086']
        # else:
        #     self.__BandWaveLenthList = ['0064', '0086', '0160', '0230', '0390', '0620', '0700', '0730',
        #                             '0860', '0960', '1040', '1120', '1230', '1330']
        #     self.__obsDataCount = 14

        # path, filename = os.path.split(file)
        # self.__description = filename.upper().replace('.HDF', '')
        self.__InitOrbitInfo()
        # self.__description=self.OrbitInfo.Sat+'_'+self.OrbitInfo.Sensor+'_'+self.OrbitInfo.Date+'_'+self.OrbitInfo.Time


    def SetAuxiliaryDataFile(self, AuxiliaryNameDict, AuxiliaryDataDict):

      	for key in AuxiliaryDataDict:
            if key == 'f30yInterpSSTData':
                self.__HdfFileHandleList[key] = AuxiliaryDataDict[key]
                self.__AuxiliaryDataNamesList[key] = AuxiliaryNameDict[key]
            else:
                self.__HdfFileHandleList[key] = self.__HdfOperator.Open(AuxiliaryDataDict[key])
                self.__AuxiliaryDataNamesList[key] = AuxiliaryNameDict[key]

        return


    def CreateBandsInfo(self):

        # index  = 1
        for wavelength in self.__BandWaveLenthList:
            self.OrbitInfo.BandsWavelength['EVB'+str(wavelength)] = wavelength
            if int(wavelength)>230:
                self.OrbitInfo.BandsType['EVB'+str(wavelength)] = 'EMIS'
            else:
                self.OrbitInfo.BandsType['EVB'+str(wavelength)] = 'REF'
            # index = index+1


    def GetLongitude(self):

        return self.GetDataSet(self.__HdfFileHandleList['Longitude'], '/', 'Lon')


    def GetLatitude(self):

        return self.GetDataSet(self.__HdfFileHandleList['Latitude'], '/', 'Lat')


    def GetResolution(self):
        return self.__dataRes

    def GetOBSData(self, band):

        bandname = self.__GetOBSDatasetName(band,self.__dataRes)
        caltableName = 'CAL'+self.OrbitInfo.BandsWavelength[band]
        ret = None
        if bandname!='':

            data=self.GetDataSet(self.__HdfFileHandleList['L1'], '/', bandname)[:,:].astype(N.int32)
            # caltable = self.GetDataSet(self.__HdfFileHandleList['L1'], '/', caltableName)
            caltable = self.__HdfOperator.ReadHdfDataset(self.__HdfFileHandleList['L1'], '/', caltableName)[:].astype(N.float32)
            height = data.shape[0]
            width = data.shape[1]
            bantype = 1
            if self.OrbitInfo.BandsType[band] == 'REF':
                bantype = 0
            ret=SD.CreateH8CalibrationData(int(width ), int(height),bantype,caltable,data)
            
        return ret

    def __GetOBSDatasetName(self, band,datares):
        bandname = ''
        waveLength = self.OrbitInfo.BandsWavelength[band]
        if self.OrbitInfo.BandsType[band] == 'REF':
            bandname = 'NOMChannelVIS'+waveLength+'_'+str(datares)
        else:
            bandname = 'NOMChannelIRX' + waveLength + '_'+str(datares)

        return  bandname

    def GetOBSDataCount(self):
        return self.__obsDataCount


    def GetDataSet(self,filehandle,group,ds):



        startLine = self.startLine
        endlLine = self.endLine
        ret = None


        if (ds == 'f30yInterpSSTData') :
            data = N.fromfile(self.__HdfFileHandleList[ds], dtype=N.dtype([('d', '<f4', 5500)]))['d']
        else:
            data = self.__HdfOperator.ReadHdfDataset(filehandle, group, ds)
        if startLine!= -1 & endlLine!= -1:
            ret = data[startLine:endlLine, :]
        else:
            ret = data[:,:]
        print ret.shape
        print ret
        return ret

    def GetAuxiliaryData(self,dataname):

        dsname = self.__AuxiliaryDataNamesList[dataname]
        ret = None
        if dsname =='':
            return  ret

        ret = self.GetDataSet(dsname, '/', dataname)

        return ret


    def GetAuxiliaryDataNamesList(self):
        return self.__AuxiliaryDataNamesList


    def SetDataDescription(self, value):
        self.__description = value

    def GetDataDescription(self):
        if self.__description == 'NULL':
            self.__description = self.GetParameter().GetParamDescription()+'_'+str(self.GetParameter().ProjectResolution)
        return  self.__description



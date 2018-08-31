from DataProvider import *
from HdfOperator import *
import types
import numpy as N
from Parameters import *
import struct
import datetime
import time
class NOAAPprovider(DataProvider):


    def __init__(self):
        super(NOAAPprovider,self).__init__()
        self.__AuxiliaryDataNamesList =dict()
        self.__HdfFileHandleList =dict()
        self.__obsDataCount = 0
        self.__description = 'NULL'
        self.__BandWaveLenthList = None

        self.__HdfOperator = HdfOperator()

        self.__longitude = None
        self.__latitude = None
        self.__dataRes = 0
        self.__dataWidth = 0
        self.__dataHeight = 0

        return

    def Dispose(self):
        self.__AuxiliaryDataNamesList.clear()
        if self.__BandWaveLenthList is not None:
            del self.__BandWaveLenthList
            self.__BandWaveLenthList=None

        # del self.__AuxiliaryDataNamesList
       # for filehandle in self.__HdfFileHandleList:
           # self.__HdfFileHandleList[filehandle].close()

            self.__HdfFileHandleList.clear()

            self.__description = 'NULL'
            self.__obsDataCount = 0
            super(NOAAPprovider, self).Dispose()

    def __InitOrbitInfo(self):
        self.OrbitInfo.Sat = 'NOAA18'
        self.OrbitInfo.Sensor = 'AVHRR'
        self.OrbitInfo.OrbitDirection= ''

        self.OrbitInfo.Width = self.__dataWidth
        self.__dataHeight = self.GetHeight()
        # solarzenith = self.GetSolarZenith()
        # if solarzenith[int(self.__dataWidthAndHeight/2),int(self.__dataWidthAndHeight/2)] <=85:
        #     self.OrbitInfo.DNFlag = 'D'
        # else:
        #     self.OrbitInfo.DNFlag = 'N'
        self.OrbitInfo.Height = self.__dataHeight
        self.OrbitInfo.Date=str(self.GetDate())
        self.OrbitInfo.Time=str(self.GetTime())



    def GetHeight(self):
        filehandle = self.__HdfFileHandleList['L1']
        Height = self.ReadDataset(filehandle, 'Height')
        return Height

    def GetDate(self):
        filehandle=self.__HdfFileHandleList['L1']
        Date = self.ReadDataset(filehandle, 'Date')
        return Date

    def GetTime(self):
        filehandle=self.__HdfFileHandleList['L1']
        Time = self.ReadDataset(filehandle, 'Time')
        return Time

    def OnParametersUpdate(self):
        super(NOAAPprovider, self).OnParametersUpdate()

        self.__BandWaveLenthList = self.GetParameter().BandWaveLengthList

        self.__obsDataCount =len(self.__BandWaveLenthList)
        self.CreateBandsInfo()

        return

    def SetLonLatFile(self,latfile,lonfile):
        # self.__latFileHandle = self.__HdfOperator.Open(latfile)
        # self.__lonFileHandle = self.__HdfOperator.Open(lonfile)l
        self.__HdfFileHandleList['Latitude'] = latfile
        self.__HdfFileHandleList['Longitude'] = lonfile

    def SetL1File(self, file):
        self.__HdfFileHandleList['L1'] = file
        self. __dataWidth = 2000 #latitude/longitude number in one scanline is 2000 after interpolation
        self.__dataRes = 1000
        self.__InitOrbitInfo()
        self.__description=self.OrbitInfo.Sat+'_'+self.OrbitInfo.Sensor+'_'+self.OrbitInfo.Date+'_'+self.OrbitInfo.Time


    def SetAuxiliaryDataFile(self,LNDfile,LMKfile,DEMfile,COASTfile,SATZENfile,SATAZIfile,Lonfile,LatFile):

        if LNDfile!='NULL':
            self.__HdfFileHandleList['LandCover'] = open(LNDfile)
            self.__AuxiliaryDataNamesList['LandCover'] = 'LandCover'
        if LMKfile!='NULL':
            self.__HdfFileHandleList['LandSeaMask'] = open(LMKfile)
            self.__AuxiliaryDataNamesList['LandSeaMask'] = 'LandSeaMask'
        if DEMfile!='NULL':
            self.__HdfFileHandleList['DEM'] = open(DEMfile)
            self.__AuxiliaryDataNamesList['DEM'] = 'DEM'
        if COASTfile!='NULL':
            self.__HdfFileHandleList['SeaCoast']= open(COASTfile)
            self.__AuxiliaryDataNamesList['SeaCoast'] = 'SeaCoast'
        if SATZENfile!='NULL':
            self.__HdfFileHandleList['SensorZenith']= SATZENfile
            self.__AuxiliaryDataNamesList['SensorZenith'] = 'SatZenith'
        if SATAZIfile!='NULL':
            self.__HdfFileHandleList['SensorAzimuth']= open(SATAZIfile)
            self.__AuxiliaryDataNamesList['SensorAzimuth'] = 'SatAzimuth'
        if Lonfile != 'NULL':
            self.__AuxiliaryDataNamesList['Longitude'] = 'Longitude'
        if LatFile != 'NULL':
            self.__AuxiliaryDataNamesList['Latitude'] = 'Latitude'

        return


    def CreateBandsInfo(self):

        for index in range(2):
            self.OrbitInfo.BandsWavelength['EVB'+str(index+1)] = self.__BandWaveLenthList[index]
            self.OrbitInfo.BandsType['EVB'+str(index+1)] = 'REF'
            index = index + 1
        for index in range(2,5):
            self.OrbitInfo.BandsWavelength['EVB' + str(index+1)] = self.__BandWaveLenthList[index]
            self.OrbitInfo.BandsType['EVB'+str(index+1)] = 'EMIS'
            index = index + 1


    def GetLongitude(self):

        return self.GetDataSet(self.__HdfFileHandleList['Longitude'],  'Longitude')


    def GetLatitude(self):

        return self.GetDataSet(self.__HdfFileHandleList['Latitude'], 'Latitude')


    def GetResolution(self):
        return self.__dataRes

    def GetOBSData(self, band):

        ret = None
        if band!='':

            ret=self.GetDataSet(self.__HdfFileHandleList['L1'], band)[:,:].astype(N.int32)

        return ret


    def GetOBSDataCount(self):
        return self.__obsDataCount


    def  GetDataSet(self,filehandle,ds):

        data = self.ReadDataset(filehandle, ds)
        startLine = self.startLine
        endlLine = self.endLine
        ret = None
        if startLine!= -1 & endlLine!= -1:
            ret = data[startLine:endlLine, :]
        else:
            ret = data[:,:]
        return ret

    def GetAuxiliaryData(self,dataname):

        dsname = self.__AuxiliaryDataNamesList[dataname]
        ret = None
        if dsname =='':
            return  ret

        ret=self.GetDataSet(self.__HdfFileHandleList[dataname], dsname)

        return ret


    def GetAuxiliaryDataNamesList(self):
        return self.__AuxiliaryDataNamesList


    def SetDataDescription(self, value):
        self.__description = value

    def GetDataDescription(self):
        if self.__description == 'NULL':
            self.__description = self.GetParameter().GetParamDescription()+'_'+str(self.GetParameter().ProjectResolution)
        return  self.__description



    def ReadDataset(self,filehandle,ds):

        data = N.fromfile(filehandle, dtype='b')#read binary

        Lines = data[128:130]
        Lines = struct.unpack('h', Lines)
        DataLines = Lines[0]  # convert tuple to int

        TatalPartNum = DataLines + 1
        NOAAData = data[22016:TatalPartNum * 22016]  # remove head
        NOAAData = NOAAData.reshape(DataLines, 22016)
        if ds == 'Height':
            # DataLines = data[128:130]
            # DataLines = struct.unpack('h', DataLines)
            # DataLines = DataLines[0]  # convert tuple to int
            return DataLines
        # CentralBand = [2659.8000, 928.1460, 833.2530]
        # CentralBand = N.array(CentralBand)

        elif ds == 'Date':
            StartDateAndTime_array = data[84:92]
            StartDateAndTime_array = struct.unpack('2hi', StartDateAndTime_array)
            StartDate = datetime.date(StartDateAndTime_array[0], 1, 1) + datetime.timedelta(StartDateAndTime_array[1])
            StartDate_str = str(StartDate)
            return StartDate_str
        elif ds == 'Time':
            StartDateAndTime_array = data[84:92]
            StartDateAndTime_array = struct.unpack('2hi', StartDateAndTime_array)
            # StartDate = datetime.date(StartDate_array[0], 1, 1) + datetime.timedelta(StartDate_array[1] - 1)
            StartTime = StartDateAndTime_array[2] / float(1000)
            # StartTime = time.strftime("%H:%M.%S", time.(StartTime))
            Hour = int(StartTime)/3600
            Minute = int(StartTime - Hour*3600)/60
            Second =int(StartTime - Hour*3600 - Minute *60)
            StartTime_str = str(Hour)+':'+str(Minute)+':'+str(Second)
            return StartTime_str
            # EndDate = data[96:104]
            # EndDate = struct.unpack('2hi', EndDate)
            # return EndDate[1]


        elif (ds == 'SatZenith'  or ds == 'SolarZenith'):
            data_sat_solar = NOAAData[:, 328:634]
            data_sat_solar = data_sat_solar.reshape(DataLines * (634 - 328))
            SatSolarUnpackPara = str(DataLines * (634 - 328) / 2) + 'h'
            data_sat_solar = struct.unpack(SatSolarUnpackPara, data_sat_solar)
            data_sat_solar = N.array(data_sat_solar)
            data_sat_solar = data_sat_solar.reshape(DataLines, 51, 3)

            if ds == 'SolarZenith':
                data_SolarZenith = data_sat_solar[:, :, 0]
                SolarZenith = self.Interpolation(data_SolarZenith,DataLines)
                SolarZenith = SolarZenith/float(100)
                return SolarZenith
            # data_SolarZenith = data_SolarZenith/float(100)
            else:
                data_SatZenith = data_sat_solar[:, :, 1]
                SatZenith = self.Interpolation(data_SatZenith,DataLines)
                SatZenith = SatZenith/float(100)
                return SatZenith

            # data_SatZenith = data_SatZenith/float(100)
        # data_RelativeZenith = data_sat_solar[:, :, 2]
        # data_RelativeZenith = data_RelativeZenith/float(100)

        elif (ds == 'Latitude') or (ds == 'Longitude'):

            data_Lat_Lon = NOAAData[:, 640:1048]
            data_Lat_Lon = data_Lat_Lon.reshape(DataLines * (1048 - 640))
            LatLonUnpackPara = str(DataLines * (1048 - 640) / 4) + 'i'
            data_Lat_Lon = struct.unpack(LatLonUnpackPara, data_Lat_Lon)
            data_Lat_Lon = N.array(data_Lat_Lon)
            data_Lat_Lon = data_Lat_Lon.reshape(DataLines, 51, 2)
            if ds == 'Latitude':
                data_Lat = data_Lat_Lon[:, :, 0]
                Latitude = self.Interpolation(data_Lat,DataLines)
                Latitude = Latitude/float(10000)
                return Latitude
            # data_Lat = data_Lat/float(10000)
            elif ds =='Longitude':
                data_Lon = data_Lat_Lon[:, :, 1]
                Longitude = self.Interpolation(data_Lon,DataLines)
                Longitude = Longitude / float(10000)
                return Longitude
            # data_Lon = data_Lon/float(10000)

        REFScalesAndOffsets = NOAAData[:, 48:228]
        REFScalesAndOffsets = REFScalesAndOffsets.reshape(DataLines * (228 - 48))
        REFUnpackPara = str((DataLines * (228 - 48)) / 4) + 'i'
        REFScalesAndOffsets = struct.unpack(REFUnpackPara, REFScalesAndOffsets)
        REFScalesAndOffsets = N.array(REFScalesAndOffsets)
        REFScalesAndOffsets_reshape = REFScalesAndOffsets.reshape(DataLines, 45)
        RefSlope = REFScalesAndOffsets_reshape[0, :]
        RefSlope = RefSlope.reshape(3, 3, 5)
        # RefSlope0 = RefSlope[0:2, 2, 0:2]
        RefSlope0 = RefSlope[0:3, 2, 0:2]
        REFScales = RefSlope0[:, 0] / float(10 ** 10)
        REFOffsets = RefSlope0[:, 1] / float(10 ** 7)

        EmissiveScalesAndOffsets = NOAAData[:, 228:300]
        EmissiveScalesAndOffsets = EmissiveScalesAndOffsets.reshape(DataLines * (300 - 228))
        EMISUnpackPara = str((DataLines * (300 - 228) / 4)) + 'i'
        EmissiveScalesAndOffsets = struct.unpack(EMISUnpackPara, EmissiveScalesAndOffsets)
        EmissiveScalesAndOffsets = N.array(EmissiveScalesAndOffsets)
        Emissive_slope = EmissiveScalesAndOffsets.reshape(DataLines, 18)
        EmissiveSlope = Emissive_slope[0, :]
        EmissiveSlope = EmissiveSlope.reshape(3, 2, 3)
        EmissiveSlope0 = EmissiveSlope[0:3, 0, 1:3]
        EmissiveScales = EmissiveSlope0[:, 0] / float(10 ** 6)
        EmissiveOffsets = EmissiveSlope0[:, 1] / float(10 ** 6)

        DATA = NOAAData[:, 1264:21744]
        DATA = DATA.reshape(DataLines * (21744 - 1264))
        DataUnpackPara = str(DataLines * (21744 - 1264) / 2) + 'h'
        DATA_shortint = struct.unpack(DataUnpackPara, DATA)
        DATA_shortint = N.array(DATA_shortint)
        DATA_shortint = DATA_shortint.reshape(DataLines, 2048, 5)

        if ds == 'EVB1':
            DATA1 = DATA_shortint[:, 24:2024, 0]
            Data_B1 = DATA1 * (REFScales[0]) + REFOffsets[0]
            Data_B1 = Data_B1 * 10 + 0.5
            return Data_B1
        elif ds == 'EVB2':
            DATA2 = DATA_shortint[:, 24:2024, 1]
            Data_B2 = DATA2 * (REFScales[1]) + REFOffsets[1]
            Data_B2 = Data_B2 * 10 + 0.5
            return Data_B2
        elif ds == 'EVB3':
            DATA3 = DATA_shortint[:, 24:2024, 2]
            Data_B3 = DATA3 * (EmissiveScales[0]) + EmissiveOffsets[0]
            # Data_B3 = DATA3 * (REFScales[2]) + REFOffsets[2]
            Data_B3 = Data_B3 * 10 + 0.5
            return Data_B3
        elif ds == 'EVB4':
            DATA4 = DATA_shortint[:, 24:2024, 3]
            Data_B4 = DATA4 * (EmissiveScales[1]) + EmissiveOffsets[1]
            Data_B4 = Data_B4 * 10 + 0.5
            return Data_B4
        elif ds == 'EVB5':
            DATA5 = DATA_shortint[:, 24:2024, 4]
            Data_B5 = DATA5 * (EmissiveScales[2]) + EmissiveOffsets[2]
            Data_B5 = Data_B5 * 10 + 0.5
            return Data_B5


    def Interpolation(self,data,dataLines):
            DateAppend = []
            OutData = []
            DataLines = dataLines
            for i in range(DataLines):
                for j in range(50):
                    StartNum = data[i, j]
                    EndNum = data[i, j + 1]
                    # StartPoint = j * 40 + 25
                    # EndPoint = (j + 1) * 40 + 25
                    Temp = N.linspace(StartNum, EndNum, 40, endpoint=False)
                    DateAppend.append(Temp)
                DateAppend = N.array(DateAppend)
                # a = a.reshape(200)
                OutData.append(DateAppend)
                DateAppend = []
            OutData = N.array(OutData)
            OutDataReshape = OutData.reshape(DataLines, 2000)

            return OutDataReshape
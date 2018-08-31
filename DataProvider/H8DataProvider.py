from DataProvider import *
from HdfOperator import *
import types
import numpy as N
from Parameters import *
import ProjOutputData_module as SD
import gc

class H8Dataprovider(DataProvider):


    def __init__(self):
        super(H8Dataprovider,self).__init__()
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
        self.__refWidth = 0
        self.__reftoplat = 0
        self.__refbottomlat = 0
        self.__leftlon = 0
        self.__rightlon = 0
        return

    def Dispose(self):
        self.__AuxiliaryDataNamesList.clear()
        if self.__BandWaveLenthList is not None:
            del self.__BandWaveLenthList
            self.__BandWaveLenthList=None

        # del self.__AuxiliaryDataNamesList
        for filehandleName in self.__HdfFileHandleList:
            filehandle = self.__HdfFileHandleList[filehandleName]
            if filehandle.id.valid:
                filehandle.close()

        self.__HdfFileHandleList.clear()

        self.__description = 'NULL'
        self.__obsDataCount = 0
        super(H8Dataprovider, self).Dispose()

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
        super(H8Dataprovider, self).OnParametersUpdate()
        self.__dataRes = int(self.GetParameter().ProjectResolution)
        
        if self.__dataRes == 2000 :
            self.__dataRes = 2000
            self.__dataWidthAndHeight = 5500
            self.__refWidth = 8100
            # self.__obsDataCount = 16
            # self.__BandWaveLenthList = ['0046', '0051', '0064', '0086', '0160', '0230', '0390', '0620', '0700', '0730',
            #                         '0860','0960','1040', '1120', '1230', '1330']
        elif self.__dataRes == 500:
            self.__dataRes = 500
            self.__dataWidthAndHeight = 22000
            self.__refWidth = 32400
            # self.__obsDataCount = 1
            # self.__BandWaveLenthList = ['0064']
        elif self.__dataRes == 1000:
            self.__dataRes = 1000
            self.__dataWidthAndHeight = 11000
            self.__refWidth = 16200
        self.__BandWaveLenthList = self.GetParameter().BandWaveLengthList

        self.__obsDataCount =len(self.__BandWaveLenthList)
        self.CreateBandsInfo()

        return

    def SetLonLatFile(self,latfile,lonfile,InverseRefFile = None):
        # self.__latFileHandle = self.__HdfOperator.Open(latfile)
        # self.__lonFileHandle = self.__HdfOperator.Open(lonfile)l
        self.__HdfFileHandleList['Latitude'] = self.__HdfOperator.Open(latfile)
        self.__HdfFileHandleList['Longitude'] = self.__HdfOperator.Open(lonfile)
        self.__HdfFileHandleList['InverseRef']  = None
        if InverseRefFile!=None:
            self.__HdfFileHandleList['InverseRef'] = self.__HdfOperator.Open(InverseRefFile)

    def SetL1File(self, file):

        # self.__L1DataFileHandle = self.__HdfOperator.Open(file)
        self.__HdfFileHandleList['L1'] = self.__HdfOperator.Open(file)

        if '_2000M_' in file:
            self.__dataRes = 2000
            self.__dataWidthAndHeight = 5500
            self.__refWidth = 8100
            # self.__obsDataCount = 16
            # self.__BandWaveLenthList = ['0046', '0051', '0064', '0086', '0160', '0230', '0390', '0620', '0700', '0730',
            #                         '0860','0960','1040', '1120', '1230', '1330']
        elif '_0500M' in file:
            self.__dataRes = 500
            self.__dataWidthAndHeight = 22000
            self.__refWidth = 32400
            # self.__obsDataCount = 1
            # self.__BandWaveLenthList = ['0064']
        elif '_1000M' in file:
            self.__dataRes = 1000
            self.__dataWidthAndHeight = 11000
            self.__refWidth = 16200
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

    def GetInverseRef(self):
        if self.__HdfFileHandleList['InverseRef'] is None:
            return None
        line = self.GetDataSet(self.__HdfFileHandleList['InverseRef'], '/', 'LINE_'+str(self.__dataRes))
        pix = self.GetDataSet(self.__HdfFileHandleList['InverseRef'], '/', 'PIX_'+str(self.__dataRes))
        # leftlon = self.__HdfOperator.ReadHdfAttri(self.__HdfFileHandleList['InverseRef'],'/'+'LINE_'+str(self.__dataRes),'LeftLon')
        # toplat = self.__HdfOperator.ReadHdfAttri(self.__HdfFileHandleList['InverseRef'],'/'+'LINE_'+str(self.__dataRes),'TopLat')

        reftoplat,refbottomlat,refleftlon,refrightlon=self.GetInverseRefCorner()
        # refWidth = line.shape[0]
        # refWidth = 32400

        return line,pix,refleftlon[0],reftoplat[0],self.__refWidth

    def GetInverseRefCorner(self):
        if self.__reftoplat == 0:
            self.__reftoplat = self.__HdfOperator.ReadHdfAttri(self.__HdfFileHandleList['InverseRef'],'/'+'LINE_'+str(self.__dataRes),'TopLat')
        
        if self.__refbottomlat == 0:
            self.__refbottomlat = self.__HdfOperator.ReadHdfAttri(self.__HdfFileHandleList['InverseRef'],'/'+'LINE_'+str(self.__dataRes),'BottomLat')
        
        if self.__leftlon == 0:
            self.__leftlon = self.__HdfOperator.ReadHdfAttri(self.__HdfFileHandleList['InverseRef'],'/'+'LINE_'+str(self.__dataRes),'LeftLon')

        if self.__rightlon == 0:
            self.__rightlon = self.__HdfOperator.ReadHdfAttri(self.__HdfFileHandleList['InverseRef'],'/'+'LINE_'+str(self.__dataRes),'RightLon')
   
        return self.__reftoplat,self.__refbottomlat,self.__leftlon,self.__rightlon 

    def GetResolution(self):
        return self.__dataRes

    def GetOBSData(self, band):

        bandname = self.__GetOBSDatasetName(band,self.__dataRes)
        caltableName = 'CAL'+self.OrbitInfo.BandsWavelength[band]
        ret = None
        if bandname!='':

            data=self.GetDataSet(self.__HdfFileHandleList['L1'], '/', bandname)[:,:].astype(N.int32)
            data = data - 1 #yuanbo 20180131 : 0_value problem
            # caltable = self.GetDataSet(self.__HdfFileHandleList['L1'], '/', caltableName)
            caltable = self.__HdfOperator.ReadHdfDataset(self.__HdfFileHandleList['L1'], '/', caltableName)[:].astype(N.float32)
            caltable[60000:] = 65535 #yuanbo 20180719
            data[data>60000]=60001   #yuanbo 20180719            
            height = data.shape[0]
            width = data.shape[1]
            bantype = 1
            if self.OrbitInfo.BandsType[band] == 'REF':
                bantype = 0
            ret=SD.CreateH8CalibrationData(int(width ), int(height),bantype,caltable,data)

        if band=="EVB0046" or band=="EVB0051" or band=="EVB0064" or band=="EVB0086" or band=="EVB0160" or band=="EVB0230":
          print "&&&&&&&&&&&&&&&&&&&&&",band
          #ret[ret == 1000] = 65535 #yuanbo 20180131 : 0_value problem
        elif band=="EVB0390" or band=="EVB0620" or band=="EVB0700" or band=="EVB0730" or band=="EVB0860" or band=="EVB0960" or band=="EVB1040" or band=="EVB1120" or band=="EVB1230" or band=="EVB1330" :
          print "#####################",band
          ret[ret == 0] = 65535 #yuanbo 20180131 : 0_value problem

        del data
        del caltable
        gc.collect()
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

        data = self.__HdfOperator.ReadHdfDataset(filehandle, group, ds)
        startLine = self.startLine
        endlLine = self.endLine
        ret = None
        # startLine=0

       #Interpolate 2016_11_4_yuanbo
        if (ds == 'NOMSunAzimuth' or ds == 'NOMSunZenith') and 	(self.__dataRes == 500 or self.__dataRes ==1000):
            RowNum = len(data)
            ColumnNum =len(data[0])
            InputArray = N.array(data).reshape(-1)
      	    zoomRate = 2000/self.__dataRes
            data = SD.BilinearInterPolateData(int(RowNum),int(ColumnNum),int(zoomRate),InputArray)
            data = data.reshape((RowNum*zoomRate), (ColumnNum*zoomRate))

        if self.__HdfFileHandleList['InverseRef']!=None:
        #     reftoplat,refbottomlat,refleftlon,refrightlon=self.GetInverseRefCorner()
            startLine = 0
        #     endlLine = data.shape[0]/2+1
        #     ret = data[startLine:endlLine, :]
      

        if startLine!= -1 and endlLine!= -1 and  ds!=('LINE_'+str(self.__dataRes)) and ds!=('PIX_'+str(self.__dataRes)) :
        # if startLine!= -1 and endlLine!= -1 :
            ret = data[startLine:endlLine, :]
        elif ds==('LINE_'+str(self.__dataRes)) or ds==('PIX_'+str(self.__dataRes)) :
            # reftoplat,refbottomlat,refleftlon,refrightlon=self.GetInverseRefCorner()
            # startLine = 0
            endlLine = data.shape[0]/2+1
            ret = data[startLine:endlLine, :]
        else:            
            ret = data[:,:]
        
        del data
        gc.collect()
        print "--->",ds
        print ret        
        return ret

    def GetAuxiliaryData(self,dataname):

        dsname = self.__AuxiliaryDataNamesList[dataname]
        ret = None
        if dsname =='':
            return  ret

        ret=self.GetDataSet(self.__HdfFileHandleList[dataname], '/', dsname)

        #RowNum = len(ret)
        #ColumnNum =len(ret[0])
        #InputArray = ret.reshape(-1)
        #zoomRate = 2
        #ret = INTERPOLATE.InterPolateData(int(RowNum),int(ColumnNum),int(zoomRate),InputArray)
        #ret = ret.reshape(RowNum*2, ColumnNum*2)

        return ret


    def GetAuxiliaryDataNamesList(self):
        return self.__AuxiliaryDataNamesList


    def SetDataDescription(self, value):
        self.__description = value

    def GetDataDescription(self):
        if self.__description == 'NULL':
            self.__description = self.GetParameter().GetParamDescription()+'_'+str(self.GetParameter().ProjectResolution)
        return  self.__description



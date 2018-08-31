from DataOuter import *
from HdfOperator import *
from DataProvider.DataProvider import *
import numpy as N
import gc

class HdfDataOuter(DataOuter):



    def __init__(self):
        super(HdfDataOuter, self).__init__()
        self.__HdfOperator = HdfOperator()

        self.__dataProvider = DataProvider()
        return

    def Dispose(self):
        self.__dataProvider = None

    def Save(self,projResult, dataProvider):
        self.__dataProvider = dataProvider


        para = self.getParameter()
        resolution = para.ProjectResolution

        dataDescription = self.__dataProvider.GetDataDescription()

        # savePath,saveFile =  os.path.split(savefile)
        # saveFile = saveFile.upper()
        # saveFile=saveFile.replace('.HDF','_Proj.HDF')

        saveFile = para.OutputPath+dataDescription+'_'+para.ProjectTaskName+'.HDF'


        if os.path.exists(saveFile):
            os.remove(saveFile)

        fileHandle = self.__HdfOperator.Open(saveFile)



        Evbcnt = dataProvider.GetOBSDataCount()
        bandWaveLength = dataProvider.OrbitInfo.BandsWavelength
        if para.IsAuxiliaryFileMode == False:
            # for i in xrange(1,Evbcnt+1):
            for wavelength in bandWaveLength:
                self.WriteDataset(wavelength, projResult, fileHandle, resolution)
                self.WriteDatasetAttribute(fileHandle,wavelength)

        AuxiliaryDataNamesList=dataProvider.GetAuxiliaryDataNamesList()
        for auxName in AuxiliaryDataNamesList:
            self.WriteDataset(auxName, projResult, fileHandle, resolution)
        # self.WriteData('SensorAzimuth', projResult, fileHandle, resolution)

        # self.__HdfOperator.Close(fileHandle)
        # return
        #
        # self.WriteData('SensorZenith', projResult, fileHandle, resolution)
        # self.WriteData('SolarAzimuth', projResult, fileHandle, resolution)
        # self.WriteData('SolarZenith', projResult, fileHandle, resolution)

        for attr in projResult.ResultInfo.keys():
            self.__HdfOperator.WriteHdfGroupAttribute(fileHandle, attr, projResult.ResultInfo[attr])
        # self.__HdfOperator.WriteHdfDataset(fileHandle, '/', 'U', U)
        # self.__HdfOperator.WriteHdfDataset(fileHandle, '/', 'V', V)
        self.__HdfOperator.Close(fileHandle)
        return

    def WriteDataset(self, datasetname, projResult, fileHandle, resolution):
        data = None
        datatype =0
        if 'EVB' in datasetname:
            data = (self.__dataProvider.GetOBSData(datasetname)).astype(N.int32)
        else:
            data = self.__dataProvider.GetAuxiliaryData(datasetname)
            #if (data.dtype == N.float)|(data.dtype == N.float32)|(data.dtype == N.float64):
            if data.dtype in (N.float, N.float32,N.float64 ,N.dtype('>f4')):  #pixel_surface_elevation has dtype:  >f4
                data = data.astype(N.float32)
                datatype = 1                        
            elif(data.dtype == N.uint8):   #2016/10/9
                datatype = 80              #2016/10/9
            elif(data.dtype == N.int8):    #2016/10/9
                datatype = 81              #2016/10/9
            elif(data.dtype == N.int16):  #2016/10/9
                datatype = 16              #2016/10/9 
            else:
                data = data.astype(N.int32)

        if data is not None:
            #if ('ongitude' in datasetname) or ('atitude' in datasetname):
            #    savedata = projResult.CreateLatLonData(datasetname,resolution) #only useful for 'latlong proj'
            #else:   
            #    savedata = projResult.CreateSaveData(data,resolution,datatype)
            
            #savedata = projResult.CreateSaveData(data,resolution,datatype)
            
            savedata = projResult.CreateSaveData(data,resolution,datatype,datasetname)

            if 'EVB' in datasetname:
                self.__HdfOperator.WriteHdfDataset(fileHandle, '/', datasetname, savedata.astype(N.uint16))
            else:
                self.__HdfOperator.WriteHdfDataset(fileHandle, '/', datasetname, savedata)
            del data
            del savedata
            gc.collect()
            print 'Save '+ str(resolution)+' M'+datasetname

    def WriteDatasetAttribute(self,fileHandle,datasetname):
        if 'EVB' in datasetname:
            orbitInfo = self.__dataProvider.OrbitInfo
            self.__HdfOperator.WriteHdfDatasetAttribute(fileHandle, '/', datasetname, 'WaveLength', orbitInfo.BandsWavelength[datasetname])
            bandstype = orbitInfo.BandsType[datasetname]
            if bandstype == 'REF':
                self.__HdfOperator.WriteHdfDatasetAttribute(fileHandle, '/', datasetname, 'slope',0.001)
            else:
                self.__HdfOperator.WriteHdfDatasetAttribute(fileHandle, '/', datasetname, 'slope', 0.01)
        return



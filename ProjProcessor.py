# -*- coding: utf-8 -*-

from DataOuter.DataOuter import *
from DataProvider.DataProvider import *
from ProjectTransformer import *
from ProjResult import *
import numpy as N
import gc

class ProjProcessor(object):

    # __dataProvider = DataProvider()

    # __ProjParam = ProjParameters()
    # __dataOuter = DataOuter()

    # __projResult = ProjResult()

    def __init__(self, dataprovider, dataouter, parameters):
        self.__dataProvider = dataprovider
        self.__ProjParam = parameters
        self.__dataOuter = dataouter
        self.__ProjTransformer = ProjTransformer()
        self.__projResult = ProjResult()

        if self.__ProjParam.ProjectResolution==0:
            self.__ProjParam.ProjectResolution = dataprovider.GetResolution()

        self.__dataProvider.SetParameter(parameters)

        self.__dataOuter.Parameter=parameters

        self.__ProjParam.register(self)

        self.__ProjParam.data_changed()
        return

    def Dispose(self):
        self.__dataProvider.Dispose()
        self.__dataOuter.Dispose()
        self.__projResult.Dispose()
        self.__ProjParam = None

    def OnParametersUpdate(self):
        self.__projResult.NeedUpdate = True
        return


    def PerformProj(self):


       
        # cornerU, cornerV=self.CalProjCorner()
        # MinU, MinV, MaxU, MaxV = self.CalProjectMinMax(cornerU,cornerV)
        
        # self.__projResult.MaxU = MaxU
        # self.__projResult.MaxV = MaxV
        # self.__projResult.MinV = MinV
        # self.__projResult.MinU = MinU

        # self.__dataOuter.Save(self.__projResult,self.__dataProvider)
        
        # return 


        proj = self.__ProjParam.DstProj
        if 'InverRef' in self.__ProjParam.ProjName:
            # inverseRefLine,inverseRefPix = self.__dataProvider.GetInverseRef()
            inverseRefLine,inverseRefPix,leftlon,toplat,refWidth=self.__dataProvider.GetInverseRef()
            self.__projResult.SetInversRef(inverseRefLine,inverseRefPix,leftlon,toplat,refWidth)
            self.__projResult.InverseCal = True
        else:

            print 'prepare proj transform......'
            lat = self.__dataProvider.GetLatitude()
            lon = self.__dataProvider.GetLongitude()
            U, V = self.__ProjTransformer.LatlonToProjUV(lon,lat,proj)
        
            del lon
        
            del lat
            gc.collect()

            self.__projResult.U = U
            self.__projResult.V = V
        self.__projResult.SetDstProj(proj)

        # self.SetResultInfo()
        self.CreateResultInfo()
        if ('InverRef' in self.__ProjParam.ProjName) is False:
            rangemask =(V[:,:]<= self.__projResult.MaxV) & (V[:,:]>= self.__projResult.MinV) & \
                 (U[:,:]<= self.__projResult.MaxU) & (U[:,:]>= self.__projResult.MinU)#返回时是true和false的数组


            self.__projResult.LatLonRangeMask = rangemask

        self.__dataOuter.Save(self.__projResult,self.__dataProvider)

    def PerformInveProj(self):
        pass

    def CalProjCorner(self):
        minlon = self.__ProjParam.ProjRange.MinLon
        maxlon = self.__ProjParam.ProjRange.MaxLon
        minlat = self.__ProjParam.ProjRange.MinLat
        maxlat = self.__ProjParam.ProjRange.MaxLat
        # centrallon=(maxlon-minlon)/2+minlon
        centrallon = self.__ProjParam.CentralLon
        if "lcc" in self.__ProjParam.DstProj.srs or "aea" in self.__ProjParam.DstProj.srs:
            lon=N.array([minlon,minlon,maxlon,maxlon,centrallon])
            lat=N.array([minlat,maxlat,minlat,maxlat,minlat])
        else:
            lon = N.array([minlon,minlon,maxlon,maxlon])
            lat = N.array([minlat,maxlat,minlat,maxlat])

        cornerU,cornerV = self.__ProjTransformer.LatlonToProjUV(lon,lat,self.__ProjParam.DstProj)
        return cornerU,cornerV

    def CalCenterUV(self,MinU, MinV, MaxU, MaxV):
        centU = (MaxU-MinU)/2+MinU
        centV = (MaxV-MinV)/2+MinV
        return  centU,centV

    def CalProjectMinMax(self, U, V):
        MinU = N.min(U[:]).astype(N.float32)
        MinV = N.min(V[:]).astype(N.float32)
        MaxU = N.max(U[:]).astype(N.float32)
        MaxV = N.max(V[:]).astype(N.float32)
        return MinU, MinV, MaxU, MaxV

    def CreateResultInfo(self):
        self.__projResult.ResultInfo={'Satellite Name':self.__dataProvider.OrbitInfo.Sat}
        self.__projResult.ResultInfo['SensorName'] = self.__dataProvider.OrbitInfo.Sensor
        self.__projResult.ResultInfo['ProjString'] = self.__ProjParam.GetParamDescription()
        self.__projResult.ResultInfo['UResolution'] = int(self.__ProjParam.ProjectResolution)
        self.__projResult.ResultInfo['VResolution'] = int(self.__ProjParam.ProjectResolution)
        if ('InverRef' in self.__ProjParam.ProjName) or ('latlong' in self.__ProjParam.ProjName):
            self.__projResult.ResultInfo['UResolution'] = (self.__ProjParam.ProjectResolution)/100000
            self.__projResult.ResultInfo['VResolution'] = (self.__ProjParam.ProjectResolution)/100000

        cornerU, cornerV=self.CalProjCorner()
        MinU, MinV, MaxU, MaxV = self.CalProjectMinMax(cornerU,cornerV)
        centU, centV = self.CalCenterUV(MinU, MinV, MaxU, MaxV)
        centlon, centlat = self.__ProjTransformer.ProjUVToLatlon(centU, centV, self.__ProjParam.DstProj)

        self.__projResult.MaxU = MaxU
        self.__projResult.MaxV = MaxV
        self.__projResult.MinV = MinV
        self.__projResult.MinU = MinU
        self.__projResult.ResultInfo['MinLon'] = self.__ProjParam.ProjRange.MinLon
        self.__projResult.ResultInfo['MaxLon'] = self.__ProjParam.ProjRange.MaxLon
        self.__projResult.ResultInfo['MinLat'] = self.__ProjParam.ProjRange.MinLat
        self.__projResult.ResultInfo['MaxLat'] = self.__ProjParam.ProjRange.MaxLat
        self.__projResult.ResultInfo['CenterLatitude'] = centlat
        self.__projResult.ResultInfo['CenterLongitude'] = centlon


    def SetResultInfo(self):

        cornerU, cornerV=self.CalProjCorner()
        MinU, MinV, MaxU, MaxV = self.CalProjectMinMax(cornerU,cornerV)
      
        self.__projResult.MaxU = MaxU
        self.__projResult.MaxV = MaxV
        self.__projResult.MinV = MinV
        self.__projResult.MinU = MinU

        if "Latlon" in self.__ProjParam.ProjName:
            resolution=float(self.__ProjParam.resolution)/100000
        else:
            resolution=self.__ProjParam.resolution

        bandlist=self.__ProjParam.BandWaveLengthList
        self.__projResult.ResultInfo=dict()
        self.__projResult.ResultInfo['Sensor Name']=str(self.__ProjParam.insName)
        self.__projResult.ResultInfo['Satellite Name']=str(self.__ProjParam.satName)
        self.__projResult.ResultInfo['Data Date']=str(self.__ProjParam.TimeFlag[0:4]+"-"+self.__ProjParam.TimeFlag[4:6]+"-"+self.__ProjParam.TimeFlag[6:8])
        self.__projResult.ResultInfo['Data Time']=str(self.__ProjParam.TimeFlag[8:10]+":"+self.__ProjParam.TimeFlag[10:12]+":00")
        self.__projResult.ResultInfo['Projection Type']=str(self.__ProjParam.ProjName)
        self.__projResult.ResultInfo['Standard Latitude 1']=N.float32(self.__ProjParam.StandardLat[0])
        self.__projResult.ResultInfo['Standard Latitude 2']=N.float32(self.__ProjParam.StandardLat[1])
        self.__projResult.ResultInfo['Projection Center Longitude']=N.float32((self.__ProjParam.ProjRange.MaxLon-self.__ProjParam.ProjRange.MinLon)/2+self.__ProjParam.ProjRange.MinLon)
        if "Latlon" in str(self.__ProjParam.ProjName):
            resolution=N.float32(float(self.__ProjParam.resolution)/100000)
        else:
            resolution=N.float32(self.__ProjParam.resolution)
        self.__projResult.ResultInfo['Longitude Precision']=resolution
        self.__projResult.ResultInfo['Latitude Precision']=resolution
        self.__projResult.ResultInfo['Minimum Latitude']=N.float32(self.__ProjParam.ProjRange.MinLat)

        self.__projResult.ResultInfo['Maximum Latitude']=N.float32(self.__ProjParam.ProjRange.MaxLat)
        self.__projResult.ResultInfo['Minimum Longitude']=N.float32(self.__ProjParam.ProjRange.MinLon)
        self.__projResult.ResultInfo['Maximum Longitude']=N.float32(self.__ProjParam.ProjRange.MaxLon)
        self.__projResult.ResultInfo['x_0']=N.int32(self.__ProjParam.XY[0])
        self.__projResult.ResultInfo['y_0']=N.int32(self.__ProjParam.XY[1])
        self.__projResult.ResultInfo['Numbers of Bands']=N.int16(len(bandlist))

        bandlist=N.array([ int(i) for i in bandlist ]).astype(N.int16)

        self.__projResult.ResultInfo['Band_names']=bandlist.astype(N.int16)

        self.__projResult.ResultInfo['Numbers of RefSB Bands']=N.int16(self.__dataProvider.RefBandNum)#N.int16(bandlist[bandlist<20].size)
        self.__projResult.ResultInfo['RefSB Band_names']=N.array(self.__dataProvider.RefBandName).astype(N.int16)#bandlist[bandlist<20].astype(N.int16)
        self.__projResult.ResultInfo['Numbers of Emissive Bands']=N.int16(self.__dataProvider.EmiBandNum)#N.int16(bandlist[bandlist>=20].size)
        self.__projResult.ResultInfo['Emissive Band_names']=N.array(self.__dataProvider.EmiBandName).astype(N.int16)#bandlist[bandlist>=20].astype(N.int16)
        self.__projResult.ResultInfo['CenterPoint Longitude']=N.float64((self.__ProjParam.ProjRange.MaxLon-self.__ProjParam.ProjRange.MinLon)/2+self.__ProjParam.ProjRange.MinLon)
        self.__projResult.ResultInfo['CenterPoint Latitude']=N.float64((self.__ProjParam.ProjRange.MaxLat-self.__ProjParam.ProjRange.MinLat)/2+self.__ProjParam.ProjRange.MinLat)

        height,width =self.__projResult.CalProjectWidthAndHeight(MinU, MinV, MaxU, MaxV,float(resolution))

        print 'height = %s,  width = %s' % (str(height),str(width))
        
        self.__projResult.ResultInfo['Piexl Height']=N.int32(height)
        self.__projResult.ResultInfo['Piexl Width']=N.int32(width)

        self.__projResult.ResultInfo['Minimum X']=N.float32(MinU)
        self.__projResult.ResultInfo['Maximum X']=N.float32(MaxU)
        self.__projResult.ResultInfo['Minimum Y']=N.float32(MinV)
        self.__projResult.ResultInfo['Maximum Y']=N.float32(MaxV)

        Attr=self.__dataProvider.GetL1HandlelistAttr("L1")
        self.__projResult.ResultInfo['Orbit Direction']=Attr["Orbit Direction"]
        self.__projResult.ResultInfo['Day Or Night Flag']=Attr["Day Or Night Flag"]
        self.__projResult.ResultInfo['Earth Radius']=N.float32(6378.137)

        self.__dataProvider.projResult = self.__projResult

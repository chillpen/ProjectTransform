# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from DataOuter.HdfDataOuter import *
# from DataProvider.H8DataProvider import *
# from DataProvider.FY3AVirrProvider import *
from ProjProcessor import *

class ParameterParser(object):
    def parseXML(self,xmlfile):
        tree = ET.parse(xmlfile)#调用elementtree
        root = tree.getroot() #获取根节点

        __minlat = 0
        __minlon = 0
        __maxlat = 0
        __maxlon = 0
        __resolution = 0
        __CentralLon = 0
        __method = None
        __format = None
        __TaskName = None
        bandWaveLenth = ''
        for ProjInfor in root.iter('ProjInfor'):#过滤出所有projinfor标签，获取投应的格式，掩模名字，方法，分辨率，中央经线
            self.__format = ProjInfor.find('ProjFormat').text#查找标签下的第一个projformat标签
            self.__TaskName = ProjInfor.find('ProjTaskName').text
            self.__method = ProjInfor.find('ProjMethod').text
            self.__resolution = ProjInfor.find('Resolution').text
            self.__CentralLon = ProjInfor.find('CentralLon').text
            # self.StandardLat1= ProjInfor.find('StandardLat1').text
            # self.StandardLat2= ProjInfor.find('StandardLat2').text
            # self.X_0= ProjInfor.find('X_0').text
            # self.Y_0= ProjInfor.find('Y_0').text
            self.resolution=self.__resolution

        for projrange in root.iter('ProjRange'):#获取图像的范围
            self.__maxlon = projrange.find('MaxLon').text
            self.__minlon = projrange.find('MinLon').text
            self.__maxlat = projrange.find('MaxLat').text
            self.__minlat = projrange.find('MinLat').text

        for BandsToProj in root.iter('BandsToProj'):#获取波段波长
            bandWaveLenth = BandsToProj.find('BandWaveLength').text
            # self.__minlon = BandsToProj.find('MinLon').text
            # self.__maxlat = BandsToProj.find('MaxLat').text
            # self.__minlat = BandsToProj.find('MinLat').text

        # for Orientation in root.iter('Orientation'):
        #     self.__IsSolarZenith = Orientation.find('SolarZenith').text
        #     self.__IsSolarAzimuth = Orientation.find('SolarAzimuth').text
        #     self.__IsSensorZenith = Orientation.find('SensorZenith').text
        #     self.__IsSensorAzimuth = Orientation.find('SensorAzimuth').text
        #     self.__IsHeight = Orientation.find('Height').text


        param = ProjParameters()#在parameters.py中有定义，是个存储参数的类，下面是从xml读到的信息传递给param SET
        param.ProjRange = ProjRange(int(self.__minlat),int(self. __maxlat), int(self.__minlon), int(self.__maxlon))
        param.DstProj = Proj(proj="latlong", datum='WGS84', lon_0=int(self.__CentralLon))
        # param.DstProj = self.UpadateDstProj(self.__method )
        param.ProjName = 'InverRef'
        #param.DstProj = Proj(proj=self.__method, datum='WGS84')
        # param.StandardLat=[self.StandardLat1,self.StandardLat2]
        # param.XY=[self.X_0,self.Y_0]
        param.resolution= self.resolution
        param.ProjectTaskName = self.__TaskName
        param.BandWaveLengthList = bandWaveLenth.split(',')#用逗号分开
        param.ProjectResolution = float(self.__resolution)#

        # param.AuxiliaryDataList['SolarZenith'] = int(self.__IsSolarZenith)
        # param.AuxiliaryDataList['SolarAzimuth'] = int(self.__IsSolarAzimuth)
        # param.AuxiliaryDataList['SensorZenith'] = int(self.__IsSensorZenith)
        # param.AuxiliaryDataList['SensorAzimuth'] = int(self.__IsSensorAzimuth)
        # param.AuxiliaryDataList['Height'] = int(self.__IsHeight)
        param.CentralLon = int(self.__CentralLon)
        return param

    def UpadateDstProj(self,ProjName):
        if "Latlon" in ProjName:
            self.__method="latlong"
            self.DstProj=Proj(proj=self.__method, ellps="krass",lon_0=int(self.__CentralLon),x_0="0" ,y_0="0",units="m" ,k="1")
            return self.DstProj
        if "InverRef" in ProjName:
            self.__method="InverRef"
            self.DstProj=Proj(proj="latlong", ellps="krass",lon_0=int(self.__CentralLon),x_0="0" ,y_0="0",units="m" ,k="1")
            return self.DstProj
        elif "Mercator" in ProjName:
            self.__method="merc"
            self.DstProj=Proj(proj=self.__method, ellps="krass",lon_0=int(self.__CentralLon),x_0="0" ,y_0="0",units="m" ,k="1",datum="WGS84")
            return  self.DstProj
        elif "Lambert" in ProjName:
            self.__method="lcc"
            self.DstProj=Proj(proj=self.__method, ellps="krass",lat_1=int(self.StandardLat1),lat_2=int(self.StandardLat2),lon_0=int(self.__CentralLon),x_0=int(self.X_0) ,y_0=int(self.Y_0),units="m" ,k="1",datum="WGS84")
            #+proj=lcc +lat_1=34.33333333333334 +lat_2=36.16666666666666 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +datum=NAD83 +units=m +no_defs '
            return self.DstProj
        elif "Stereographic" in ProjName:
            self.__method="stere"
            self.DstProj=Proj(proj=self.__method, ellps="krass",lat_0=int(self.StandardLat1),lat_ts=int(self.StandardLat2),lon_0=int(self.__CentralLon),x_0=int(self.X_0) ,y_0=int(self.Y_0),units="m" ,k="1")
            return self.DstProj
        elif "Albers" in ProjName:
            self.__method="aea"
            self.DstProj=Proj(proj=self.__method, ellps="krass",lat_1=int(self.StandardLat1),lat_2=int(self.StandardLat2),lon_0=int(self.__CentralLon),x_0=int(self.X_0) ,y_0=int(self.Y_0),units="m" ,k="1")
            #+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs
            return self.DstProj
        self.DstProj=Proj(proj=self.__method, ellps="krass",lat_1=int(self.StandardLat1),lat_2=int(self.StandardLat2),lon_0=int(self.__CentralLon),x_0=int(self.X_0) ,y_0=int(self.Y_0),units="m" ,k="1")
        return self.DstProj
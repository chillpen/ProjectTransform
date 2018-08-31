from DataOuter.HdfDataOuter import *
from DataProvider.H8DataProvider import *
from DataProvider.FY3AVirrProvider import *
from ProjProcessor import *
import sys
from ParameterParser import *
import multiprocessing


L1FilePath = ''


def CreateStdProjProvider(resolution):
    provider = H8Dataprovider()

    #Latfile = '/FY4COMM/FY4A/COM/fygatNAV.Himawari08.xxxxxxx.000001(2000).hdf'
    #Lonfile = '/FY4COMM/FY4A/COM/fygatNAV.Himawari08.xxxxxxx.000002(2000).hdf'
    Latfile = Lonfile = '/FY4COMM/FY4A/COM/AHI8_OBI_2000M_NOM_LATLON.HDF'

    L1file = L1FilePath+'AHI8_OBI_2000M_NOM_' + sys.argv[1] + '.hdf'

    if resolution == 1000:
        Latfile = '/FY4COMM/FY4A/COM/AHI8_OBI_1000M_NOM_LAT.hdf'
        Lonfile = '/FY4COMM/FY4A/COM/AHI8_OBI_1000M_NOM_LON.hdf'
        L1file = L1FilePath+'AHI8_OBI_1000M_NOM_' + sys.argv[1] + '.hdf'       
    elif resolution == 500:
        Latfile = '/FY4COMM/FY4A/COM/AHI8_OBI_500M_NOM_LAT.HDF'
        Lonfile = '/FY4COMM/FY4A/COM/AHI8_OBI_500M_NOM_LON.HDF'
        L1file = L1FilePath+'AHI8_OBI_0500M_NOM_' + sys.argv[1] + '.hdf'


    provider.SetLonLatFile(Latfile,Lonfile)

    print sys.argv[1]
    if os.path.exists(L1file) == False:
        print("L1file do not exist!!:")    
        print(L1file)
        exit()
    elif os.path.getsize(L1file) < 1024:
        print("ERROR:L1file exsits but is empty!!!")
        exit()    
    provider.SetL1File(L1file)
    provider.SetDataDescription('Himawari8_OBI_'+sys.argv[1])
    
    if resolution == 4000 or resolution == 2000:
        AuxiliaryName = dict()
        AuxiliaryPath = dict()
        AuxiliaryName['SunAzimuth'] = 'NOMSunAzimuth'
        AuxiliaryName['SunZenith'] = 'NOMSunZenith'
        AuxiliaryPath['SunAzimuth'] = AuxiliaryPath['SunZenith'] = L1file
        provider.SetAuxiliaryDataFile(AuxiliaryName, AuxiliaryPath)
    if  resolution == 1000 or resolution == 500:
        AuxiliaryName = dict()
        AuxiliaryPath = dict()
        AuxiliaryName['SunAzimuth'] = 'NOMSunAzimuth'
        AuxiliaryName['SunZenith'] = 'NOMSunZenith'
        AuxiliaryPath['SunAzimuth'] = AuxiliaryPath['SunZenith'] = L1file = L1FilePath+'AHI8_OBI_2000M_NOM_' + sys.argv[1] + '.hdf'
        provider.SetAuxiliaryDataFile(AuxiliaryName, AuxiliaryPath)
    return  provider

def ProcessProj(param,resolution):

    provider = CreateStdProjProvider(resolution)

    dataouter = HdfDataOuter()

    processor = ProjProcessor(provider, dataouter, param)
    processor.PerformProj()
    processor.Dispose()

def ProcessAuxProj(resolution):
    paramparser = ParameterParser()
    auxparam = paramparser.parseXML(sys.argv[2])
    auxparam.OutputPath = sys.argv[5]								
    auxparam.ProjectResolution = resolution
##    auxparam.IsAuxiliaryFileMode = True
##    ProcessProj(auxparam, resolution, True)
    ProcessProj(auxparam, resolution)
    
    
    
    
def CheckAuxiliaryData(xmlFileName,resolution):
    print "did i come here"
    fileHandle = xml.etree.ElementTree.parse(xmlFileName)
    root = fileHandle.getroot()
    maxlon = 0
    minlon = 0
    maxlat = 0
    minlat = 0
    for projrange in root.iter('ProjRange'):
      maxlon = projrange.find('MaxLon').text
      minlon = projrange.find('MinLon').text
      maxlat = projrange.find('MaxLat').text
      minlat = projrange.find('MinLat').text          
    tempString = "_"+minlat+"-"+maxlat+"-"+minlon+"-"+maxlon+"_"+resolution
    AuxiliaryFilePath = "/FY4COMM/FY4A/COM/PRJ/"
    files = os.listdir(AuxiliaryFilePath)
    AuxiliaryFiles = []
    result = ""
    print tempString
    for filepath in files:
        #result = re.match(tempString,filepath)
        if (tempString in filepath) and (resolution in filepath):
          AuxiliaryFiles.append(filepath)
    print len(AuxiliaryFiles)
    if len(AuxiliaryFiles) == 0:
      print "Auxiliary File do not Exist!"
      return 1
    else:
      print "Auxiliary File Exists!"    
    return 0

import xml.etree.ElementTree 
import os     
if __name__ == '__main__':
    DataResolution = sys.argv[3]  #2017_4_7
    DataTime = sys.argv[1]        #2017_4_7
    DataTime = int(DataTime[9:11])#2017_4_7
    if((DataResolution == '500' or DataResolution == '1000') and (DataTime>12 and DataTime<22)):
        exit()	
    L1FilePath = sys.argv[4]
    paramparser = ParameterParser()
    param = paramparser.parseXML(sys.argv[2])
#    param.OutputPath = '/FY4COMM/FY4A/L2/AGRIX/PRJ/' #2016.10.12
    param.OutputPath = sys.argv[5]									
    # ProcessProj(param, 2000,False)
    #
    # p1 = multiprocessing.Process(target = ProcessProj, args = (param,2000,False,))
    # p1.start()
    #
    # p2 = multiprocessing.Process(target = ProcessProj, args = (param,1000,False,))
    # p2.start()
    #
    # p2 = multiprocessing.Process(target = ProcessProj, args = (param,500,False,))
    # p2.start()
    L1FilePath = sys.argv[4]
    ProcessProj(param, int(sys.argv[3]))

#
#python /FY4COMM/FY4A/EXE/ProjectTransform/FY4AAutoProj.py     20171120_0000  /FY4COMM/FY4A/PAR/SCH/H8_2000m_Proj.xml 2000 /FY4COMM/FY4A/L1/AGRIX/ /FY4COMM/FY4A/L2/AGRIX/PRD/
#
    #yuanbo 20171115-->
    doAuxiProj = CheckAuxiliaryData(sys.argv[2],DataResolution)
    print doAuxiProj
    if(doAuxiProj == 1):
      print "Auxiliary Project Begin"
      command = "python "+sys.argv[0].replace("FY4AAutoProj.py","FY4AAuxiliaryAutoProj.py")+" 0 "+" "+sys.argv[2]+" "+DataResolution+" "+sys.argv[4]+" /FY4COMM/FY4A/COM/PRJ/"
      print command
      os.system(command)
    #yuanbo 20171115<--
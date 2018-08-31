from DataOuter.HdfDataOuter import *
from DataProvider.H8DataProvider import *
from DataProvider.FY3AVirrProvider import *
from ProjProcessor import *
import sys
from ParameterParser import *
import multiprocessing
import AuxiliaryDict

#L1FilePath = ''

def CreateAuxilaryProvider(resolution):
    provider = H8Dataprovider()

    #Latfile = AuxiliaryDict.LatitudeFilePath        # not static dataset
    #Lonfile = AuxiliaryDict.LongitudeFilePath       # not static dataset
    Latfile = AuxiliaryDict.AuxiliaryDataDict['Latitude']
    Lonfile = AuxiliaryDict.AuxiliaryDataDict['Longitude']
    InverRefFile = '/FY4COMM/FY4A/COM/LATLON_TO_PIXLINE_'+str(resolution)+'.HDF'
    if resolution == 500:
      InverRefFile = '/FY4COMM/FY4A/COM/LATLON_TO_PIXLINE_0500.HDF'
    print InverRefFile
    provider.SetLonLatFile(Latfile,Lonfile,InverRefFile)
    provider.SetAuxiliaryDataFile(AuxiliaryDict.AuxiliaryNameDict, AuxiliaryDict.AuxiliaryDataDict)

    return  provider


def ProcessProj(param, resolution):

    provider = CreateAuxilaryProvider(resolution)

    dataouter = HdfDataOuter()

    processor = ProjProcessor(provider, dataouter, param)
    processor.PerformProj()
    processor.Dispose()

def ProcessAuxProj(resolution):
    paramparser = ParameterParser()
    auxparam = paramparser.parseXML(sys.argv[2])
    #auxparam.OutputPath = '/FY4COMM/FY4A/COM/PRJ/' #yuanbo 20171026
    auxparam.OutputPath = sys.argv[5] #yuanbo 20171026

    auxparam.ProjectResolution = resolution
    auxparam.IsAuxiliaryFileMode = True
    ProcessProj(auxparam, resolution)
if __name__ == '__main__':

    paramparser = ParameterParser()
    param = paramparser.parseXML(sys.argv[2])
    #param.OutputPath = '/FY4COMM/FY4A/L2/AGRIX/PRJ/'		#2016_10_14
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
#    L1FilePath = sys.argv[4]
#    ProcessProj(param, int(sys.argv[3]),False)
#    auxfile = '/FY4COMM/FY4A/COM/PRJ/'+ param.GetParamDescription() + '_'+sys.argv[3]+'_'+param.ProjectTaskName+'.HDF'		#2016_10_14
    #auxfile = sys.argv[5]+ param.GetParamDescription() + '_'+sys.argv[3]+param.ProjectTaskName+'.HDF'
    auxfile = sys.argv[5]+ param.GetParamDescription() + '_'+sys.argv[3]+'_'+param.ProjectTaskName+'.HDF'
    #auxfile ='/home/bozi/Downloads/TestData/'+ param.GetParamDescription() + '_'+'2000'+'_'+param.ProjectTaskName+'.HDF'
    if os.path.exists(auxfile) == False:
        ProcessAuxProj(int(sys.argv[3]))
        #command = "mv "+'"'+auxfile+'"'+" "+'"'+auxfile_2+'"'
        #print command
        #os.system(command)
    else:
          print "auxiliary file already exist! -->"
          print auxfile

    
    
        #ProcessAuxProj(2000)
    # auxfile = param.OutputPath + param.GetParamDescription() + '_1000_Proj.HDF'
    # if os.path.exists(auxfile) == False:
    #     ProcessAuxProj(1000)

    # auxfile = param.OutputPath + param.GetParamDescription() + '_500_Proj.HDF'
    # if os.path.exists(auxfile) == False:
    #     ProcessAuxProj(500)

    # p1 = multiprocessing.Process(target = ProcessProj, args = (param,2000,))
    # p1.start()
    #
    # p2 = multiprocessing.Process(target = ProcessProj, args = (param,1000,))
    # p2.start()
    #
    # p3 = multiprocessing.Process(target = ProcessProj, args = (param,500,))
    # p3.start()
    # ProcessProj(param,2000)
    # ProcessProj(param, 1000)
    # ProcessProj(param, 500)
from DataOuter.HdfDataOuter import *
from DataProvider.FY4A_DAT_Provider import *
from ProjProcessor import *
import sys
from ParameterParser import *
import multiprocessing


#L1FilePath = ''

def CreateAuxilaryProvider(resolution):
    provider = FY4A_DAT_Provider()
    AuxiliaryNameDict = {}
    AuxiliaryDataDict = {}
    AuxiliaryNameDict['f30yInterpSSTData'] = 'f30yInterpSSTData'
    AuxiliaryDataDict['f30yInterpSSTData'] = '/FY4COMM/FY4A/PAR/AGRIX/SSTData/30YearAvgSSTData/AHI8_OBI_2000M_NOM_XXXX'+sys.argv[1][-9:-5]+'.dat'
    Latfile =Lonfile= '/FY4COMM/FY4A/COM/AHI8_OBI_2000M_NOM_LATLON.HDF'

    provider.SetLonLatFile(Latfile,Lonfile)
    provider.SetAuxiliaryDataFile(AuxiliaryNameDict, AuxiliaryDataDict)

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
    auxparam.OutputPath = '/FY4COMM/FY4A/PAR/AGRIX/SSTData/30YearAvgSSTData_HDF/'
    auxparam.ProjectResolution = resolution
    auxparam.IsAuxiliaryFileMode = True
    ProcessProj(auxparam, resolution)
if __name__ == '__main__':

    paramparser = ParameterParser()
    param = paramparser.parseXML(sys.argv[2])
    auxfile_final = '/FY4COMM/FY4A/PAR/AGRIX/SSTData/30YearAvgSSTData_HDF/Himawari8_30YearAvgSST_XXXX'+sys.argv[1][-9:-5]+'_'+sys.argv[3]+'M_'+param.ProjectTaskName+'.HDF'
    auxfile = '/FY4COMM/FY4A/PAR/AGRIX/SSTData/30YearAvgSSTData_HDF/'+ param.GetParamDescription() + '_'+sys.argv[3]+'_'+param.ProjectTaskName+'.HDF'
    #print    auxfile_final
    #print auxfile
    #res = "/FY4COMM/FY4A/PAR/AGRIX/SSTData/30YearAvgSSTData_HDF/Himawari8_30YearAvgSST_XXXX{MonthDay}_{Resolution}M_{prj}.HDF".format(
    #	MonthDay=sys.argv[1][-9:-5],
    #	Resolution=sys.argv[3],
    #	prj=param.ProjectTaskName)
    if os.path.exists(auxfile_final) == False:
        ProcessAuxProj(int(sys.argv[3]))
        os.rename(auxfile,auxfile_final)
            #auxfile

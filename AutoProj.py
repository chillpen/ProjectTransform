from DataOuter.HdfDataOuter import *
from DataProvider.H8DataProvider import *
from DataProvider.FY3AVirrProvider import *
from ProjProcessor import *
import sys
from ParameterParser import *
import multiprocessing


L1FilePath = ''
Projstring = ''
paramFilePath= ''
def ProviderFactory(isCreateAuxfile,resolution):
    provider = None
    if isCreateAuxfile:
        provider = CreateAuxilaryProvider(resolution)
    else:
        provider = CreateStdProjProvider(resolution)

    return provider


def CreateAuxilaryProvider(resolution):
    provider = H8Dataprovider()

    Latfile='/FY4COMM/FY4A/COM/fygatNAV.Himawari08.xxxxxxx.000001(2000).hdf'
    Lonfile = '/FY4COMM/FY4A/COM/fygatNAV.Himawari08.xxxxxxx.000002(2000).hdf'
    pixel_desert_mask = '/FY4COMM/FY4A/PAR/AGRIX/ancillary_data/navigation/fygatNAV.Himawari08.xxxxxxx.2000m.hdf' #add on 2016.10.8
    if resolution == 1000:
        Latfile = '/FY4COMM/FY4A/COM/AHI8_OBI_1000M_NOM_LAT.hdf'
        Lonfile = '/FY4COMM/FY4A/COM/AHI8_OBI_1000M_NOM_LON.hdf'
        pixel_desert_mask = 'NULL' #add on 2016.10.8
    elif resolution ==500:
        Latfile = '/FY4COMM/FY4A/COM/AHI8_OBI_500M_NOM_LAT.HDF'
        Lonfile = '/FY4COMM/FY4A/COM/AHI8_OBI_500M_NOM_LON.HDF'
        pixel_desert_mask = 'NULL' #add on 2016.10.8
    LNDfile = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_LND_'+str(resolution)+'M.HDF'
    LMKfile = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_LMK_'+str(resolution)+'M.HDF'
    DEMfile = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_DEM_'+str(resolution)+'M.HDF'
    COASTfile = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_COAST_'+str(resolution)+'M.HDF'
    SATZENfile = '/FY4COMM/FY4A/COM/AHI8_OBI_'+str(resolution)+'M_NOM_SATZEN.HDF'
    SATAZIfile = '/FY4COMM/FY4A/COM/AHI8_OBI_'+str(resolution)+'M_NOM_SATAZI.HDF'
   
    SOLARZENfile = 'NULL'  #add on 2016.9.30
    SOLARZIfile = 'NULL' #add on 2016.9.30
   

    provider.SetLonLatFile(Latfile,Lonfile)
    provider.SetAuxiliaryDataFile(LNDfile,LMKfile,DEMfile,COASTfile,SATZENfile,SATAZIfile,Lonfile,Latfile,SOLARZENfile,SOLARZIfile,pixel_desert_mask)

    return  provider

def CreateStdProjProvider(resolution):
    provider = H8Dataprovider()

    Latfile =paramFilePath+ 'AHI8_OBI_2000M_NOM_LATLON.HDF'
    Lonfile = paramFilePath+ 'AHI8_OBI_2000M_NOM_LATLON.HDF'
    L1file = L1FilePath+'AHI8_OBI_2000M_NOM_' + Projstring + '.hdf'
    InverRefFile = L1FilePath+'LATLON_TO_PIXLINE_2000'+'.HDF'

    if resolution == 1000:
        Latfile = paramFilePath+'AHI8_OBI_1000M_NOM_LAT.hdf'
        Lonfile = paramFilePath+'AHI8_OBI_1000M_NOM_LON.hdf'
        L1file = L1FilePath+'AHI8_OBI_1000M_NOM_' +Projstring + '.hdf'
        InverRefFile = L1FilePath+'LATLON_TO_PIXLINE_1000'+'.HDF'

    elif resolution == 500:
        Latfile = paramFilePath+'AHI8_OBI_500M_NOM_LAT.HDF'
        Lonfile = paramFilePath+'AHI8_OBI_500M_NOM_LON.HDF'
        L1file = L1FilePath+'AHI8_OBI_0500M_NOM_' + Projstring + '.hdf'
        InverRefFile = L1FilePath+'LATLON_TO_PIXLINE_0500'+'.HDF'

    provider.SetLonLatFile(Latfile,
                           Lonfile,InverRefFile)

    print Projstring
    provider.SetL1File(L1file)
    provider.SetDataDescription('Himawari8_OBI_'+Projstring)

    # if resolution == 2000:
    #     provider.SetAuxiliaryDataFile('NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL',L1file,L1file, 'NULL')
    return  provider

def ProcessProj(param,reslution,isCreateAuxfile):

    provider = ProviderFactory(isCreateAuxfile,reslution)

    dataouter = HdfDataOuter()

    processor = ProjProcessor(provider, dataouter, param)
    processor.PerformProj()
    processor.Dispose()

def ProcessAuxProj(resolution):
    paramparser = ParameterParser()
    auxparam = paramparser.parseXML(sys.argv[2])
    auxparam.OutputPath = '/FY4COMM/FY4A/COM/PRJ/'
    auxparam.ProjectResolution = resolution
    auxparam.IsAuxiliaryFileMode = True
    ProcessProj(auxparam, resolution, True)

if __name__ == '__main__':

    
    paramparser = ParameterParser()
    # param = paramparser.parseXML('E:/Data/Vmware Win7/Project/ProjectTransform/H8_1000m_Proj.xml')
    # param.OutputPath = 'E:/Data/Vmware Win7/proj/'
    param = paramparser.parseXML('z:/Project/ProjectTransform/H8_1000m_Proj.xml')
    param.OutputPath = 'z:/proj/'

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
    Projstring = '20180829_0310'
    L1FilePath = 'z:/proj/'
    # L1FilePath = 'E:/Data/Vmware Win7/proj/'
    paramFilePath = L1FilePath
    ProcessProj(param, 1000,False)
    # auxfile = '/FY4COMM/FY4A/COM/PRJ/'+ param.GetParamDescription() + '_'+sys.argv[3]+'_'+param.ProjectTaskName+'.HDF'
    # if os.path.exists(auxfile) == False:
    #     ProcessAuxProj(int(sys.argv[3]))

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
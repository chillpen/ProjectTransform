import sys

AuxiliaryDataDict = dict()
AuxiliaryNameDict = dict()

resolution = sys.argv[3]

#def SetLatLon(AuxiliaryDataDICT,Resolution):
#    AuxiliaryDataDICT['Latitude'] = '/FY4COMM/FY4A/COM/AHI8_OBI_'+Resolution+'M_NOM_LAT.hdf'
#    AuxiliaryDataDICT['Longitude'] = '/FY4COMM/FY4A/COM/AHI8_OBI_'+Resolution+'M_NOM_LON.hdf'
    		
def SetNameAndPath(AuxiliaryNameDICT, AuxiliaryDataDICT, Resolution):
    
    #AuxiliaryNameDICT['SensorZenith'] = 'pixel_satellite_zenith_angle'
    #AuxiliaryNameDICT['SensorAzimuth'] = 'pixel_satellite_azimuth_angle'
    AuxiliaryNameDICT['pixel_desert_mask'] = 'pixel_desert_mask'
    AuxiliaryNameDICT['pixel_ecosystem_type'] = 'pixel_ecosystem_type'
    AuxiliaryNameDICT['pixel_snow_mask'] = 'pixel_snow_mask'
    AuxiliaryNameDICT['pixel_surface_elevation'] = 'pixel_surface_elevation'
    AuxiliaryNameDICT['pixel_surface_type'] = 'pixel_surface_type'
    AuxiliaryNameDICT['pixel_volcano_mask'] = 'pixel_volcano_mask'
    AuxiliaryNameDICT['pixel_land_mask'] = 'pixel_land_mask'
    AuxiliaryNameDICT['pixel_coast_mask'] = 'pixel_coast_mask'    
    
    FilePath = '/FY4COMM/FY4A/PAR/AGRIX/ancillary_data/navigation/fygatNAV.Himawari08.xxxxxxx.'+Resolution+'m.hdf'
    #AuxiliaryDataDICT['SensorZenith'] = FilePath 
    #AuxiliaryDataDICT['SensorAzimuth'] = FilePath 
    AuxiliaryDataDICT['pixel_desert_mask'] = FilePath
    AuxiliaryDataDICT['pixel_ecosystem_type'] = FilePath
    AuxiliaryDataDICT['pixel_snow_mask'] = FilePath 
    AuxiliaryDataDICT['pixel_surface_elevation'] = FilePath 
    AuxiliaryDataDICT['pixel_surface_type'] = FilePath
    AuxiliaryDataDICT['pixel_volcano_mask'] = FilePath
    AuxiliaryDataDICT['pixel_land_mask'] =  FilePath
    AuxiliaryDataDICT['pixel_coast_mask'] = FilePath
    

AuxiliaryNameDict['Latitude'] = 'Lat'
AuxiliaryNameDict['Longitude'] = 'Lon'

if resolution == '2000':
    print(2000)
    #LatitudeFilePath = AuxiliaryDataDict['Latitude'] = '/FY4COMM/FY4A/COM/fygatNAV.Himawari08.xxxxxxx.000001(2000).hdf'
    #LongitudeFilePath = AuxiliaryDataDict['Longitude'] =  '/FY4COMM/FY4A/COM/fygatNAV.Himawari08.xxxxxxx.000002(2000).hdf' 
    #AuxiliaryDataDict['Latitude'] = '/FY4COMM/FY4A/COM/fygatNAV.Himawari08.xxxxxxx.000001(2000).hdf'
    #AuxiliaryDataDict['Longitude'] =  '/FY4COMM/FY4A/COM/fygatNAV.Himawari08.xxxxxxx.000002(2000).hdf' 
    AuxiliaryDataDict['Latitude'] = '/FY4COMM/FY4A/COM/AHI8_OBI_2000M_NOM_LATLON.HDF'
    AuxiliaryDataDict['Longitude'] =  '/FY4COMM/FY4A/COM/AHI8_OBI_2000M_NOM_LATLON.HDF' 
   
    AuxiliaryNameDict['SensorZenith'] = 'SatZenith'
    AuxiliaryDataDict['SensorZenith'] = '/FY4COMM/FY4A/COM/AHI8_OBI_'+str(resolution)+'M_NOM_SATZEN.HDF'#2017_2_24

    AuxiliaryNameDict['SensorAzimuth'] = 'SatAzimuth'
    AuxiliaryDataDict['SensorAzimuth'] = '/FY4COMM/FY4A/COM/AHI8_OBI_'+str(resolution)+'M_NOM_SATAZI.HDF'#2017_2_24
    
    SetNameAndPath(AuxiliaryNameDict, AuxiliaryDataDict, resolution)    
    
    AuxiliaryNameDict['LandCover'] = 'LandCover'
    AuxiliaryDataDict['LandCover'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_LND_'+str(resolution)+'M.HDF'

    AuxiliaryNameDict['LandSeaMask'] = 'LandSeaMask'
    AuxiliaryDataDict['LandSeaMask'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_LMK_'+str(resolution)+'M.HDF'

    AuxiliaryNameDict['DEM'] = 'DEM'
    AuxiliaryDataDict['DEM'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_DEM_'+str(resolution)+'M.HDF'

    AuxiliaryNameDict['SeaCoast'] = 'SeaCoast'
    AuxiliaryDataDict['SeaCoast'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_COAST_'+str(resolution)+'M.HDF'
elif resolution == '4000':				#2016_10_21
    print(4000)
    #AuxiliaryDataDict['Latitude'] = AuxiliaryDataDict['Longitude'] = '/FY4COMM/FY4A/COM/AHI8_OBI_4000M_NOM_LATLON.HDF'
    #SetNameAndPath(AuxiliaryNameDict, AuxiliaryDataDict, resolution)
    
    #AuxiliaryNameDict['SensorZenith'] = 'SatZenith'
    #AuxiliaryDataDict['SensorZenith'] = '/FY4COMM/FY4A/COM/AHI8_OBI_'+str(resolution)+'M_NOM_SATZEN.HDF'#2017_2_24

    #AuxiliaryNameDict['SensorAzimuth'] = 'SatAzimuth'
    #AuxiliaryDataDict['SensorAzimuth'] = '/FY4COMM/FY4A/COM/AHI8_OBI_'+str(resolution)+'M_NOM_SATAZI.HDF'#2017_2_24
    
    AuxiliaryDataDict['Latitude'] = AuxiliaryDataDict['Longitude'] = '/FY4COMM/FY4A/COM/AHI8_OBI_2000M_NOM_LATLON.HDF'
    #SetNameAndPath(AuxiliaryNameDict, AuxiliaryDataDict, resolution)
    SetNameAndPath(AuxiliaryNameDict, AuxiliaryDataDict, '2000')
    
    AuxiliaryNameDict['SensorZenith'] = 'SatZenith'
    AuxiliaryDataDict['SensorZenith'] = '/FY4COMM/FY4A/COM/AHI8_OBI_2000M_NOM_SATZEN.HDF'#2017_2_24

    AuxiliaryNameDict['SensorAzimuth'] = 'SatAzimuth'
    AuxiliaryDataDict['SensorAzimuth'] = '/FY4COMM/FY4A/COM/AHI8_OBI_2000M_NOM_SATAZI.HDF'#2017_2_24
    
    AuxiliaryNameDict['LandCover'] = 'LandCover'
    AuxiliaryDataDict['LandCover'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_LND_'+'2000'+'M.HDF'

    AuxiliaryNameDict['LandSeaMask'] = 'LandSeaMask'
    AuxiliaryDataDict['LandSeaMask'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_LMK_'+'2000'+'M.HDF'

    AuxiliaryNameDict['DEM'] = 'DEM'
    AuxiliaryDataDict['DEM'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_DEM_'+'2000'+'M.HDF'

    AuxiliaryNameDict['SeaCoast'] = 'SeaCoast'
    AuxiliaryDataDict['SeaCoast'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_COAST_'+'2000'+'M.HDF'
elif resolution == '8000':				
    print(8000)
    #AuxiliaryDataDict['Latitude'] = AuxiliaryDataDict['Longitude'] = '/FY4COMM/FY4A/COM/AHI8_OBI_8000M_NOM_LATLON.HDF'
    #AuxiliaryDataDict['Latitude'] = AuxiliaryDataDict['Longitude'] = '/FY4COMM/FY4A/COM/AHI8_OBI_8000M_NOM_LATLON.HDF'
    AuxiliaryDataDict['Latitude'] = AuxiliaryDataDict['Longitude'] = '/FY4COMM/FY4A/COM/AHI8_OBI_2000M_NOM_LATLON.HDF'
    #SetNameAndPath(AuxiliaryNameDict, AuxiliaryDataDict, resolution)
    SetNameAndPath(AuxiliaryNameDict, AuxiliaryDataDict, '2000')
    
    AuxiliaryNameDict['SensorZenith'] = 'SatZenith'
    AuxiliaryDataDict['SensorZenith'] = '/FY4COMM/FY4A/COM/AHI8_OBI_'+'2000'+'M_NOM_SATZEN.HDF'#2017_2_24
    AuxiliaryNameDict['SensorAzimuth'] = 'SatAzimuth'
    AuxiliaryDataDict['SensorAzimuth'] = '/FY4COMM/FY4A/COM/AHI8_OBI_'+'2000'+'M_NOM_SATAZI.HDF'#2017_2_24
    
    AuxiliaryNameDict['LandCover'] = 'LandCover'
    AuxiliaryDataDict['LandCover'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_LND_'+'2000'+'M.HDF'

    AuxiliaryNameDict['LandSeaMask'] = 'LandSeaMask'
    AuxiliaryDataDict['LandSeaMask'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_LMK_'+'2000'+'M.HDF'

    AuxiliaryNameDict['DEM'] = 'DEM'
    AuxiliaryDataDict['DEM'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_DEM_'+'2000'+'M.HDF'

    AuxiliaryNameDict['SeaCoast'] = 'SeaCoast'
    AuxiliaryDataDict['SeaCoast'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_COAST_'+'2000'+'M.HDF'
elif resolution == '1000':
    print(1000)
    AuxiliaryDataDict['Latitude'] = '/FY4COMM/FY4A/COM/AHI8_OBI_1000M_NOM_LAT.hdf'
    AuxiliaryDataDict['Longitude'] = '/FY4COMM/FY4A/COM/AHI8_OBI_1000M_NOM_LON.hdf'

    AuxiliaryNameDict['SensorZenith'] = 'SatZenith'
    AuxiliaryDataDict['SensorZenith'] = '/FY4COMM/FY4A/COM/AHI8_OBI_'+str(resolution)+'M_NOM_SATZEN.HDF'#2016_10_13

    AuxiliaryNameDict['SensorAzimuth'] = 'SatAzimuth'
    AuxiliaryDataDict['SensorAzimuth'] = '/FY4COMM/FY4A/COM/AHI8_OBI_'+str(resolution)+'M_NOM_SATAZI.HDF'#2016_10_13
    
    AuxiliaryNameDict['LandCover'] = 'LandCover'
    AuxiliaryDataDict['LandCover'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_LND_'+str(resolution)+'M.HDF'

    AuxiliaryNameDict['LandSeaMask'] = 'LandSeaMask'
    AuxiliaryDataDict['LandSeaMask'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_LMK_'+str(resolution)+'M.HDF'

    AuxiliaryNameDict['DEM'] = 'DEM'
    AuxiliaryDataDict['DEM'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_DEM_'+str(resolution)+'M.HDF'

    AuxiliaryNameDict['SeaCoast'] = 'SeaCoast'
    AuxiliaryDataDict['SeaCoast'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_COAST_'+str(resolution)+'M.HDF'

elif resolution == '500':
    print(500)
    AuxiliaryDataDict['Latitude'] = '/FY4COMM/FY4A/COM/AHI8_OBI_500M_NOM_LAT.HDF'
    AuxiliaryDataDict['Longitude'] = '/FY4COMM/FY4A/COM/AHI8_OBI_500M_NOM_LON.HDF'
       
    AuxiliaryNameDict['SensorZenith'] = 'SatZenith'
    AuxiliaryDataDict['SensorZenith'] = '/FY4COMM/FY4A/COM/AHI8_OBI_'+str(resolution)+'M_NOM_SATZEN.HDF'

    AuxiliaryNameDict['SensorAzimuth'] = 'SatAzimuth'
    AuxiliaryDataDict['SensorAzimuth'] = '/FY4COMM/FY4A/COM/AHI8_OBI_'+str(resolution)+'M_NOM_SATAZI.HDF'

    AuxiliaryNameDict['LandCover'] = 'LandCover'
    AuxiliaryDataDict['LandCover'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_LND_'+str(resolution)+'M.HDF'

    AuxiliaryNameDict['LandSeaMask'] = 'LandSeaMask'
    AuxiliaryDataDict['LandSeaMask'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_LMK_'+str(resolution)+'M.HDF'

    AuxiliaryNameDict['DEM'] = 'DEM'
    AuxiliaryDataDict['DEM'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_DEM_'+str(resolution)+'M.HDF'

    AuxiliaryNameDict['SeaCoast'] = 'SeaCoast'
    AuxiliaryDataDict['SeaCoast'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_COAST_'+str(resolution)+'M.HDF'


		
		

     

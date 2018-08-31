from DataOuter.HdfDataOuter import *
from DataProvider.HiresSatProvider import *
from ProjProcessor import *
from ParameterParser import *
import numpy as N

if __name__ == '__main__':

    # test = 1
    param = ProjParameters()
    # param.ProjRange = ProjRange(24, 29, 116,123)
    # param.ProjRange = ProjRange(26, 27, 118,119)
    param.DstProj = Proj(proj='latlong', datum='WGS84', lon_0=145)
    param.ProjectTaskName = 'PRJ'
    param.BandWaveLengthList = '0'
    param.ProjectResolution = 50

    param.OutputPath = sys.argv[2]

    provider = HiresSatProvider()
    provider.SetL1File(sys.argv[1])
    lat = provider.GetLatitude()
    lon = provider.GetLongitude()
    minlat = N.min(lat)
    maxlat = N.max(lat)
    minlon = N.min(lon)
    maxlon = N.max(lon)
    param.ProjRange=ProjRange((minlat),(maxlat), (minlon), (maxlon))
    dataouter = HdfDataOuter()

    processor = ProjProcessor(provider, dataouter, param)
    processor.PerformProj()
    processor.Dispose()

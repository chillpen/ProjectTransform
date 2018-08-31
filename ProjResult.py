import numpy as N
import ProjOutputData_module as SD
import h5py
import gc
class ProjResult(object):


    def __init__(self):
        super(ProjResult,self).__init__()
        self.U = None
        self.V = None

        self.ResultInfo = None

        self.LatLonRangeMask = None

        self.NeedUpdate = True

        self.__DstProj = None

        self.__Width = 0
        self.__Height = 0
        self.__tv = None
        self.__tu = None
        self.__DataSearchTable = None
        self.__IslatlongProj = False

        self.MaxU = None
        self.MinU = None
        self.MaxV = None
        self.MinV = None
        self.__latlonResRate = float(0.01) / float(1000)

        self.InverseCal = False
        self.__InverRefPix = None
        self.__InverRefLine = None
        self.__InversRefX = None
        self.__InversRefY = None
        self.__LeftLon = None
        self.__TopLat = None
        self.__RefWidth = None
        return

    def SetDstProj(self,dstProj):
        self.__DstProj = dstProj
        if ('latlong' in dstProj.srs)  :
            self.__IslatlongProj = True
       

    def SetInversRef(self,refline,refpix,leftLon,topLat,refWidth):
        self.__InverRefPix = refpix
        self.__InverRefLine = refline
        self.__LeftLon = leftLon
        self.__TopLat = topLat
        self.__RefWidth = refWidth

    def Dispose(self):

       del self.U

       del self.V

       del self.ResultInfo

       del self.LatLonRangeMask

       del self.__DataSearchTable
    #    del self.__InverRefPix
    #    del self.__InverRefLine



    # def CalProjectMinMax(self, U, V):
    #
    #     maskU = (U < 999999999)
    #     maskV = (V < 999999999)
    #
    #     RealU = U[maskU]
    #     RealV = V[maskV]
    #     self.MinU = N.min(RealU[:]).astype(N.float32)
    #     self.MinV = N.min(RealV[:]).astype(N.float32)
    #     self.MaxU = N.max(RealU[:]).astype(N.float32)
    #     self.MaxV = N.max(RealV[:]).astype(N.float32)
    #     return self.MinU, self.MinV, self.MaxU, self.MaxV

    # def CalProjectMinMax(self,projRange):

    # def CalCenterUV(self,U,V):
    #     self.CalProjectMinMax(U,V)
    #     centU = (self.MaxU-self.MinU)/2+self.MinU
    #     centV = (self.MaxV-self.MinV)/2+self.MinV
    #     return  centU,centV


    def CalProjectWidthAndHeight(self,minU,minV,maxU,maxV,resolution):

        Height = round((maxV- minV) / resolution+ 0.5)
        Width = round((maxU- minU) / resolution+ 0.5)



        return Height,Width

    def CalUVToIJ(self,resolution,U,V,minU,minV):
        tu = []
        tv = []
        if self.InverseCal == False:
            resolutionFactor = float(1)/float(resolution)
            ru = U*resolutionFactor
            rv = V*resolutionFactor
            minUF = minU*resolutionFactor
            minVF = minV*resolutionFactor
            tu = (ru-minUF).astype(N.int32)#(ru-minUF+0.5).astype(N.int32)is wrong,because  max(tv)==height, actully max(tv)==height-1 otherwise cause trubble in CreateData.c
            tv = (rv-minVF).astype(N.int32)
            del ru
            del rv
            gc.collect()

        else:
            ru = N.linspace( self.MinU, self.MaxU, self.__Width )
            tu = ((ru-self.__LeftLon )/resolution+0.5).astype(N.int32)
            rv = N.linspace(self.MaxV,self.MinV,self.__Height)
            tv = ((self.__TopLat-rv)/resolution+0.5).astype(N.int32)
            
            # ru = N.linspace( self.MinU, self.MaxU, self.__Width )
            # tu = (([143.36359,138.60704]-self.__LeftLon )/resolution+0.5).astype(N.int32)
            # rv = N.linspace(self.MaxV,self.MinV,self.__Height)
            # tv = ((self.__TopLat-[23.166971,34.927864])/resolution+0.5).astype(N.int32)
            
            
            del ru
            del rv
            gc.collect()

        return  tu,tv

    def CreateSaveData(self, refdata,resolution,datatype,datasetName):

        # if self.MaxU > 180: #if is'latlong proj' and longitude is out of range
        #   print self.V,self.U,self.MaxV,self.MinV,self.MaxU,self.MinU
        #   self.LatLonRangeMask = (self.V[:,:]<= self.MaxV) & (self.V[:,:]>= self.MinV) & \
        #               (self.U[:,:]<= self.MaxU) & (self.U[:,:]>= self.MinU)

        res = resolution
        if self.__IslatlongProj:
            res = self.__latlonResRate*resolution

        if self.NeedUpdate:
            # if self.MaxU == None:
            #     self.CalProjectMinMax(self.U[(self.LatLonRangeMask)], self.V[(self.LatLonRangeMask)])
            self.__Height, self.__Width = self.CalProjectWidthAndHeight( self.MinU, self.MinV, self.MaxU, self.MaxV,res)
            # pix = self.__InverRefPix
            if self.InverseCal == False:
                self.__tu, self.__tv = self.CalUVToIJ(res,self.U,self.V,self.MinU,self.MinV)
                self.__DataSearchTable = SD.CreateOutputSearTable(int(self.__Width ), int(self.__Height), self.__tu[(self.LatLonRangeMask)], self.__tv[(self.LatLonRangeMask)])
            else:
                self.__tu, self.__tv = self.CalUVToIJ(res,self.U,self.V,self.MinU,self.MinV)
                reftab = N.zeros((len(self.__tv),len(self.__tu)))
                # reftab = reftab+self.__tu
                reftab += self.__tu
                # temp = self.__tv
                # temp.shape=(1,len(self.__tv))
                self.__tv.shape = (1,len(self.__tv))
                temp = N.transpose(self.__tv)
                del self.__tu
                del self.__tv
                gc.collect()

                index = ((reftab+temp*self.__RefWidth).astype(N.int32)).ravel()
                del reftab
                del temp
                gc.collect()

                self.__InversRefX = (self.__InverRefPix.ravel())[index]
                self.__InversRefY = (self.__InverRefLine.ravel())[index]
 
                x = self.__InversRefX
                y = self.__InversRefY
                del self.__InverRefPix
                del self.__InverRefLine

                del index
                gc.collect()
                # self.__DataSearchTable = x+y*11000
                # width = int(self.__Width )
                # dt = self.__DataSearchTable
                # reftab = reftab+self.__tv*16200
                # test = 1
                
                # self.__DataSearchTable = SD.CreateOutputSearTable(int(self.__Width ), int(self.__Height), ti, ti,self.InverseCal)
            #file = h5py.File("/FY4COMM/FY4A/COM/PRJ/test/searchtable.HDF")
            #file.create_dataset("self.__DataSearchTable",data = self.__DataSearchTable)
            #file.close()
            self.NeedUpdate = False
        
        if self.__IslatlongProj and ("ongitude" in datasetName):
            saveData = N.linspace(self.MinU,self.MaxU,int(self.__Width))
            saveData = N.tile(saveData,int(self.__Height))
            saveData = saveData.reshape(int(self.__Height),int(self.__Width)).astype('f4')
            if self.MaxU > 180:
              saveData[saveData > 180] -= 360
              saveData[saveData < -180] += 360         
        elif self.__IslatlongProj and "atitude" in datasetName:
            saveData = N.linspace(self.MaxV,self.MinV,self.__Height)
            saveData = N.tile(saveData,int(self.__Width))
            saveData = saveData.reshape(int(self.__Width),int(self.__Height)).astype('f4')
            saveData = saveData.T
            
        else:
            #print "@@@@@@@@@@@@@@@@@@"
            #print refdata
            #print refdata[refdata<65534]
            if self.InverseCal == False: 
                data = refdata[(self.LatLonRangeMask)]//20180829
                saveData  = SD.CreateOutputData(int(self.__Width ), int(self.__Height),datatype,self.__DataSearchTable,data)
                del data
                gc.collect()
            else:
                # data = refdata
                # st = self.__InversRefX
                saveData  = SD.CreateOutputDataInversRef(int(self.__Width ), int(self.__Height),int(refdata.shape[1]), datatype,self.__InversRefX.astype(N.int32),self.__InversRefY.astype(N.int32),refdata)
            # st = self.__DataSearchTable
          
            
        if (type(saveData[0,0]) is N.float32):
        	FillValue = 65535
        	self.FourCorner(saveData,FillValue)
        if (type(saveData[0,0]) is N.int32):
        	FillValue = 65535
        	self.FourCorner(saveData,FillValue)
        elif type(saveData[0,0]) is N.int16:
          FillValue = 32767
          self.FourCorner(saveData,FillValue)
        elif type(saveData[0,0]) is N.int8:
          FillValue = 127
          self.FourCorner(saveData,FillValue)
        elif type(saveData[0,0]) is N.uint8:
          FillValue = 255
          self.FourCorner(saveData,FillValue)
         
        return saveData
        
    def FourCorner(self,saveData,FillValue):
    	    #left up
          if saveData[0,0] == FillValue and saveData[0,1] != FillValue:
             saveData[0,0] = saveData[0,1]
          elif saveData[0,0] == FillValue and saveData[1,0] != FillValue:
             saveData[0,0] = saveData[1,0]
          elif saveData[0,0] == FillValue and saveData[1,1] != FillValue:
             saveData[0,0] = saveData[1,1]
          #left down
          if saveData[int(self.__Height-1),0] == FillValue and saveData[int(self.__Height-1),1] != FillValue:
             saveData[int(self.__Height-1),0] = saveData[int(self.__Height-1),1]
          elif saveData[int(self.__Height-1),0] == FillValue and saveData[int(self.__Height-1-1),0] != FillValue:
             saveData[int(self.__Height-1),0] = saveData[int(self.__Height-1-1),0]
          elif saveData[int(self.__Height-1),0] == FillValue and saveData[int(self.__Height-1-1),1] != FillValue:
             saveData[int(self.__Height-1),0] = saveData[int(self.__Height-1-1),1]
          #right up
          if saveData[0,int(self.__Width-1)] == FillValue and saveData[1,int(self.__Width-1)] != FillValue:
             saveData[0,int(self.__Width-1)] = saveData[1,int(self.__Width-1)]
          elif saveData[0,int(self.__Width-1)] == FillValue and saveData[0,int(self.__Width-1-1)] != FillValue:
             saveData[0,int(self.__Width-1)] = saveData[0,int(self.__Width-1-1)]
          elif saveData[0,int(self.__Width-1)] == FillValue and saveData[1,int(self.__Width-1-1)] != FillValue:
             saveData[0,int(self.__Width-1)] = saveData[1,int(self.__Width-1-1)] 
          #right down
          if saveData[int(self.__Height-1),int(self.__Width-1)] == FillValue and saveData[int(self.__Height-1-1),int(self.__Width-1)] != FillValue:
             saveData[int(self.__Height-1),int(self.__Width-1)] = saveData[int(self.__Height-1-1),int(self.__Width-1)]
          elif saveData[int(self.__Height-1),int(self.__Width-1)] == FillValue and saveData[int(self.__Height-1),int(self.__Width-1-1)] != FillValue:
             saveData[int(self.__Height-1),int(self.__Width-1)] = saveData[int(self.__Height-1),int(self.__Width-1-1)]
          elif saveData[int(self.__Height-1),int(self.__Width-1)] == FillValue and saveData[int(self.__Height-1-1),int(self.__Width-1-1)] != FillValue:
             saveData[int(self.__Height-1),int(self.__Width-1)] = saveData[int(self.__Height-1-1),int(self.__Width-1-1)]
          
          return
    '''
    def CreateLatLonData(self, datasetName,resolution):
                
        res = resolution
        if self.__IslatlongProj:
            res = self.__latlonResRate*resolution

        if self.NeedUpdate:
            # if self.MaxU == None:
            #     self.CalProjectMinMax(self.U[(self.LatLonRangeMask)], self.V[(self.LatLonRangeMask)])
            self.__Height, self.__Width = self.CalProjectWidthAndHeight( self.MinU, self.MinV, self.MaxU, self.MaxV,res)
            self.__tu, self.__tv = self.CalUVToIJ(res,self.U,self.V,self.MinU,self.MinV)
            self.__DataSearchTable = SD.CreateOutputSearTable(int(self.__Width ), int(self.__Height), self.__tu[(self.LatLonRangeMask)], self.__tv[(self.LatLonRangeMask)])
            self.NeedUpdate = False
        # U longitude    V latitude   
        if "ongitude" in datasetName:   
            saveData = N.linspace(self.MinU,self.MaxU,int(self.__Width))
            saveData = N.tile(saveData,int(self.__Height))
            saveData = saveData.reshape(int(self.__Height),int(self.__Width)).astype('f4')
            if self.MaxU > 180:
              saveData[saveData > 180] -= 360
              saveData[saveData < -180] + 360         
        elif "atitude" in datasetName:
            saveData = N.linspace(self.MaxV,self.MinV,self.__Height)
            saveData = N.tile(saveData,int(self.__Width))
            saveData = saveData.reshape(int(self.__Width),int(self.__Height)).astype('f4')
            saveData = saveData.T

        return saveData
    '''
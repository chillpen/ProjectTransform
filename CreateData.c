/*  Example of wrapping the cos function from math.h using the Numpy-C-API. */

#include <Python.h>
#include <numpy/arrayobject.h>
#include <math.h>
#include <stdint.h>

/*  wrapped cosine function */
static PyObject* CreateOutputSearTable(PyObject* self, PyObject* args)
{

    int width;
    int height;
    PyArrayObject *in_array_tu;
    PyArrayObject *in_array_tv;
    PyArrayObject *in_array_refdata;


    /*  parse single numpy array argument */
    if (!PyArg_ParseTuple(args, "iiO!O!",&width,&height, &PyArray_Type, &in_array_tu, &PyArray_Type, &in_array_tv))
        return NULL;

      PyArrayIterObject *tu_iter = (PyArrayIterObject *)PyArray_IterNew((PyObject*)in_array_tu);
      PyArrayIterObject *tv_iter = (PyArrayIterObject* )PyArray_IterNew((PyObject*)in_array_tv);

    npy_intp dims[2] = {height,width};

    PyObject *savedata = PyArray_SimpleNew(2, dims, NPY_INT32);

    PyArrayIterObject *save_iter;
    save_iter = (PyArrayIterObject *)PyArray_IterNew(savedata);

    int index = 0;
    int count = width*height;


    int *OD = malloc(sizeof(int)*count);

    for(index = 0;index<count;index++)
    {
          
           //*(OD+index) = 65535;
           *(OD+index) = -1; //2016_12_27
    }

    int i =0;

    for( i =0 ;i < tu_iter->size;i++)
     {

            int * tudataptr = (int *)tu_iter->dataptr;
            int * tvdataptr = (int *)tv_iter->dataptr;

            int index  =  (height-(*tvdataptr)-1) * width+*(tudataptr);

            *(OD+index) = i;


            PyArray_ITER_NEXT(tu_iter);
            PyArray_ITER_NEXT(tv_iter);

     }

    //CFill_Gap_By_NeighbourPoint(OD,width,height,8,65535); 
    CFill_Gap_By_NeighbourPoint(OD,width,height,8,-1);
//    CFill_Gap_By_InterpolatingAlongX(OD,width,height, 0 , 65535, 0);

    for(index = 0;index<count;index++)
    {
           int * out_savedataptr = (int *)save_iter->dataptr;
           *(out_savedataptr) = *(OD+index);
           PyArray_ITER_NEXT(save_iter);
    }

    free(OD);
    /*  clean up and return the result */
//    Py_DECREF(in_array_tu);
//    Py_DECREF(in_array_tv);
    Py_DECREF(tv_iter);
    Py_DECREF(tu_iter);
//    Py_DECREF(in_array_refdata);
    Py_DECREF(save_iter);
    Py_INCREF(savedata);
    return savedata;

    /*  in case bad things happen */
    fail:

        Py_XDECREF(tv_iter);
        Py_XDECREF(tu_iter);
    //    Py_DECREF(in_array_refdata);
        Py_XDECREF(save_iter);
        Py_XDECREF(savedata);
        return NULL;
}


/*  wrapped cosine function */
static PyObject* CreateOutputDataInversRef(PyObject* self, PyObject* args)
{

    
    int width;
    int height;
    int datatype;
	int refwidth;
    PyArrayObject *in_array_SearchTableX;
	PyArrayObject *in_array_SearchTableY;

    PyArrayObject *in_array_refdata;


    /*  parse single numpy array argument */
    if (!PyArg_ParseTuple(args, "iiiiO!O!O!",&width,&height,&refwidth, &datatype,&PyArray_Type, &in_array_SearchTableX,&PyArray_Type, &in_array_SearchTableY,
     &PyArray_Type, &in_array_refdata))
        return NULL;

      PyArrayIterObject *Tabel_iterX = (PyArrayIterObject *)PyArray_IterNew((PyObject*)in_array_SearchTableX);
	  PyArrayIterObject *Tabel_iterY = (PyArrayIterObject *)PyArray_IterNew((PyObject*)in_array_SearchTableY);

      PyArrayIterObject *ref_iter = (PyArrayIterObject *)PyArray_IterNew((PyObject*)in_array_refdata);


    npy_intp dims[2] = {height,width};

    PyObject *savedata ;
    if (datatype == 0)
        savedata= PyArray_SimpleNew(2, dims, NPY_INT32);  
    else if(datatype == 80)                              //ADD ON 2016/10/9
        savedata= PyArray_SimpleNew(2, dims, NPY_UINT8); //ADD ON 2016/10/9	 
    else if(datatype == 81)                              //ADD ON 2016/10/9
        savedata= PyArray_SimpleNew(2, dims, NPY_INT8);  //ADD ON 2016/10/9
    else if(datatype == 16)                              //ADD ON 2016/10/9
        savedata= PyArray_SimpleNew(2, dims, NPY_INT16); //ADD ON 2016/10/9       
    else
        savedata= PyArray_SimpleNew(2, dims, NPY_FLOAT32);
    PyArrayIterObject *save_iter;
    save_iter = (PyArrayIterObject *)PyArray_IterNew(savedata);

    int count = height*width;

    int i =0;
	printf("beging create savedata  ");
    for( i =0 ;i < count;i++)
     {
        int * tabledataptrX = (int *)Tabel_iterX->dataptr;
		int * tabledataptrY = (int *)Tabel_iterY->dataptr;
        // printf("X and Y is %i\n" , *(tabledataptrX));
        if(* tabledataptrX == -1 || * tabledataptrY == -1  ) //2016_12_27
        {            	            	
	        	if (datatype == 0)
	          {
	              int * savedataptr = (int *)save_iter->dataptr;	                
	              *(savedataptr) = 65535;	           
	          }	            
	          else if(datatype == 80)
	          //if(datatype == 80)
	          {
	              unsigned char * savedataptr = (unsigned char *)save_iter->dataptr;	                
	              *(savedataptr) = 255;
	          }
	          else if(datatype == 81)
	          {
	              char * savedataptr = (char *)save_iter->dataptr;	                
	              *(savedataptr) = 127;
	          }
	          else if(datatype == 16)
	          {
	              short * savedataptr = (short *)save_iter->dataptr;	                
	              *(savedataptr) = 32767;
	          }
	          else
	          {
	              float * savedataptr = (float *)save_iter->dataptr;	                
	              *(savedataptr) = 65535.0;
	          }
        }
        else
        {
          PyArray_ITER_GOTO1D(ref_iter,(*tabledataptrY)*refwidth+*tabledataptrX);
        //   printf("%i\n" , i);
          if (datatype == 0)
          {
              int * savedataptr = (int *)save_iter->dataptr;
              int * refdataptr = (int *)ref_iter->dataptr;
              *(savedataptr) = *(refdataptr);	           
          }
          
          else if(datatype == 80)
          {
              unsigned char * savedataptr = (unsigned char *)save_iter->dataptr;
              unsigned char * refdataptr = (unsigned char *)ref_iter->dataptr;
              *(savedataptr) = *(refdataptr);
          }
          else if(datatype == 81)
          {
              char * savedataptr = (char *)save_iter->dataptr;
              char * refdataptr = (char *)ref_iter->dataptr;
              *(savedataptr) = *(refdataptr);
          }
          else if(datatype == 16)
          {
              short * savedataptr = (short *)save_iter->dataptr;
              short * refdataptr = (short *)ref_iter->dataptr;
              *(savedataptr) = *(refdataptr);
          }
          else
          {
              float * savedataptr = (float *)save_iter->dataptr;
              float * refdataptr = (float *)ref_iter->dataptr;
              *(savedataptr) = *(refdataptr);
          }
        }
       
        PyArray_ITER_NEXT(Tabel_iterX);
		PyArray_ITER_NEXT(Tabel_iterY);
        PyArray_ITER_NEXT(save_iter);        
     }

    /*  clean up and return the result */
//    Py_DECREF(in_array_SearchTable);
//    Py_DECREF(in_array_refdata);
    Py_DECREF(Tabel_iterX);
	 Py_DECREF(Tabel_iterY);
    Py_DECREF(ref_iter);
    Py_DECREF(save_iter);

    Py_INCREF(savedata);


//    return Py_BuildValue("O", savedata);
    return savedata;
    /*  in case bad things happen */
    fail:
        Py_XDECREF(Tabel_iterX);
		Py_XDECREF(Tabel_iterY);
        Py_XDECREF(ref_iter);
        Py_XDECREF(save_iter);

        Py_XDECREF(savedata);
        printf("AH~~~~~~~~~~~~Bad things happen!");
        return NULL;
}

/*  wrapped cosine function */
static PyObject* CreateOutputData(PyObject* self, PyObject* args)
{

//    printf("beging create savedata  ");
    int width;
    int height;
    int datatype;
    PyArrayObject *in_array_SearchTable;

    PyArrayObject *in_array_refdata;


    /*  parse single numpy array argument */
    if (!PyArg_ParseTuple(args, "iiiO!O!",&width,&height, &datatype,&PyArray_Type, &in_array_SearchTable,
     &PyArray_Type, &in_array_refdata))
        return NULL;

      PyArrayIterObject *Tabel_iter = (PyArrayIterObject *)PyArray_IterNew((PyObject*)in_array_SearchTable);

      PyArrayIterObject *ref_iter = (PyArrayIterObject *)PyArray_IterNew((PyObject*)in_array_refdata);


    npy_intp dims[2] = {height,width};

    PyObject *savedata ;
    if (datatype == 0)
        savedata= PyArray_SimpleNew(2, dims, NPY_INT32);  
    else if(datatype == 80)                              //ADD ON 2016/10/9
        savedata= PyArray_SimpleNew(2, dims, NPY_UINT8); //ADD ON 2016/10/9	 
    else if(datatype == 81)                              //ADD ON 2016/10/9
        savedata= PyArray_SimpleNew(2, dims, NPY_INT8);  //ADD ON 2016/10/9
    else if(datatype == 16)                              //ADD ON 2016/10/9
        savedata= PyArray_SimpleNew(2, dims, NPY_INT16); //ADD ON 2016/10/9       
    else
        savedata= PyArray_SimpleNew(2, dims, NPY_FLOAT32);
    PyArrayIterObject *save_iter;
    save_iter = (PyArrayIterObject *)PyArray_IterNew(savedata);

    int count = height*width;

    int i =0;

    for( i =0 ;i < count;i++)
     {
        int * tabledataptr = (int *)Tabel_iter->dataptr;
       
        if(* tabledataptr == -1) //2016_12_27
        {            	            	
	        	if (datatype == 0)
	          {
	              int * savedataptr = (int *)save_iter->dataptr;	                
	              *(savedataptr) = 65535;	           
	          }	            
	          else if(datatype == 80)
	          //if(datatype == 80)
	          {
	              unsigned char * savedataptr = (unsigned char *)save_iter->dataptr;	                
	              *(savedataptr) = 255;
	          }
	          else if(datatype == 81)
	          {
	              char * savedataptr = (char *)save_iter->dataptr;	                
	              *(savedataptr) = 127;
	          }
	          else if(datatype == 16)
	          {
	              short * savedataptr = (short *)save_iter->dataptr;	                
	              *(savedataptr) = 32767;
	          }
	          else
	          {
	              float * savedataptr = (float *)save_iter->dataptr;	                
	              *(savedataptr) = 65535.0;
	          }
        }
        else
        {
          PyArray_ITER_GOTO1D(ref_iter,*tabledataptr);
          
          if (datatype == 0)
          {
              int * savedataptr = (int *)save_iter->dataptr;
              int * refdataptr = (int *)ref_iter->dataptr;
              *(savedataptr) = *(refdataptr);	           
          }
          
          else if(datatype == 80)
          {
              unsigned char * savedataptr = (unsigned char *)save_iter->dataptr;
              unsigned char * refdataptr = (unsigned char *)ref_iter->dataptr;
              *(savedataptr) = *(refdataptr);
          }
          else if(datatype == 81)
          {
              char * savedataptr = (char *)save_iter->dataptr;
              char * refdataptr = (char *)ref_iter->dataptr;
              *(savedataptr) = *(refdataptr);
          }
          else if(datatype == 16)
          {
              short * savedataptr = (short *)save_iter->dataptr;
              short * refdataptr = (short *)ref_iter->dataptr;
              *(savedataptr) = *(refdataptr);
          }
          else
          {
              float * savedataptr = (float *)save_iter->dataptr;
              float * refdataptr = (float *)ref_iter->dataptr;
              *(savedataptr) = *(refdataptr);
          }
        }
       
        PyArray_ITER_NEXT(Tabel_iter);
        PyArray_ITER_NEXT(save_iter);        
     }

    /*  clean up and return the result */
//    Py_DECREF(in_array_SearchTable);
//    Py_DECREF(in_array_refdata);
    Py_DECREF(Tabel_iter);
    Py_DECREF(ref_iter);
    Py_DECREF(save_iter);

    Py_INCREF(savedata);


//    return Py_BuildValue("O", savedata);
    return savedata;
    /*  in case bad things happen */
    fail:
        Py_XDECREF(Tabel_iter);
        Py_XDECREF(ref_iter);
        Py_XDECREF(save_iter);

        Py_XDECREF(savedata);
        printf("AH~~~~~~~~~~~~Bad things happen!");
        return NULL;
}

/*  wrapped H8Calibration function */
static PyObject* CreateH8CalibrationData(PyObject* self, PyObject* args)
{

//    printf("beging create savedata  ");
    int width;
    int height;
    int datatype;
    PyArrayObject *in_array_SearchTable;

    PyArrayObject *in_array_refdata;


    /*  parse single numpy array argument */
    if (!PyArg_ParseTuple(args, "iiiO!O!",&width,&height, &datatype,&PyArray_Type, &in_array_SearchTable,
     &PyArray_Type, &in_array_refdata))
        return NULL;

      PyArrayIterObject *Tabel_iter = (PyArrayIterObject *)PyArray_IterNew((PyObject*)in_array_SearchTable);

      PyArrayIterObject *ref_iter = (PyArrayIterObject *)PyArray_IterNew((PyObject*)in_array_refdata);


    npy_intp dims[2] = {height,width};

    PyObject *savedata ;

    savedata= PyArray_SimpleNew(2, dims, NPY_INT32);

    PyArrayIterObject *save_iter;
    save_iter = (PyArrayIterObject *)PyArray_IterNew(savedata);

    int count = height*width;

    int i =0;

    for( i =0 ;i < count;i++)
     {

        {

            int * refdataptr = (int *)ref_iter->dataptr;

            PyArray_ITER_GOTO1D(Tabel_iter,*refdataptr);
            int factor = 1000;

            if (datatype == 1)
            {
                factor = 100;
            }
             int * savedataptr = (int *)save_iter->dataptr;
             float * tableValue = (float *)Tabel_iter->dataptr;
//                int * refdataptr = ((float *)Tabel_iter->dataptr) ;
             float calValue =(*tableValue);
             if(calValue<65534)
                calValue*=factor;


             *(savedataptr) = (int)calValue;
//            else
//            {
//                float * savedataptr = (float *)save_iter->dataptr;
//                float * refdataptr = (float *)ref_iter->dataptr;
//                *(savedataptr) = *(refdataptr);
//            }

//            printf("%i\n" , calValue);
            PyArray_ITER_NEXT(ref_iter);
            PyArray_ITER_NEXT(save_iter);


        }
     }

    /*  clean up and return the result */
//    Py_DECREF(in_array_SearchTable);
//    Py_DECREF(in_array_refdata);
    Py_DECREF(Tabel_iter);
    Py_DECREF(ref_iter);
    Py_DECREF(save_iter);

    Py_INCREF(savedata);


//    return Py_BuildValue("O", savedata);
    return savedata;
    /*  in case bad things happen */
    fail:
        Py_XDECREF(Tabel_iter);
        Py_XDECREF(ref_iter);
        Py_XDECREF(save_iter);

        Py_XDECREF(savedata);
        printf("AH~~~~~~~~~~~~Bad things happen!");
        return NULL;
}




/*  BilinearInterpolation */
void BilinearInterpolation_SetCtlPoint(float x1, float y1, float x2, float y2,float * m_x1,float * m_y1, float * m_x21,float * m_y21)
{

	  *m_x1 = x1;
	  *m_y1 = y1;
	  *m_x21 = x2 - x1;
	  *m_y21 = y2 - y1;
}
float BilinearInterpolation_Execute(float x, float y,float m_x1,float m_y1, float m_x21,float m_y21,float m_V1,float m_V2, float m_V31,float m_V42)
{
    float temp = (y - m_y1) / m_y21;
    float Va = m_V1 + m_V31 * temp;
    float Vb = m_V2 + m_V42 * temp;
    return (Va + (Vb - Va) * (x - m_x1) / m_x21);
}
void BilinearInterpolation_SetCtlValue(float V1, float V2, float V3, float V4,float * m_V1,float * m_V2, float * m_V31,float * m_V42)
{
    *m_V1 = V1;
    *m_V2 = V2;
    *m_V31 = V3 - V1;
    *m_V42 = V4 - V2;
}
static PyObject* BilinearInterPolateData(PyObject* self, PyObject* args)
{
//printf("------------------BilinearInterpolate Begin------------------\n");


    PyArrayObject *dataOrg;
    int dataOrgRowCount;
    int dataOrgColCount;
    int zoomRate;
    
    float m_V1, m_V2,m_V31, m_V42;
    float m_x1, m_y1,m_x21, m_y21;
    int index_i,index_j,index_m,index_n;
    int rectRes;
    int distZoom;
    int interPolateRowCount,interPolateColCount;
    int offset;
    float v,v1,v2,v3,v4;
    //zoomRate = OriginalResolution/DestResolution
    if (!PyArg_ParseTuple(args, "iiiO!",&dataOrgRowCount,&dataOrgColCount, &zoomRate,&PyArray_Type,  &dataOrg))
    {
    printf("Arguments Wrong!\n");
    return NULL;
    }

    PyArrayIterObject *dataOrg_iter = (PyArrayIterObject *)PyArray_IterNew((PyObject*)dataOrg);
    float* dataOrg_Local = (float *) malloc(sizeof(float)*(dataOrgRowCount * dataOrgColCount));
    //printf("dataOrgRowCount: %d ,dataOrgColCount :%d \n",dataOrgRowCount,dataOrgColCount);
    for(index_i = 0;index_i<dataOrgRowCount * dataOrgColCount;index_i++)
    {
           float * Data_ptr = (float *)dataOrg_iter->dataptr;
           dataOrg_Local[index_i] =*(Data_ptr);
           PyArray_ITER_NEXT(dataOrg_iter);
    }

    interPolateRowCount = (dataOrgRowCount) * zoomRate; ;
    interPolateColCount = (dataOrgColCount) * zoomRate;
    //printf("interPolateRowCount: %d ,interPolateColCount :%d \n",interPolateRowCount,interPolateColCount);
    float* interPolateData = (float *) malloc(sizeof(float)*(interPolateRowCount * interPolateColCount));

    //npy_intp dims = (dataOrgRowCount - 2) * zoomRate * (dataOrgColCount - 2) * zoomRate;
    npy_intp dims = (dataOrgRowCount) * zoomRate * (dataOrgColCount) * zoomRate;
    PyObject *result = PyArray_SimpleNew(1, &dims, NPY_FLOAT);
    PyArrayIterObject *result_iter = (PyArrayIterObject *)PyArray_IterNew(result);

    //����˫���Բ�ֵ��ԭʼ��������֮��ľ��뽫��������þ���ΪdistZoom,����ÿһ�㶼Ϊ��ֵ��õ�Ŵ���
    //���ĵ㣬�����������Ϊ����0.5������������루����zoomrate�����������������ľ��루+1�������Ŵ���Ϊ����
    //�Ų���Ҫ��1
    distZoom = zoomRate;
    if (zoomRate % 2 == 0)
        distZoom = zoomRate + 1;

    //ÿ����ֵ����������Ҫ����ĵ���ķֱ���ΪrectRes��rectRes
    //int rectRes;

    if (zoomRate % 2 == 0)
        rectRes = zoomRate;
    else
        rectRes = (zoomRate + 1);

 //printf("distZoom: %d ,rectRes :%d \n",distZoom,rectRes);

    for ( index_i = 0; index_i < dataOrgRowCount - 1; index_i++)
    {
        for ( index_j = 0; index_j < dataOrgColCount - 1; index_j++)
        {
            BilinearInterpolation_SetCtlPoint(0, 0, distZoom, distZoom, &m_x1, &m_y1, &m_x21, &m_y21);

            v1 = dataOrg_Local[index_i * dataOrgColCount + index_j];
            v2 = dataOrg_Local[index_i * dataOrgColCount + index_j + 1];
            v3 = dataOrg_Local[(index_i + 1) * dataOrgColCount + index_j];
            v4 = dataOrg_Local[(index_i + 1) * dataOrgColCount + index_j + 1];
            BilinearInterpolation_SetCtlValue(v1, v2, v3, v4, &m_V1, &m_V2, &m_V31, &m_V42);


            for (index_m = 0; index_m < rectRes; index_m++)
            {
                for (index_n = 0; index_n < rectRes; index_n++)
                {
                    if (zoomRate % 2 == 0)
                    {
                        v = BilinearInterpolation_Execute(0.5f + index_n, 0.5f + index_m, m_x1, m_y1, m_x21, m_y21, m_V1, m_V2, m_V31, m_V42);

                        offset = (zoomRate / 2 + index_i * rectRes) * interPolateColCount + zoomRate / 2 + index_j * rectRes;


                        interPolateData[offset + index_m * interPolateColCount + index_n] = (float)v;//(Roundound(v));
                    }
                    else
                    {
                        v = BilinearInterpolation_Execute(index_n, index_m, m_x1, m_y1, m_x21, m_y21, m_V1, m_V2, m_V31, m_V42);
                        offset = ((zoomRate - 1) / 2 + index_i * rectRes) * interPolateColCount + (zoomRate - 1) / 2 + index_j * rectRes;

                        interPolateData[offset + index_m * interPolateColCount + index_n] = (float)v;//(Round(v));
                    }
                }
            }

        }
    }
    for (index_i = 0; index_i < interPolateRowCount; index_i++)
    {
        for (index_j = 0; index_j < interPolateColCount; index_j++)
        {
            float * ResultData_ptr = (float *)result_iter->dataptr;
            *(ResultData_ptr) = interPolateData[index_i * interPolateRowCount + index_j];;
            PyArray_ITER_NEXT(result_iter);
        }
    }

    Py_DECREF(dataOrg_iter);
    Py_DECREF(result_iter);

    memset(dataOrg_Local,0,sizeof(dataOrg_Local));
    free(dataOrg_Local);
    memset(interPolateData,0,sizeof(interPolateData));
    free(interPolateData);
    Py_INCREF(result);
    //printf("------------------BilinearInterpolate End------------------\n");
    return result;
}



/*  define functions in module */
static PyMethodDef OutputDataMethods[] =
{
     {"CreateOutputSearTable", CreateOutputSearTable, METH_VARARGS,
         ""},
     {"CreateOutputData", CreateOutputData, METH_VARARGS,
         ""},
	 {"CreateOutputDataInversRef", CreateOutputDataInversRef, METH_VARARGS,
         ""},
     {"CreateH8CalibrationData", CreateH8CalibrationData, METH_VARARGS,
         ""},
     {"BilinearInterPolateData", (PyCFunction)BilinearInterPolateData,METH_VARARGS,
     	NULL},
     {NULL, NULL, 0, NULL}
};

/* module initialization */
PyMODINIT_FUNC

initProjOutputData_module(void)
{
     (void) Py_InitModule("ProjOutputData_module", OutputDataMethods);
     /* IMPORTANT: this must be called */
     import_array();
}


void CFill_Gap_By_NeighbourPoint(int *lpDIBorigin, int iImgWidth, int iImgHeight, int iNumberOfRepeat, int iFillValue)
{
    if(lpDIBorigin == NULL)    //DIB has not been allocated
		return;

	int   *pRowUp, *pRowMiddle, *pRowDown, *pRowBuffer,* pRowBuffer0;
	int *lpDataUp, *lpDataDown,*lpDIB;

	//&
	lpDataUp = NULL;

	pRowBuffer0= ( int  * )malloc( iImgWidth * 3 *sizeof(int));
	pRowUp		= pRowBuffer0;
	pRowMiddle  = pRowBuffer0 + iImgWidth;
	pRowDown	= pRowBuffer0 + iImgWidth * 2;

  //yuanbo 20171103-->
  int *pColumUp_left;
  pColumUp_left = (int *)malloc(iImgHeight*sizeof(int));
  memset(pColumUp_left,0,iImgHeight*sizeof(int));
  int *pColumUp_right;
  pColumUp_right = (int *)malloc(iImgHeight*sizeof(int));
  memset(pColumUp_right,0,iImgHeight*sizeof(int));
  //yuanbo 20171103<--


	long i, iRow;
    long myNumberOfRepeat;
	for( myNumberOfRepeat=0; myNumberOfRepeat < iNumberOfRepeat; myNumberOfRepeat++)
	{
		memset( pRowBuffer0, 0, iImgWidth * 3 );

		//for the first line
		lpDIB = lpDIBorigin +1;
		lpDataDown =lpDIB + iImgWidth;

		for( i= 1 ; i < (iImgWidth - 1); i++)
		{
			if (*lpDIB == iFillValue)   //  need to fill a value for this point
			{
				/*					if(m_bIsInOrb[i] == 0){//if(!rgn.PtInRegion (i,iRow)){
				lpDIB ++;
				lpDataUp ++;
				lpDataDown ++;
				continue;
				}
				*/
				if (lpDIB[1] != iFillValue )			// the right point
				{
					*lpDIB =lpDIB[1];		pRowUp[i]=1;
				}
				else if( *lpDataDown != iFillValue )	// the down point
				{
					*lpDIB = *lpDataDown;	pRowUp[i]=1;
				}
				else if (lpDIB[-1] != iFillValue && pRowUp[i-1] != 1)		// the left point
				{
					*lpDIB =lpDIB[-1];		pRowUp[i]=1;
				}
				else if( lpDataDown[1] != iFillValue )	// the down- right point
				{
					*lpDIB = lpDataDown[1];	pRowUp[i]=1;
				}
				else if (lpDataDown[-1] != iFillValue)	// the down-left point
				{
					*lpDIB =lpDataDown[-1];	pRowUp[i]=1;
				}
			}

			lpDIB ++;
			lpDataUp ++;
			lpDataDown ++;
		}

	//for the internal points
		for (iRow=1; iRow < (iImgHeight-1) ; iRow++)
		{
			lpDIB = lpDIBorigin +  iImgWidth  *  iRow + 1;
			lpDataUp =lpDIB - iImgWidth ;
			lpDataDown =lpDIB + iImgWidth ;

			for( i= 1 ; i < (iImgWidth - 1); i++)
			{
				if (*lpDIB == iFillValue)	//  need to fill a value for this point
				{
					/*if(m_bIsInOrb[iRow*iImgWidth+i] == 0){//if(!rgn.PtInRegion (i,iRow)){
						lpDIB ++;
						lpDataUp ++;
						lpDataDown ++;
						continue;
					}*/
					if (lpDIB[1] != iFillValue && pRowMiddle[i+1] != 1)			// the right point
					{
						*lpDIB =lpDIB[1];			pRowMiddle[i]=1;
					}
					else if( *lpDataDown != iFillValue )						// the down point
					{
						*lpDIB = lpDataDown[0];		pRowMiddle[i]=1;
					}
					else if (lpDIB[-1] != iFillValue && pRowMiddle[i-1] != 1)	// the left point
					{
						*lpDIB =lpDIB[-1];			pRowMiddle[i]=1;
					}
					else if (*lpDataUp != iFillValue && pRowUp[i] != 1)			// the up point
					{
						*lpDIB = lpDataUp[0];		pRowMiddle[i]=1;
					}
					else if ( lpDataUp[1] != iFillValue && pRowUp[i+1] != 1)	// the up- right point
					{
						*lpDIB =  lpDataUp[1];		pRowMiddle[i]=1;
					}
					else if( lpDataDown[1] != iFillValue )						// the down- right point
					{
						*lpDIB = lpDataDown[1];		pRowMiddle[i]=1;
					}
					else if (lpDataDown[-1] != iFillValue)						// the down-left point
					{
						*lpDIB =lpDataDown[-1];		pRowMiddle[i]=1;
					}
					else if (lpDataUp[-1] != iFillValue && pRowUp[i-1] != 1)	// the up-left point
					{
						*lpDIB =lpDataUp[-1];		pRowMiddle[i]=1;
					}
				}

				lpDIB ++;
				lpDataUp ++;
				lpDataDown ++;
			}

			pRowBuffer		= pRowUp;
			pRowUp			= pRowMiddle;
			pRowMiddle		= pRowDown;
			pRowDown		= pRowBuffer;

			memset(pRowDown, 0, iImgWidth);
		}
	}

	// for the last line
	lpDIB		= lpDIBorigin + iImgWidth * (iImgHeight-1) + 1;
	lpDataUp	= lpDIB - iImgWidth;

	for( i= 1 ; i < (iImgWidth- 1 ); i++)
	{
		if (*lpDIB == iFillValue)	//  need to fill a value for this point
		{
			///*if(m_bIsInOrb[i + iImgWidth  *   (iImgHeight-1)] == 0){//if(!rgn.PtInRegion (i,iRow))
			//{
			//	lpDIB ++;
			//	lpDataUp ++;
			//	lpDataDown ++;
			//	continue;
			//}
			//*/
			if (lpDIB[1] != iFillValue && pRowMiddle[i+1] != 1)			// the right point
			{
				*lpDIB =lpDIB[1];
				pRowMiddle[i]=1;
			}
			else if (lpDIB[-1] != iFillValue && pRowMiddle[i-1] != 1)	// the left point
			{
				*lpDIB =lpDIB[-1];
				pRowMiddle[i]=1;
			}
			else if (*lpDataUp != iFillValue && pRowUp[i] != 1)			// the up point
			{
				*lpDIB = lpDataUp[0];
				pRowMiddle[i]=1;
			}
			else if ( lpDataUp[1] != iFillValue && pRowUp[i+1] != 1)	// the up- right point
			{
				*lpDIB =  lpDataUp[1];
				pRowMiddle[i]=1;
			}
			else if (lpDataUp[-1] != iFillValue && pRowUp[i-1] != 1)	// the up-left point
			{
				*lpDIB =lpDataUp[-1];
				pRowMiddle[i]=1;
			}
		}

		lpDIB ++;
		lpDataUp ++;
		lpDataDown ++;
	}

	//for the left column
	lpDIB = lpDIBorigin;

	for(i = 1; i < (iImgHeight - 1); i++)
	{
		lpDIB += iImgWidth;

		if (*lpDIB == iFillValue)	//  need to fill a value for this point
		{
			///*if(m_bIsInOrb[i * iImgWidth] == 0){//if(!rgn.PtInRegion (i,iRow))
			//{
			//	continue;
			//}*/
			if (lpDIB[1] != iFillValue)					// the right point
			{
				*lpDIB = lpDIB[1];
			}
			else if( lpDIB[iImgWidth] != iFillValue)	// the down point
			{
				*lpDIB = lpDIB[iImgWidth];
			}
			//else if (lpDIB[-iImgWidth] != iFillValue)	// the up point
			else if (lpDIB[-iImgWidth] != iFillValue && pColumUp_left[i-1] != 1)	// yuanbo 20171103 
			{
				*lpDIB = lpDIB[-iImgWidth];
				pColumUp_left[i] = 1;//yuanbo 20171103 
			}
		}
	}

	//for the right column
	lpDIB = lpDIBorigin + iImgWidth - 1;

	for(i = 1; i < (iImgHeight - 1); i++)
	{
		lpDIB  += iImgWidth;

		if (*lpDIB == iFillValue)	//  need to fill a value for this point
		{
			///*if(m_bIsInOrb[(i+1) * iImgWidth-1] == 0){//if(!rgn.PtInRegion (i,iRow))
			//{
			//	continue;
			//}*/
			if (lpDIB[-1] != iFillValue)				// the left point
			{
				*lpDIB = lpDIB[-1];
			}
			else if( lpDIB[iImgWidth] != iFillValue)	// the down point
			{
				*lpDIB = lpDIB[iImgWidth];
			}
			//else if (lpDIB[-iImgWidth] != iFillValue)	// the up point
			else if (lpDIB[-iImgWidth] != iFillValue && pColumUp_right[i-1] != 1)	// yuanbo 20171103 
			{
				*lpDIB = lpDIB[-iImgWidth];
				pColumUp_right[i] = 1;//yuanbo 20171103 

			}
		}
	}

	free(pRowBuffer0);

	return;
}


void CFill_Gap_By_InterpolatingAlongY(unsigned short *lpDIBorigin, int iImgWidth, int iImgHeight, int iInputType, short iFillValue, short iBadData)
{
    if(lpDIBorigin == NULL) return ;   //DIB has not been allocated

	long iCol,  iRow;
	long iYstart,iYend;
	double dV1,dV2;
	short *lpDIB = lpDIBorigin ;
	short *p;
	for( iCol= 0 ; iCol < iImgWidth; iCol++){


		iYstart=0;
		lpDIB = lpDIBorigin + iCol;
		p= lpDIB;

		//find the first  valid point
		if( *p == iFillValue){
			while(*p == iFillValue){  //find the fisrt point with valid value
				iYstart++;
				p += iImgWidth;
				if(iYstart >= iImgHeight)  break;
			}
		}

		//now p point has value; iYStart

		while(iYstart < iImgHeight) {
			while(*p != iFillValue){  //find the fisrt point with invalid value
				iYstart++;
				p += iImgWidth;
				if(iYstart >= iImgHeight)  break;

			}

			if(iYstart < iImgHeight) {
				iYend =iYstart ;
				iYstart--;

				while(*p == iFillValue){  //find the fisrt point with invalid value
					iYend++;
					p += iImgWidth;
					if(iYend >= iImgHeight)  break;
				}
				if(iYend < iImgHeight){

					//interpolate the points between iYstart and iYend
					if(iInputType == 0 ){ // WORD
						dV2 = (double)(*p) /(double)(iYend-iYstart);
						p = lpDIB + iYstart * iImgWidth ;
						dV1 = (double)(*p) /(double)(iYend-iYstart);
						for(iRow =iYstart +1; iRow <iYend; iRow++){
							p += iImgWidth;
							if(*p != iBadData ) *p = (int)(dV2 *(iRow - iYstart) + dV1 *(iYend -iRow));
						}
					}else{ //short int
						short int n;
						n= (short int)(*p);
						dV2 = (double)(n) /(double)(iYend-iYstart);
						p = lpDIB + iYstart * iImgWidth ;
						n= (short int)(*p);
						dV1 = (double)(n) /(double)(iYend-iYstart);
						for(iRow =iYstart +1; iRow <iYend; iRow++){
							p += iImgWidth;
							n = (int)(dV2 *(iRow - iYstart) + dV1 *(iYend -iRow));
							if(( short)(*p) != iBadData ) *p =(short)n;
						}
					}
				}

				iYstart =iYend;
				p = lpDIB + iYstart * iImgWidth ;

			}else
				break;
		}


	}//loop: iCol


}


void CFill_Gap_By_InterpolatingAlongX(unsigned short *lpDIBorigin, int iImgWidth, int iImgHeight, int iInputType, short iFillValue, short iBadData)
{
    if(lpDIBorigin == NULL) return ;   //DIB has not been allocated
	long iCol,  iRow;
	long iXstart,iXend;
	double dV1,dV2;
	short *lpDIB = lpDIBorigin ;
	short *p;
	for( iRow= 0 ; iRow < iImgHeight; iRow++){


		iXstart=0;
		lpDIB = lpDIBorigin + iRow * iImgWidth;
		p= lpDIB;

		//find the first  valid point
		if( *p == iFillValue){
			while(*p == iFillValue){  //find the fisrt point with valid value
				iXstart++;
				p++;
				if(iXstart >= iImgWidth)  break;
			}
		}

		//now p point has value; iYStart

		while(iXstart < iImgWidth) {
			while(*p != iFillValue){  //find the fisrt point with invalid value
				iXstart++;
				p++;
				if(iXstart >= iImgWidth)  break;
			}

			if(iXstart < iImgWidth) {
				iXend =iXstart ;
				iXstart--;

				while(*p == iFillValue){  //find the fisrt point with invalid value
					iXend++;
					p++;
					if(iXend >= iImgWidth)  break;
				}
				if(iXend < iImgWidth){

					//interpolate the points between iXstart and iXend
					if(iInputType == 0 ){ // WORD
						dV2 = (double)(*p) / (double)(iXend-iXstart);
						p = lpDIB +  iXstart;
						dV1 = (double)(*p) /(double)(iXend-iXstart);
						for(iCol =iXstart +1; iCol <iXend; iCol++){
							p ++;
							if(*p != iBadData ) *p = (int)(dV2 *(iCol - iXstart) + dV1 *(iXend -iCol));
						}
					}else{ //short int
						short int n;
						n= (short int)(*p);
						dV2 = (double)(n) /(double)(iXend-iXstart);
						p = lpDIB + iXstart;
						n= (short int)(*p);
						dV1 = (double)(n) /(double)(iXend-iXstart);
						for(iCol =iXstart +1; iCol <iXend; iCol++){
							p ++;
							n = (int)(dV2 *(iCol - iXstart) + dV1 *(iXend -iCol));
							if((short)(*p) != iBadData ) *p = (short)n;
						}
					}
				}

				iXstart =iXend;
				p = lpDIB +  iXstart;

			}else
				break;
		}


	}//loop: iCol

}